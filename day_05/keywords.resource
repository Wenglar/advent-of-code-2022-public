*** Settings ***
Library     CratesLibrary.py

*** Variables ***
${result}

*** Keywords ***
Load Initial State And Steps From File
    [Arguments]                 ${file_path}
    Set File And Validate       ${file_path}
    Extract Initial State And Steps

Apply Steps Using ${name} ${subname:\d+}
    ${number} =         Convert To Integer  ${subname}
    Validate Crane      ${number}
    ${identical} =      Apply Steps     ${number}
    ${result} =         Get Top Row

    Set Task Variable   ${result}

Count Pairs That Overlap
    ${result} =         Get Count Of Overlaps

    Set Task Variable   ${result}

Log Top Row For ${name} ${subname:\d+}
    Log                 \n\tThe top row after using ${name} ${subname} is: "${result}"      console=True
