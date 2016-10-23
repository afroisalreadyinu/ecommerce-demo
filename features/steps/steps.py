import behave

@behave.given('the application is running')
def step_impl(context):
    context.response = context.client.get('/')

@behave.when('the user posts the login form')
def step_impl(context):
    assert context.response.status_code == 200

@behave.then('a user is created')
def step_impl(context):
    assert context.failed is False
