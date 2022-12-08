*** Settings ***
Resource        keywords.resource
Suite Setup     Run Keywords    Prepare File    ${FILE}     AND     Extract Forest Map From File
Task Teardown   Log Result


*** Variables ***
${FILE}     ${CURDIR}/input.txt

*** Tasks ***
Count Visible Trees
    Count Trees That Are Visible From Outside

The Highest View Score
    Find The Highest View Score
