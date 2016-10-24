A demo application for exercising testing techniques, especially
test-driven design.

## Building and running

1. Install Python 3, or make sure that you have it.

2. Create a virtualenv and activate it.

3. Run `pip install -r requirements.txt`. If you also want to execute
the tests, run `pip install -r test_requirements.txt`.

4. Run `python setup.py develop`.

Afterwards, you should be able to initialize the test database
(located at `/tmp/ecomm-demo.db`) with `init-ecomm-db`, and run the
application with `run-ecomm-demo`.