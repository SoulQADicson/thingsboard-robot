# thingsboard-robot

Laboratório de automação do ThingsBoard Community Edition com Robot Framework.
Objetivo: construir cobertura de interface, API e integração, rastreável aos
requisitos e, futuramente, executada por GitHub Actions.

## Estado atual

CT01, CT02 e CT03 de autenticação UI estão implementados e passaram na execução
local com Robot Framework e Browser Library. Ainda não há testes de API ou
integração. O workflow de CI passou também na primeira execução no GitHub em
Linux, com três testes aprovados. Consulte as [evidências remotas](docs/ci-first-run.md).
A configuração
Docker do laboratório foi instalada e iniciada localmente. Consulte as
[evidências de execução](docs/lab-execution.md) para resultados e limitações.
O arquivo `AGENTS.md` contém as diretrizes de trabalho e deve ser lido antes de
alterações. Cada próxima etapa depende da validação do responsável pelo projeto.

A etapa 2 está documentada em [Ambiente de execução](docs/environment.md), com
comandos, resultados observados e limitações. Para repetir a verificação local:

```powershell
.\.venv\Scripts\python.exe infrastructure/check_environment.py --browser
```

A etapa 3 está em [Laboratório ThingsBoard](docs/thingsboard-lab.md): arquitetura
Docker, instalação guiada, critérios de prontidão e investigação de falhas.

A etapa 4 define [requisitos e cenários de autenticação](docs/authentication-requirements.md)
e a [matriz de rastreabilidade](docs/traceability.md). O desenho inicial foi validado.
A etapa 5 implementa login válido, senha incorreta e acesso direto sem sessão:
veja [execução de autenticação](docs/authentication-execution.md) para configuração,
comandos, resultado real, explicação dos Resources e leitura dos relatórios.

A etapa 7 prepara o [CI de autenticação](docs/ci-authentication.md), com laboratório
temporário e publicação de relatórios como artefatos. Consulte o guia para o
Secret necessário, verificações realizadas e limites da validação local.

## Estrutura e responsabilidades

```text
thingsboard-robot/
├── AGENTS.md
├── tests/
│   ├── ui/
│   ├── api/
│   └── integration/
├── resources/
│   ├── pages/
│   └── api/
├── libraries/
├── variables/
├── data/
├── infrastructure/
├── docs/
│   └── traceability.md
├── .github/
│   └── workflows/
├── requirements.txt
├── .gitignore
└── README.md
```

| Diretório | Responsabilidade |
| --- | --- |
| `tests/ui` | Casos que verificam comportamento pela interface com Browser Library/Playwright. |
| `tests/api` | Casos que verificam contratos e comportamento HTTP com RequestsLibrary. |
| `tests/integration` | Casos que verificam fluxos entre componentes, como API e persistência, conforme os requisitos. |
| `resources` | Resources Robot compartilhados; poderão centralizar preparação, limpeza e keywords comuns. |
| `resources/pages` | Keywords de interação com páginas e seus seletores, após inspeção da aplicação. |
| `resources/api` | Keywords reutilizáveis de sessão HTTP, autenticação e chamadas de API. |
| `libraries` | Bibliotecas Python próprias para necessidades não atendidas pelas bibliotecas existentes. |
| `variables` | Configurações por ambiente, sem credenciais versionadas. Segredos virão do ambiente ou do CI. |
| `data` | Dados e fixtures de teste, sem segredos ou dados pessoais reais. |
| `infrastructure` | Futura configuração de ThingsBoard, PostgreSQL e Docker para o laboratório. |
| `docs` | Decisões de arquitetura, requisitos e matriz de rastreabilidade. |
| `.github/workflows` | Futuros pipelines de execução e publicação de relatórios. |

Diretórios sem conteúdo usam `.gitkeep`: é uma convenção para que o Git consiga
versionar sua presença. Esses arquivos não executam nenhuma ação.

## Arquitetura prevista

