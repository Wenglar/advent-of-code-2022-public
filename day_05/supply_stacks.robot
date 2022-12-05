*** Settings ***
Resource    keywords.resource

*** Variables ***
${FILE}     ${CURDIR}/input.txt

*** Tasks ***
Get Top Row Using CrateMover 9000
    Load Initial State And Steps From File      ${FILE}
    Apply Steps Using CrateMover 9000
    Log Top Row For CrateMover 9000

Get Top Row Using CrateMover 9001
    Load Initial State And Steps From File      ${FILE}
    Apply Steps Using CrateMover 9001
    Log Top Row For CrateMover 9001
