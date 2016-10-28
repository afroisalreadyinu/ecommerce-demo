import json

import behave
from hamcrest import assert_that, equal_to

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

# Product import etc

@behave.given('the user is logged in')
def step_impl(context):
    if context.client.logged_in():
        return
    data = {'email': USER_EMAIL, 'password': USER_PASSWORD, 'company': USER_COMPANY}
    response = context.client.post_json('/signup', data)
    assert_that(response.status_code, equal_to(200))
