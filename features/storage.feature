Feature: Storage

  Scenario: Create a storage location
     Given the user is logged in
      when the user posts the new storage location form
      then a new storage location is created