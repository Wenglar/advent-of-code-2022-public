*** Settings ***
Library     AssignmentsLibrary.py
Library     String

*** Variables ***
${result}

*** Keywords ***
Load Assignments From File
    [Arguments]         ${file_path}
    Load File           ${file_path}

Count Pairs Where One Is Redundant
    ${part1} =          Get Count Of Firsts In Seconds
    ${part2} =          Get Count Of Seconds In Firsts
    ${identical} =      Get Count Of Identical
    ${result} =         Evaluate    ${part1} + ${part2} - ${identical}

    Set Task Variable   ${result}

Count Pairs That Overlap
    ${result} =         Get Count Of Overlaps

    Set Task Variable   ${result}

Log Result For ${strategy}
    ${strategy} =       Convert To Lowercase    ${strategy}
    Log                 \n\tThe number of ${strategy} is: "${result}"       console=True
