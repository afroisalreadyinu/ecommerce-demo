# E-Commerce Demo

A demo application for exercising testing techniques, especially
test-driven design.

## Functional Scope

In this repo, some basic functions of a standard ecommerce application
are implemented. These are:

- Users

- Simplified product information

- Stock availability

- Orders
  + Order information
  + Adding, removing, modifying order items

- Routing & shipments

- Returns & cancellations

- Payment

All domains are extremely simplified (especially the last one, which
is a hell of its own), but functional complexities are meant to be
part of the application, to verify the effectiveness of test-driven
design.

### Users

Authentication and authorization are not the point of this demo, so
they are kept to a minimum. A user can sign up and create a company at
the same time. Every member of a company can add new users using an
end point for this purpose. Authentication is also rather limited;
it's based on setting a cookie, which means that you need a client
with that capability for API scripts. Security is not the point of
this demo.

### Product information & stock availability

A product consists of a GTIN, a label, and a free-form dictionary of
attributes. The stock information for products is kept on the basis of
storage locations. Each product can have three kinds of stock in a
certain storage location:

- Physical: The number of physical items available
- Sold: The number that is bound to paid orders
- Reserved: The number that is bound to unpaid orders

These numbers are adjusted according to incoming orders. On the basis
of these numbers, the available-to-purchase (ATP) quantity is
calculated.

### Orders

An order consists of an order id, customer name and address, and a
list of order items. An order item is a product and quantity. Both
order and order item have status fields that give information on
whether the order or item have been packed or shipped. There is also
another field on order that signals the payment status.

### Routing & shipments

Once an order is placed, it is possible to ship this order from one of
the various storage locations by making a routing request. The
conditions for this routing are controlled using a number of options.

### Returns and cancellations

An order can be completely or partially cancelled or returned,
depending on various conditions.

## Building and running

1. Install Python 3, or make sure that you have it.

2. Create a virtualenv and activate it.

3. Run `pip install -r requirements.txt`. If you also want to execute
the tests, run `pip install -r test_requirements.txt`.

4. Run `python setup.py develop`.

Afterwards, you should be able to initialize the test database
(located at `/tmp/ecomm-demo.db`) with `init-ecomm-db`, and run the
application with `run-ecomm-demo`.