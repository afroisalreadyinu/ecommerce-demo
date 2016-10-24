import os
from setuptools import setup

dependencies = ['Flask', 'Flask-SQLAlchemy', 'passlib']
test_dependencies = ['behave', 'PyHamcrest']

setup(
    name = "ecommerce-demo",
    version = "0.01",
    author = "Ulas Tuerkmen",
    author_email = "ulas.tuerkmen@gmail.com",
    description = ("A demo ecommerce application"),
    install_requires = dependencies,
    tests_require = test_dependencies,
    packages=['ecomm_demo'],
    entry_points = {
        'console_scripts': ['run-ecomm = ecomm_demo:run_app']
    },
    url = "https://github.com/afroisalreadyinu/",
)
