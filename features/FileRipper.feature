@FileRipper
Feature: File Ripper Business Features

  Scenario Outline: A delimited with "<delimiter>" file is processed by file ripper
    Given a file whose fields are separated by a "<delimiter>"
    And a delimited file definition with "<delimiter>"
    When the file is ripped
    Then the file data is returned

    Examples:
      | delimiter |
      | \|        |
      | \t        |
      | ,         |
      | .         |

  Scenario: A fixed file is processed by file ripper
    Given a file whose fields are of fixed width
    And a fixed file definition
    When the file is ripped
    Then the file data is returned

  Scenario: An xml file is processed by file ripper
    Given a file in xml format
    And a xml file definition
    When the file is ripped
    Then the file data is returned
