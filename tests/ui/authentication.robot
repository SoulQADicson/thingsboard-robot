*** Settings ***
Documentation       Autenticacao UI: identidade, rejeicao e acesso sem sessao.
Resource            ../../resources/pages/authenticated.resource
Suite Setup         Iniciar Navegador
Suite Teardown      Encerrar Navegador
Test Setup          Criar Sessao Isolada
Test Teardown       Encerrar Sessao Isolada
Test Tags           ui    auth

*** Test Cases ***
CT01 - Login valido
    [Documentation]    UI-AUTH-001: confirma identidade e acesso ao recurso de dispositivos.
    [Tags]    CT01    UI-AUTH-001    AUTH-001    smoke    regression
    Abrir Pagina De Login
    Entrar Com Credenciais    ${USERNAME}    ${PASSWORD}
    Area Autenticada Deve Estar Disponivel
    Recurso Protegido Deve Estar Acessivel

CT02 - Senha incorreta
    [Documentation]    UI-AUTH-002: uma tentativa invalida, feedback e negacao de acesso.
    [Tags]    CT02    UI-AUTH-002    AUTH-002    regression    security    negative
    Abrir Pagina De Login
    Entrar Com Credenciais    ${USERNAME}    ${INVALID_PASSWORD}
    Login Deve Ser Rejeitado
    Abrir Rota Protegida Sem Sessao
    Acesso Protegido Deve Ser Negado

CT03 - Acesso direto a rota protegida sem sessao
    [Documentation]    UI-AUTH-006: contexto novo sem autenticar tenta acessar /home.
    [Tags]    CT03    UI-AUTH-006    AUTH-004    regression    security
    Abrir Rota Protegida Sem Sessao
    Acesso Protegido Deve Ser Negado
