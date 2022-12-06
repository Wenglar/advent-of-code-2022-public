*** Settings ***
Resource        keywords.resource
Suite Setup     Prepare Stream File     ${FILE}
Task Teardown   Log Result


*** Variables ***
${FILE}     ${CURDIR}/input.txt

*** Tasks ***
Start-Of-Packet Marker Position
    Count Characters Until First Start-Of-Packet Marker Received

Start-Of-Message Marker Position
    Count Characters Until First Start-Of-Message Marker Received
