# Etapa 2 — ambiente de execução

## Objetivo e arquitetura

Validar o executor antes de configurar o sistema sob teste. O script
`infrastructure/check_environment.py` usa a biblioteca padrão do Python para ler
os pins de `requirements.txt`, consultar versões e importar as bibliotecas.
Com `--browser`, usa a Browser Library para iniciar Chromium sem janela e
encerrá-lo. Retorna código 0 em sucesso e 1 quando detecta falhas.

Não instala pacotes, não acessa ThingsBoard e não altera dados de aplicação.
O script assume o formato atual de requirements: dependências diretas com `==`.
Não é um teste funcional nem substitui o `pip check` das dependências transitivas.

## Executar no PowerShell

Na raiz do repositório, use explicitamente o Python do ambiente virtual:

```powershell
.\.venv\Scripts\python.exe infrastructure/check_environment.py
.\.venv\Scripts\python.exe infrastructure/check_environment.py --browser
.\.venv\Scripts\python.exe -m pip check
docker info --format '{{.ServerVersion}}'
```

Para consultar a CLI da Browser Library:

```powershell
.\.venv\Scripts\rfbrowser.exe --help
```

`python -m Browser` não é uma entrada válida nesta instalação; use `rfbrowser`.

## Evidências de 25/10/2026

| Verificação | Resultado observado |
| --- | --- |
| Python da .venv | 3.12.1 |
| Robot Framework | 7.5; CLI inicia |
| Browser Library | 20.6.0; importação passou |
| RequestsLibrary | 0.9.7; importação passou |
| Psycopg | 3.3.6; importação passou |
| Script com --browser | Código 0; Chromium headless iniciou e foi encerrado |
| pip check | No broken requirements found |
| Docker Engine | 29.9.2; consulta passou fora do sandbox |

A primeira consulta Docker no sandbox recebeu acesso negado à configuração e
ao pipe. A consulta autorizada fora do sandbox passou, portanto essa falha não
demonstrava indisponibilidade do serviço Docker.

O navegador foi iniciado localmente sem navegar para a aplicação. Não foram
verificadas conexão PostgreSQL, instalação ThingsBoard, autenticação ou cobertura
de requisitos. Não houve instalação ou atualização de dependências.

A .venv também contém BrowserBatteries 20.6.0, que não está declarada nas
dependências diretas. O sucesso local não comprova uma instalação limpa: a
preparação de dependências Node e navegadores deverá ser documentada e validada
ao configurar o executor reproduzível/CI.

## Investigar falhas

- Interpretador incorreto: confira a linha `Interpreter` impressa pelo script.
- Versão divergente ou importação falhando: compare a mensagem com requirements
  e execute `pip check` usando o mesmo Python. Não atualize tudo indiscriminadamente.
- Chromium não inicia: guarde a mensagem completa e consulte `rfbrowser --help`.
  A importação Python pode passar mesmo com dependências Node ou binários de
  navegador ausentes. Uma instalação limpa requer preparação específica.
- Docker com acesso negado: confira permissões e contexto de execução antes de
  concluir que o serviço está parado. Não exclua configuração ou volumes.
- Docker sem resposta: confira Docker Desktop e o contexto Docker ativo.

## Atividade individual e validação

Execute os quatro comandos de verificação. Anote códigos de saída com
`$LASTEXITCODE` imediatamente após cada comando e explique o que cada resultado
comprova. Não é necessário provocar uma falha ou alterar dependências.

Perguntas de revisão:

1. Por que importar Browser com sucesso não garante que Chromium inicie?
2. Por que um navegador local funcionando não garante um pipeline reproduzível?
3. Como distinguir falha do executor, falha de infraestrutura e defeito do produto?

A próxima etapa será definir o ambiente ThingsBoard (instância existente ou
laboratório Docker) e seus critérios de prontidão, após validação desta etapa.
