*** Settings ***
Variables   ../variables/environment.py
Library     Browser    timeout=${UI_TIMEOUT}    retry_assertions_for=${UI_TIMEOUT}

*** Keywords ***
Iniciar Navegador
    New Browser    ${BROWSER}    headless=${HEADLESS}

Criar Sessao Isolada
    New Context    locale=en-US    viewport={'width': 1440, 'height': 1000}
    New Page    about:blank

Encerrar Sessao Isolada
    TRY
        IF    '${TEST STATUS}' == 'FAIL'
            Run Keyword And Ignore Error    Take Screenshot    filename=failure-{index}
        END
    FINALLY
        Close Context
    END

Encerrar Navegador
    Close Browser    ALL
