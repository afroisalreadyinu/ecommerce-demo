import os
from setuptools import setup

dependencies = ['Flask', 'Flask-SQLAlchemy', 'passlib', 'attrs']
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
        'console_scripts': ['run-ecomm-demo = ecomm_demo.run:run_app',
                            'init-ecomm-db = ecomm_demo.run:create_db']
    },
    url = "https://github.com/afroisalreadyinu/",
)
