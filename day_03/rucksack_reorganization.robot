*** Settings ***
Resource    keywords.resource

*** Variables ***
${FILE}     ${CURDIR}/input.txt

*** Tasks ***
Find Duplicates In Compartments Of Rucksacks And Sum Their Values
    Load Rucksacks From File            ${FILE}
    Split Rucksacks To Compartments And Find Duplicates
    Evaluate Duplicates And Sum Their Values
    Log Result

Find Duplicates In Triplet Groups of Rucksacks And Sum Their Values
    Load Rucksacks From File            ${FILE}
    Group Rucksacks To Triplets And Find Duplicates
    Evaluate Duplicates And Sum Their Values
    Log Result
