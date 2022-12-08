*** Settings ***
Library     TreeLibrary.py

*** Variables ***
${result}
${log_text}

*** Keywords ***
Prepare File
    [Arguments]             ${file_path}
    Set File And Validate   ${file_path}

Extract Forest Map From File
    Load Forest Layout

Count Trees That Are Visible From Outside
    ${total_cnt} =      Get Total Tree Count
    ${log_text} =       Set Variable            The number of visible trees out of ${total_cnt} is

    ${result} =         Get Visible Tree Count

    Set Task Variable   ${result}
    Set Task Variable   ${log_text}

Find The Highest View Score
    ${log_text} =       Set Variable            The highest view score is

    ${result} =         Get Highest View Score

    Set Task Variable   ${result}
    Set Task Variable   ${log_text}

Log Result
    Log     \n\t${log_text}: "${result}"    console=True
