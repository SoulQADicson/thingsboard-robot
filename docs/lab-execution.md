# Execução do laboratório — 25/10/2026

## O que foi feito e por quê

O agente executou a configuração e instalação, conforme a orientação atualizada
em `AGENTS.md`. As atividades do usuário passam a ser de revisão e aprendizado.

1. Criou `infrastructure/.env` com senha aleatória para PostgreSQL, sem imprimi-la.
   O arquivo é ignorado pelo Git; o modelo versionável continua sendo `.env.example`.
2. Validou o Compose e confirmou ausência de containers deste projeto.
3. Baixou `postgres:18` e `thingsboard/tb-node:4.3.1.7`.
4. Criou rede, volume e banco, e executou o instalador com dados de demonstração.
5. Iniciou a aplicação e verificou HTTP, renderização da tela e acesso de tenant.

## Comandos utilizados

Na raiz do projeto, todos os comandos Compose usaram o mesmo arquivo e ambiente:

```powershell
docker compose --env-file infrastructure/.env -f infrastructure/compose.yaml config --quiet
docker compose --env-file infrastructure/.env -f infrastructure/compose.yaml ps --all
docker compose --env-file infrastructure/.env -f infrastructure/compose.yaml pull
docker compose --env-file infrastructure/.env -f infrastructure/compose.yaml run --rm -e INSTALL_TB=true -e LOAD_DEMO=true thingsboard-ce
docker compose --env-file infrastructure/.env -f infrastructure/compose.yaml up -d
docker compose --env-file infrastructure/.env -f infrastructure/compose.yaml logs --tail 60 thingsboard-ce
```

Não repita o comando de instalação em banco já inicializado.

## Evidências observadas

| Verificação | Resultado |
| --- | --- |
| Instalador | `Installation finished successfully!`; código 0 |
| PostgreSQL | Container ativo e healthy |
| ThingsBoard | Container ativo nas consultas antes e depois da inspeção |
| Inicialização | Log `Started ThingsBoard in 63 seconds` |
| HTTP na raiz | Status 200 |
| Chromium | Página de login renderizada |
| Login de demonstração | URL `/home`; interface identificou `tenant@thingsboard.org` como administrador do tenant |

O endereço local é `http://127.0.0.1:8080`. Banco não publicado no host.
Os serviços foram deixados em execução. Dados persistem no volume
`thingsboard-robot_postgres-data`.

As capturas `reports/thingsboard-login.png` e `reports/thingsboard-tenant.png`
foram geradas pela inspeção temporária `reports/inspect_lab.py`. Essa pasta é
ignorada pelo Git. A inspeção não é uma suíte Robot nem estabelece cobertura de
requisitos. A senha de demonstração foi fornecida por variável de ambiente
temporária, removida ao término do comando.

## Falhas encontradas e interpretação

- Docker no sandbox: acesso negado ao pipe; comandos fora do sandbox passaram.
- HTTP antes do fim da inicialização: conexão encerrada. As consultas seguintes
  receberam 200; não houve reinstalação como tentativa de correção.
- Inspeção com seletor `input`: encontrou dois elementos e falhou em strict mode.
  O DOM revelou `#username-input` e `#password-input`; usar o primeiro para aguardar
  a tela resolveu a falha. Era erro da inspeção, não defeito do produto.
- Avisos Java sobre APIs depreciadas/restritas: registrados durante a instalação;
  não impediram sua conclusão. Não houve alteração de parâmetros Java.
- Capturas com caminho relativo não ficaram na pasta esperada; a inspeção passou
  a informar caminho absoluto. A saída de texto também precisou de UTF-8 para
  imprimir o símbolo de infinito da interface no terminal Windows. Após os ajustes,
  a inspeção completa terminou com código zero e as capturas foram salvas em reports.

Para problemas posteriores, consulte primeiro `ps --all` e logs do serviço afetado.
Não execute novamente o instalador nem remova volumes como primeira tentativa.
O procedimento completo de operação está em [Laboratório](thingsboard-lab.md).

## Revisão e limite desta etapa

Nenhum commit, push ou merge foi feito. Ainda não há suíte funcional implementada.
Aguarda-se validação antes de definir requisitos e automatizar autenticação.

Atividade de aprendizado: revise a tabela e identifique qual evidência comprova
processo ativo, qual comprova resposta HTTP e qual comprova acesso pela interface.

Perguntas:

1. Por que HTTP 200 na raiz não comprova que a autenticação funciona?
2. Por que um seletor ambíguo deve ser investigado antes de registrar um defeito?
3. Como controlar o estado persistido para executar uma suíte repetidamente?
