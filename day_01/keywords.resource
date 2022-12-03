*** Settings ***
Library    CustomLibrary.py

*** Variables ***
${last_1_elf}
${last_3_elves}
${max}

*** Keywords ***
Load Elf Calories From File
    [Arguments]    ${file_path}
    Load And Process File    ${file_path}

Sort Elves In Ascending Order
    Sort Values

Get Elf With Maximum
    ${max} =            Get Maximum Value
    Set Test Variable   ${max}

Get 1 Last Elf
    ${last_1_elf} =     Get Last N Values       ${1}
    Set Test Variable   ${last_1_elf}

Get ${number:\d+} Last Elves
    ${number} =         Convert To Integer  ${number}
    ${last_3_elves} =   Get Last N Values   ${number}
    Set Test Variable   ${last_3_elves}

Verify Last Elf Has Maximum
    Should Be Equal     ${last_1_elf}[0]    ${max}
    Log                 \n\tCalories of last elf: "${last_1_elf}[0]"    console=True

Log Info For 3 Last Elves
    ${sum} =            Evaluate    sum(map(int, ${last_3_elves}))
    Log                 \n\tCalories of 3 last elves: List "${last_3_elves}" gives total of "${sum}"    console=True
