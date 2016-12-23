import json

import behave
from hamcrest import assert_that, equal_to, is_in

USER_EMAIL =  'goofy@acmeinc.com'
USER_PASSWORD = 'secret'
USER_COMPANY = 'Acme Inc'

def to_json(response):
    return json.loads(response.data.decode(response.charset))

@behave.given('the application is running')
def step_impl(context):
    response = context.client.get('/')
    assert_that(response.status_code, equal_to(200))
    assert_that(to_json(response), equal_to({}))

@behave.when('the user posts the signup form')
def step_impl(context):
    data = {'email': USER_EMAIL, 'password': USER_PASSWORD, 'company': USER_COMPANY}
    response = context.client.post_json('/signup', data)
    context.response = response

@behave.then('a user and its company are created')
def step_impl(context):
    assert_that(context.response.status_code, equal_to(200))
    json_response = to_json(context.response)
    assert_that(json_response['email'], equal_to(USER_EMAIL))
    assert_that(json_response['company'], equal_to(USER_COMPANY))

@behave.then('an error message is returned')
def step_impl(context):
    assert_that(context.response.status_code, equal_to(400))
    json_response = to_json(context.response)
    assert_that(json_response['error'], 'User exists')

@behave.given('the user has logged out')
def step_impl(context):
    response = context.client.get('/logout')
    assert_that(response.status_code, equal_to(200))

@behave.when('the user posts the login form')
def step_impl(context):
    data = {'email': USER_EMAIL, 'password': USER_PASSWORD}
    response = context.client.post_json('/login', data)
    assert_that(response.status_code, equal_to(200))
    json_response = to_json(response)
    assert_that(json_response['email'], equal_to(USER_EMAIL))

@behave.then('the user is logged in')
def step_impl(context):
    response = context.client.get('/')
    assert_that(response.status_code, equal_to(200))
    json_response = to_json(response)
    assert_that(json_response['email'], equal_to(USER_EMAIL))

@behave.when('the user posts the invite form')
def step_impl(context):
    data = {'invitee_email': 'seconduser@comp.com'}
    response = context.client.post_json('/invite', data)
    assert_that(response.status_code, equal_to(200))
    context.response_data = to_json(response)

@behave.then('an invitation is sent')
def step_impl(context):
    """
    Since sending emails is mocked, this step is oversimplified, but
    it would still be an interesting exercise to figure out how to
    check the sending of emails at all.
    """
    assert_that(context.response_data['recipient'], 'seconduser@comp.com')

@behave.then('invitation can be used to sign up')
def step_impl(context):
    invitations = to_json(context.client.get('/invite'))
    assert_that(len(invitations), equal_to(1))
    nonce = invitations[0]['nonce']
    email = invitations[0]['email']
    response = context.client.get('/logout')
    data = {'nonce': nonce, 'password': 'test'}
    response = context.client.post_json('/signup-with-invitation', data)
    assert_that(response.status_code, equal_to(200))
    data = {'email': email, 'password': 'test'}
    response = context.client.post_json('/login', data)
    assert_that(response.status_code, equal_to(200))
    json_response = to_json(response)
    assert_that(json_response['email'], equal_to(email))
    assert_that(json_response['company'], equal_to(USER_COMPANY))

# Product import etc

@behave.given('the user is logged in')
def step_impl(context):
    if context.client.logged_in():
        return
    data = {'email': USER_EMAIL, 'password': USER_PASSWORD, 'company': USER_COMPANY}
    response = context.client.post_json('/signup', data)
    assert_that(response.status_code, equal_to(200))

@behave.when('the user posts a list of products')
def step_impl(context):
    products = [x.as_dict() for x in context.table.rows]
    response = context.client.post_json('/products', products)
    assert_that(response.status_code, equal_to(200))
    context.products = products

@behave.then('the products are imported')
def step_impl(context):
    response = context.client.get('/products')
    assert_that(response.status_code, equal_to(200))
    json_response = to_json(response)
    assert_that(len(json_response), equal_to(len(context.products)))
    no_stock = {'physical': 0, 'sold': 0, 'reserved': 0, 'atp': 0}
    for product in json_response:
        assert_that('id', is_in(product))
        product.pop('id')
        stock = product.pop('stock')
        assert_that(stock, equal_to(no_stock))
        assert_that(product, is_in(context.products))

STORE_NAME = 'Store on Friedrichstrasse'

@behave.when('the user posts the new storage location form')
def step_impl(context):
    data = {'label': STORE_NAME}
    response = context.client.post_json('/storage', data)
    assert_that(response.status_code, equal_to(200))
    context.storage = to_json(response)

@behave.then('a new storage location is created')
def step_impl(context):
    assert_that(context.storage['label'], equal_to(STORE_NAME))
    response = context.client.get('/storage')
    assert_that(response.status_code, equal_to(200))
    storages = to_json(response)
    assert_that(len(storages), equal_to(1))
    assert_that(storages[0]['label'], equal_to(STORE_NAME))

@behave.given('a product is imported')
def step_impl(context):
    products = [x.as_dict() for x in context.table.rows]
    context.client.post_json('/products', products)

@behave.given('storage location exists')
def step_impl(context):
    storages = to_json(context.client.get('/storage'))
    if storages:
        context.storage_location_id = storages[0]['id']
    else:
        storage = to_json(context.client.post_json(
            '/storage', {'label': STORE_NAME}))
        context.storage_location_id = storage['id']

@behave.when('the user posts inventory to stock intake')
def step_impl(context):
    intakes = [x.as_dict() for x in context.table.rows]
    for intake in intakes:
        intake['intake'] = int(intake['intake'])
    context.intakes = intakes
    storage_path = '/storage/{}/stock'.format(context.storage_location_id)
    response = context.client.post_json(storage_path, intakes)
    assert_that(response.status_code, equal_to(200))

@behave.then('the stock value is increased')
def step_impl(context):
    resp = context.client.get('/storage/{}/stock'.format(context.storage_location_id))
    assert_that(resp.status_code, equal_to(200))
    stock = to_json(resp)
    assert_that(len(stock), 1)
    assert_that(stock[0]['stock']['physical'], equal_to(context.intakes[0]['intake']))
    assert_that(stock[0]['stock']['sold'], equal_to(0))
    assert_that(stock[0]['stock']['reserved'], equal_to(0))

@behave.then('product shows total inventory')
def step_impl(context):
    resp = context.client.get('/products')
    assert_that(resp.status_code, equal_to(200))
    products = to_json(resp)
    assert_that(len(products), 1)
    assert_that(products[0]['stock']['physical'], equal_to(10))
    assert_that(products[0]['stock']['atp'], equal_to(10))
