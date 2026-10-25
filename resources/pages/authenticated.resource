*** Settings ***
Resource    login.resource

*** Variables ***
${USER_IDENTITY}       css=.tb-user-display-name
${DEVICES_TABLE}       css=table[role="table"]

*** Keywords ***
Identidade Autenticada Deve Ser
    [Arguments]    ${usuario}
    Get Text    ${USER_IDENTITY}    ==    ${usuario}
    Wait For Elements State    ${LOGIN_USERNAME}    detached

Area Autenticada Deve Estar Disponivel
    Get Url    ==    ${BASE_URL}/home
    Identidade Autenticada Deve Ser    ${USERNAME}

Recurso Protegido Deve Estar Acessivel
    Go To    ${BASE_URL}/entities/devices
    Get Url    ==    ${BASE_URL}/entities/devices
    Identidade Autenticada Deve Ser    ${USERNAME}
    Wait For Elements State    ${DEVICES_TABLE}    visible

Abrir Rota Protegida Sem Sessao
    Go To    ${BASE_URL}/home

Acesso Protegido Deve Ser Negado
    Login Deve Estar Visivel
    Wait For Elements State    ${USER_IDENTITY}    detached
    Wait For Elements State    ${DEVICES_TABLE}    detached
