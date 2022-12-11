*** Settings ***
Library     MonkeyLibrary.py

*** Variables ***
@{mb_individual}
${mb_level}         0

*** Keywords ***
Prepare File
    [Arguments]             ${file_path}
    Set File And Validate   ${file_path}

Initialize Monkeys
    Load File

Use Default Worry Level Divider
    Set Worry Level Management  //  ${3}

Use Custom Worry Level Divider
    ${divider} =                Get Product Of Test Dividors
    Set Worry Level Management  \%  ${divider}

Execute ${round_cnt:\d+} Rounds And Calculate Level Of Monkey Bussiness
    ${round_cnt} =      Convert to Integer      ${round_cnt}

    Execute Rounds      ${round_cnt}
    @{mb_individual} =  Get All Monkey Interactions
    ${mb_level} =       Get Monkey Business Level

    Set Task Variable   @{mb_individual}
    Set Task Variable   ${mb_level}

Log Result
    Log     \n\tInteraction of individual monkeys: @{mb_individual}\n\tMonkey Business Level: "${mb_level}"     console=True