Os casos em `tests` expressarão cenários e resultados esperados. Importarão
keywords de `resources`, que usarão Browser Library, RequestsLibrary ou extensões
Python em `libraries`. Configurações ficarão em `variables` e massas em `data`.
Evitar duplicar seletores e chamadas HTTP nos casos de teste.

Setup e teardown serão definidos quando houver recursos concretos a preparar e
liberar. Tags identificarão camada, requisito e finalidade de execução; assertions
verificarão resultados observáveis. A matriz em `docs/traceability.md` ligará
requisitos, casos e evidências, sem declarar cobertura antes da implementação.

## Dependências

O `requirements.txt` registra as versões diretas observadas na `.venv` existente:

- Robot Framework: execução das suítes e relatórios.
- Browser Library: automação de interface baseada em Playwright.
- RequestsLibrary: testes de API HTTP.
- Psycopg com binários: futura integração Python com PostgreSQL.

Essas versões não foram instaladas nesta etapa. As importações e a inicialização
local do Chromium foram verificadas; a integração com ThingsBoard ainda não.
O arquivo não fixa todas as dependências transitivas. Node.js e a preparação dos
navegadores da Browser Library serão verificados na etapa de interface. Docker
CLI instalado não comprova que o daemon esteja funcionando.

## Como verificar esta etapa

Na raiz do projeto, em PowerShell:

```powershell
Get-Content -Encoding UTF8 README.md
tree tests /F
tree resources /F
tree .github /F
Get-ChildItem libraries, variables, data, infrastructure, docs -Force -Recurse
Get-Content requirements.txt
git status --short --untracked-files=all
git check-ignore .venv/
.\.venv\Scripts\python.exe -m pip check
```

O status deve mostrar os novos arquivos como não rastreados e omitir `.venv`.
`pip check` verifica a consistência dos pacotes instalados, mas não comprova
funcionamento dos testes ou compatibilidade com ThingsBoard.

Para executar a suíte atual, configure TB_USERNAME e TB_PASSWORD no ambiente
conforme o guia `docs/authentication-execution.md` e execute:

```powershell
.\.venv\Scripts\python.exe -m robot --outputdir results/authentication tests/ui/authentication.robot
```

Para uma futura instalação, depois da revisão das dependências, o comando será:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Esse comando não foi executado na criação da estrutura.

## Como investigar falhas

- Caminho não encontrado: confirme a raiz com `Get-Location` e confira os nomes com `Get-ChildItem -Force`.
- Acentos incorretos no terminal: leia os arquivos com `Get-Content -Encoding UTF8`.
- `.venv` aparecendo no status: confira `.gitignore` e `git check-ignore -v .venv/`.
- Conflito de dependências: confira o interpretador com `.\.venv\Scripts\python.exe --version` e examine a saída de `pip check`.
- Falha no Docker: registre a mensagem exata; verifique permissões da configuração e disponibilidade do daemon na etapa de infraestrutura.

## Git e próximas etapas

O fluxo previsto usa `main`, `develop` e `feature/*`. A preparação está em
[Git Flow](docs/git-flow.md), incluindo o escopo do primeiro commit local.
O bootstrap autorizado foi registrado em `69b89f9`, e develop foi criada a partir
dele. O pipeline está em `feature/ci-authentication`, publicado no remoto origin
com as branches main e develop. Nenhum merge foi realizado.

Repositório público: [SoulQADicson/thingsboard-robot](https://github.com/SoulQADicson/thingsboard-robot).
Revisão de privacidade e credenciais em [Publicação segura](docs/publication-security.md).

## Atividade de revisão

Execute os comandos de inspeção e explique onde colocaria: um cenário de login,
uma keyword de autenticação HTTP, uma URL de ambiente e uma massa de dispositivos.
Depois revise a matriz de rastreabilidade, sem preencher resultados fictícios.

Perguntas para discussão:

1. Qual critério separa um teste de API de um teste de integração que também usa HTTP?
2. Como garantir que o teardown libere recursos mesmo quando uma assertion falha?
3. Por que fixar apenas dependências diretas não garante reprodução completa no CI?

Aguardar validação desta etapa antes de implementar automação.
