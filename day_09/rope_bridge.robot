*** Settings ***
Resource        keywords.resource
Suite Setup     Run Keywords    Prepare File    ${FILE}     AND     Extract Rope Head Movements
Task Teardown   Log Result


*** Variables ***
${FILE}     ${CURDIR}/input.txt

*** Tasks ***
Tail Position Count With Two Knots
    Perform Head Movements And Count Unique Tail Positions For 2 Knots

Tail Position Count With Ten Knots
    Perform Head Movements And Count Unique Tail Positions For 10 Knots
