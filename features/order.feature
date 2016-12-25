Feature: Orders

  @wip
  Scenario: Create an order
     Given the user is logged in
       and a product is imported
	| label        | gtin           |
	| Leather shoe | 00845982006196 |
      when the user posts order data
      then an order is created