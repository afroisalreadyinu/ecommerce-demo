Feature: Product import

  @wip
  Scenario: Import a product
     Given the user is logged in
      when the user posts a list of products
      then the products are imported and available
