*** Settings ***
Library    RSPLibrary.py

*** Variables ***
${result}

*** Keywords ***
Load Events From File
    [Arguments]         ${file_path}
    Load File           ${file_path}

Execute Part 1 Strategy
    # Commented out and replaced for performance reasons

    # @{events} =         Get Events

    # FOR     ${event}    IN      @{events}
    #     ${points} =     Get Points  ${event['enemy']}   ${event['me']}
    #     ${result} =     Evaluate    ${result}+${points}
    # END

    # Set Test Variable   ${result}

    ${result} =     Calculate Points From Events And Sum Them

    Set Test Variable   ${result}


Execute Part 2 Strategy
    # Commented out and replaced for performance reasons

    # @{events} =         Get Events

    # FOR     ${event}    IN      @{events}
    #     ${event_me} =   Get Strategic Event     ${event['enemy']}   ${event['me']}
    #     ${points} =     Get Points              ${event['enemy']}   ${event_me}
    #     ${result} =     Evaluate                ${result}+${points}
    # END

    # Set Test Variable   ${result}

    Evaluate Actions Based On Strategy
    ${result} =     Calculate Points From Events And Sum Them

    Set Test Variable   ${result}

Log Result
    Log                 \n\tTotal score is: "${result}"     console=True
