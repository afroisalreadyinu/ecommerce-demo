Feature: Signup and login

  Scenario: Signup and create company
     Given the application is running
      when the user posts the signup form
      then a user and its company are created

  Scenario: Login
     Given the user has logged out
      when the user posts the login form
      then the user is logged in