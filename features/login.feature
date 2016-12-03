Feature: Signup and login

  Scenario: Signup and create company
     Given the application is running
      when the user posts the signup form
      then a user and its company are created

  Scenario: Signup with same credentials again
     Given the user has logged out
      when the user posts the signup form
      then an error message is returned

  Scenario: Login
     Given the user has logged out
      when the user posts the login form
      then the user is logged in

  @wip
  Scenario: Invite
     Given the user is logged in
      when the user posts the invite form
      then an invitation is sent