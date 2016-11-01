Feature: Product import

  Scenario: Import a product
     Given the user is logged in
      when the user posts a list of products
	| label        | gtin           |
	| Leather shoe | 00845982006196 |
	| Sneakers     | 08716398158477 |
      then the products are imported
