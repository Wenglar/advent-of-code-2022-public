*** Settings ***
Library     SpaceLibrary.py

*** Variables ***
${result}
${log_text}

*** Keywords ***
Prepare Command History File
    [Arguments]             ${file_path}
    Set File And Validate   ${file_path}

Extract File System From File
    Extract File System

Calculate Total Sum Of Folders Of Maximum Size ${number:\d+}
    ${log_text} =       Set Variable            The sum of total folder sizes smaller than ${number} is
    ${number} =         Convert To Integer      ${number}

    ${result} =         Get Sum Of Sizes Where MaxSize      ${number}

    Set Task Variable   ${result}
    Set Task Variable   ${log_text}

Find The Lowest Folder Total Size To Get At Least ${needed:\d+} Out Of ${total:\d+} freed.
    ${log_text} =       Set Variable            The lowest folder total size to free enough space is
    ${needed} =         Convert To Integer      ${needed}
    ${total} =          Convert To Integer      ${total}

    ${result} =         Get Lowest To Free Enough   ${needed}   ${total}

    Set Task Variable   ${result}
    Set Task Variable   ${log_text}

Log Result
    Log     \n\t${log_text}: "${result}"    console=True
