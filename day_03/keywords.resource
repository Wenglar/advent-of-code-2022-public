*** Settings ***
Library    RucksackLibrary.py

*** Variables ***
${result}

*** Keywords ***
Load Rucksacks From File
    [Arguments]         ${file_path}
    Load File           ${file_path}
    Validate Rucksacks

Split Rucksacks To Compartments And Find Duplicates
    Get Compartment Duplicates

Group Rucksacks To Triplets And Find Duplicates
    Get Triplet Duplicates

Evaluate Duplicates And Sum Their Values
    Evaluate Duplicates
    Validate Duplicate Values
    ${result} =         Sum Duplicates

    Set Task Variable   ${result}

Log Result
    Log     \n\tTotal value of duplicates is: "${result}"       console=True
