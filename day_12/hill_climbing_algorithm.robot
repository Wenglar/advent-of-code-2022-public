*** Settings ***
Resource        keywords.resource
Task Setup      Run Keywords    Prepare File    ${FILE}     AND     Initialize Map
Task Teardown   Log Result


*** Variables ***
${FILE}     ${CURDIR}/input.txt

*** Tasks ***
Find Way From Start To End
    Set Start To Default Start
    Find The Shortest Path To The Highest Point

Find The Shortest Way From Bottom To The End
    Set Start To Default End
    Find The Shortest Path To The Bottom
