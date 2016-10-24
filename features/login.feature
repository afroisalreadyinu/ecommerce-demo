Feature: Signup and login

  Scenario: Signup and create company
     Given the application is running
      when the user posts the signup form
      then a user and its company are created