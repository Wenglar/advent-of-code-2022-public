*** Settings ***
Resource        keywords.resource
Task Setup      Run Keywords    Prepare File    ${FILE}     AND     Initialize Monkeys
Task Teardown   Log Result


*** Variables ***
${FILE}     ${CURDIR}/input.txt

*** Tasks ***
Monkey Business After 20 Cycles
    Use Default Worry Level Divider
    Execute 20 Rounds And Calculate Level Of Monkey Bussiness

Monkey Business After 10000 Cycles
    Use Custom Worry Level Divider
    Execute 10000 Rounds And Calculate Level Of Monkey Bussiness
