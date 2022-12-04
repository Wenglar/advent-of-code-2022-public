*** Settings ***
Resource    keywords.resource

*** Variables ***
${FILE}     ${CURDIR}/input.txt

*** Tasks ***
Count Assignment Pairs Where One Fully Contains The Other
    Load Assignments From File          ${FILE}
    Count Pairs Where One Is Redundant
    Log Result For Redundancies

Count Assignment Pairs Where There Is An Overlap
    Load Assignments From File          ${FILE}
    Count Pairs That Overlap
    Log Result For Overlaps
