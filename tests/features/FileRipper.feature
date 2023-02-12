@FileRipper
Feature: File Ripper Business Features

  Scenario Outline: A delimited with <delimiter> file is processed by file ripper
    Given a file whose fields are separated by a <delimiter>
    And a delimited file definition with <delimiter>
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
    When the files are ripped
    Then data is returned for all files

  Scenario: File ripper looks up files and processes them
    Given files stored on file system
    And a fixed file definition
    And file definition has input directory, file mask
    When the files are found and ripped
    Then data is returned for all files
    And files are still in input directory

  Scenario: File ripper looks up files, processes them, and moves them to completed
    Given files stored on file system
    And a fixed file definition
    And file definition has input directory, file mask
    And file definition has completed directory
    When the files are found and ripped
    Then data is returned for all files
    And files are in completed directory

  Scenario: A delimited file and a fixed file definition
    Given a file whose fields are separated by a ","
    And a fixed file definition
    When the file is ripped
    Then a IndexError occurs

  Scenario: A delimited file and a xml file definition
    Given a file whose fields are separated by a "|"
    And a xml file definition
    When the file is ripped
    Then a ParseError occurs

  Scenario: A fixed file and a xml file definition
    Given a file whose fields are of fixed width
    And a xml file definition
    When the file is ripped
    Then a ParseError occurs

  Scenario: A fixed file and a delimited file definition
    Given a file whose fields are of fixed width
    And a delimited file definition with "|"
    When the file is ripped
    Then a OSError occurs

  Scenario: A xml file and a delimited file definition
    Given a file in xml format
    And a delimited file definition with "\t"
    When the file is ripped
    Then a OSError occurs

  Scenario: A xml file and a fixed file definition
    Given a file in xml format
    And a fixed file definition
    When the file is ripped
    Then a IndexError occurs

