*** Settings ***
Resource        keywords.resource
Task Setup      Run Keywords    Prepare File    ${FILE}     AND     Extract Instructions
Task Teardown   Log Result


*** Variables ***
${FILE}     ${CURDIR}/input.txt

*** Tasks ***
Sum Of Signal Strengths
    Set First Examination At Cycle 20 And Cycle Step To 40
    Execute Instructions And Sum Signal Strengths At Examined Cycles

Draw CRT Output
    Set CRT Display Width To 40 Pixels
    Execute Instructions, Move Sprite Accordingly And Draw Ouput
