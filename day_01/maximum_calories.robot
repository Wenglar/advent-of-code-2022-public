*** Settings ***
Resource        keywords.resource

*** Variables ***
${FILE}     ${CURDIR}/input.txt

*** Test Cases ***
Total Maximum
    Load Elf Calories From File     ${FILE}
    Get Elf With Maximum
    Sort Elves In Ascending Order
    Get 1 Last Elf
    Verify Last Elf Has Maximum

Total Of 3 Maximum
    Load Elf Calories From File     ${FILE}
    Sort Elves In Ascending Order
    Get 3 Last Elves
    Log Info For 3 Last Elves
