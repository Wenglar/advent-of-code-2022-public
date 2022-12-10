*** Settings ***
Library     RegisterLibrary.py

*** Variables ***
${result}
${log_text}

*** Keywords ***
Prepare File
    [Arguments]             ${file_path}
    Set File And Validate   ${file_path}

Extract Instructions
    Load File

Set First Examination At Cycle ${start:\d+} And Cycle Step To ${step:\d+}
    ${start} =              Convert to Integer      ${start}
    ${step} =               Convert to Integer      ${step}
    Set Examined Cycles     ${start}    ${step}

Execute Instructions And Sum Signal Strengths At Examined Cycles
    Execute Instructions And Examine Cycles
    ${cycles} =         Get Examined Cycles
    ${result} =         Get Sum Of Signal Strengths

    ${log_text} =       Set Variable    \n\tExamined cycles: ${cycles}\n\tSum Of Signal Strengths: "${result}"

    Set Task Variable   ${log_text}

Set CRT Display Width To ${width:\d+} Pixels
    ${width} =          Convert to Integer      ${width}
    Set Display Width   ${width}

Execute Instructions, Move Sprite Accordingly And Draw Ouput
    Execute Instructions And Draw CRT
    ${result} =         Get CRT output

    ${log_text} =       Set Variable    \n\tCRT output: ${result}

    Set Task Variable   ${log_text}

Log Result
    Log     ${log_text}     console=True
