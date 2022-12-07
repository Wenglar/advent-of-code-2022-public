*** Settings ***
Resource        keywords.resource
Suite Setup     Run Keywords    Prepare Command History File    ${FILE}     AND     Extract File System From File
Task Teardown   Log Result


*** Variables ***
${FILE}     ${CURDIR}/input.txt

*** Tasks ***
Sum Of Total Sizes
    Calculate Total Sum Of Folders Of Maximum Size 100000

Smallest Folder To Delete
    Find The Lowest Folder Total Size To Get At Least 30000000 Out Of 70000000 freed.
