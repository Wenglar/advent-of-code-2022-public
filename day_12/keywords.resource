*** Settings ***
Library         ExplorationLibrary.py

*** Variables ***
${start}        start
${end}          end

*** Keywords ***
Prepare File
    [Arguments]             ${file_path}
    Set File And Validate   ${file_path}

Initialize Map
    Load File

Set Start To Default Start
    Set Start       start

Set Start To Default End
    Set Start       end

Find The Shortest Path To The Highest Point
    ${path_len} =       Get The Shortest Path To Z

    Set Task Variable   ${path_len}

Find The Shortest Path To The Bottom
    ${path_len} =       Get The Shortest Path Down

    Set Task Variable   ${path_len}

Log Result
    Log     \n\tThe shortest path is: "${path_len}"     console=True
