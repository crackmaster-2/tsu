



Feature: Check su is installed

Scenario: Run a simple test
    Given user has Magisk installed
    When we check the version
    Then it returns the binary
