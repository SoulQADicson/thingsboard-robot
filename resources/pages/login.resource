*** Settings ***
Resource    ../browser.resource

*** Variables ***
${LOGIN_USERNAME}       css=#username-input
${LOGIN_PASSWORD}       css=#password-input
${LOGIN_SUBMIT}         css=button[type="submit"]
${LOGIN_ERROR}          css=.error-toast .toast-text
${LOGIN_ERROR_TEXT}     Invalid username or password

*** Keywords ***
Abrir Pagina De Login
    Go To    ${BASE_URL}/login
    Login Deve Estar Visivel

Login Deve Estar Visivel
    Get Url    ==    ${BASE_URL}/login
    Wait For Elements State    ${LOGIN_USERNAME}    visible
    Wait For Elements State    ${LOGIN_PASSWORD}    visible
    Wait For Elements State    ${LOGIN_SUBMIT}    enabled

Entrar Com Credenciais
    [Arguments]    ${usuario}    ${senha}
    Fill Text    ${LOGIN_USERNAME}    ${usuario}
    Fill Secret    ${LOGIN_PASSWORD}    ${senha}
    Click    ${LOGIN_SUBMIT}

Login Deve Ser Rejeitado
    Get Text    ${LOGIN_ERROR}    ==    ${LOGIN_ERROR_TEXT}
    Login Deve Estar Visivel
