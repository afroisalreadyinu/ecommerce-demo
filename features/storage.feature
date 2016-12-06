Feature: Storage

  Scenario: Create a storage location
     Given the user is logged in
      when the user posts the new storage location form
      then a new storage location is created

  @wip
  Scenario: Import stock
     Given the user is logged in
       and storage location exists
       and a product is imported
	| label        | gtin           |
	| Leather shoe | 00845982006196 |
      when the user posts inventory to stock intake
	| gtin           | intake         |
	| 00845982006196 | 10             |
      then the stock value is increased