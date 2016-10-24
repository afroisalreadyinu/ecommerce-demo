import json

import behave
from hamcrest import assert_that, equal_to

def to_json(response):
    return json.loads(response.data.decode(response.charset))

@behave.given('the application is running')
def step_impl(context):
    response = context.client.get('/')
    assert_that(response.status_code, equal_to(200))
    assert_that(to_json(response), equal_to({}))

@behave.when('the user posts the signup form')
def step_impl(context):
    data = {'email': 'goofy@acmeinc.com', 'password': 'secret', 'company': 'Acme Inc'}
    response = context.client.post('/signup',
                                   data=json.dumps(data),
                                   content_type='application/json')
    context.response = response

@behave.then('a user and its company are created')
def step_impl(context):
    assert_that(context.response.status_code, equal_to(200))
    json_response = to_json(context.response)
    assert_that(json_response['email'], equal_to('goofy@acmeinc.com'))
    assert_that(json_response['company'], equal_to('Acme Inc'))
