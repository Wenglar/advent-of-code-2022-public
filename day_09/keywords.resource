*** Settings ***
Library     RopeLibrary.py

*** Variables ***
${result}
${log_text}

*** Keywords ***
Prepare File
    [Arguments]             ${file_path}
    Set File And Validate   ${file_path}

Extract Rope Head Movements
    Load Directions

Perform Head Movements And Count Unique Tail Positions For ${number:\d+} Knots
    ${number} =         Convert to Integer      ${number}
    Verify Knot Count   ${number}

    Initialize Knots    ${number}
    Perform Movements
    ${result} =         Get Unique Tail Position Count

    Set Task Variable   ${number}
    Set Task Variable   ${result}

Log Result
    Log     \n\tNumber of unique tail positions for ${number} knots: "${result}"    console=True
