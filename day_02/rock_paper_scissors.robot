*** Settings ***
Resource        keywords.resource

*** Variables ***
${FILE}     ${CURDIR}/input.txt

*** Tasks ***
Strategy 1
    Load Events From File       ${FILE}
    Execute Part 1 Strategy
    Log Result

Strategy 2
    Load Events From File       ${FILE}
    Execute Part 2 Strategy
    Log Result
