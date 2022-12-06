*** Settings ***
Library     TuningLibrary.py

*** Variables ***
${result}

*** Keywords ***
Prepare Stream File
    [Arguments]             ${file_path}
    Set File And Validate   ${file_path}

Count Characters Until First Start-Of-Packet Marker Received
    ${result} =         Get First Unique Set        ${4}

    Set Task Variable   ${result}

Count Characters Until First Start-Of-Message Marker Received
    ${result} =         Get First Unique Set        ${14}

    Set Task Variable   ${result}

Log Result
    Log     \n\tThe number of characters received: "${result}"      console=True
