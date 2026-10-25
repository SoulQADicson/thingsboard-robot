# Etapa 7 — CI de autenticação com GitHub Actions

Atualização: publicação autorizada concluída, com origin configurado e primeiro
job Linux aprovado (CT01–CT03). TB_PASSWORD foi configurado como Secret.
Consulte [Primeira execução](ci-first-run.md) para o resultado remoto. As seções
de preparação e evidências locais abaixo registram o estado anterior à publicação.

## Objetivo e arquivos

Executar CT01–CT03 em uma máquina de CI preparada explicitamente, com laboratório
ThingsBoard próprio, e preservar evidências. Esta etapa prepara integração
contínua; não implementa deploy contínuo de uma aplicação.

- `.github/workflows/authentication.yml`: eventos, runner e sequência do job.
- `infrastructure/wait_for_http.py`: espera limitada por HTTP 200, reutilizável
  localmente e no runner, usando apenas a biblioteca padrão Python.
- `docs/git-flow.md` e README: situação atual das branches e orientação de uso.

Branch atual: `feature/ci-authentication`, criada de `develop`. O commit baseline
`69b89f9` é a baseline comum a main/develop/feature; alterações desta etapa ainda não
foram commitadas, enviadas ou integradas.

## Como o workflow funciona

1. Eventos: push em main, develop ou feature/**; pull request destinado a main ou
   develop; workflow_dispatch para execução manual.
2. Runner `ubuntu-24.04`, com limite de 30 minutos. Configura Python 3.12 e Node 24.
3. Verifica a presença de TB_PASSWORD e gera senha aleatória de PostgreSQL. O
   valor é mascarado e enviado via GITHUB_ENV aos passos seguintes, sem arquivo
   .env versionado e sem alterar seu laboratório Windows.
4. Instala requirements, executa pip check e `rfbrowser init --with-deps chromium`.
   O preflight confirma importações e inicialização do navegador.
5. Usa o mesmo Compose, com nome de projeto específico de run e tentativa.
   Baixa imagens, inicializa banco novo com demonstração e inicia ThingsBoard.
6. Aguarda HTTP 200 na raiz por até 240s; falha com código 1 se o prazo expirar.
   Isso é uma condição de entrada, não prova de autenticação. As assertions da
   suíte verificam identidade e acesso protegido.
7. Executa a suíte com tag regression (atualmente CT01–CT03), Chromium headless,
   contexto en-US e timeout de UI de 30s.
8. Com `if: always()`, tenta coletar estado/logs dos containers, publicar a pasta
   results e parar o laboratório, inclusive após falha. Falha anterior permanece
   falha; não usamos continue-on-error para ocultá-la.

Always não garante execução após encerramento forçado do runner. Se o banco nem
foi preparado, o diagnóstico registra isso e a limpeza não tenta iniciá-lo.
O runner hospedado é temporário; seu volume não é o volume do laboratório local.

Permissão do token: contents: read. Checkout não persiste credenciais. Concorrência
por workflow/ref cancela execução anterior da mesma ref, evitando trabalho duplicado.
Push e PR de uma feature podem criar duas execuções distintas nesta configuração.

## Configuração necessária no GitHub

Ainda não existe remoto configurado. Para ativar será necessário, em etapa
autorizada, definir/criar o repositório, publicar as branches e configurar:

Repository → Settings → Secrets and variables → Actions → New repository secret:

| Nome | Conteúdo |
| --- | --- |
| TB_PASSWORD | Senha do administrador de tenant criado pelos dados de demonstração. |

TB_USERNAME está configurado como tenant@thingsboard.org no workflow. TB_PASSWORD
não redefine a senha no ThingsBoard: deve corresponder à conta da demonstração
descrita no guia do laboratório. Não usar senha de produção. A senha do banco é
separada, gerada a cada job. Não é necessário versionar ou enviar .env local.

PR de fork não recebe esse Secret; nesta configuração falhará explicitamente na
validação de credenciais, sem iniciar o laboratório. Não foi usado pull_request_target
para contornar a restrição. A primeira versão é voltada a branches do laboratório.

O botão manual normalmente só fica disponível quando o workflow está na branch
padrão; antes disso, a publicação da feature acionará o evento push previsto.
Nada foi publicado nesta etapa.

## Resultados e artefatos

No GitHub: Actions → Authentication UI → execução → job authentication para os
logs dos passos. Na seção Artifacts, baixar o ZIP `authentication-<run>-<attempt>`
e extrair a pasta inteira. Abrir authentication/report.html para o resumo e
authentication/log.html para keywords, assertions e capturas. Em infrastructure,
containers.txt e compose.log ajudam a diagnosticar a inicialização.

Retenção configurada: 7 dias, sujeita aos limites do repositório. Esses artefatos
não são um site público de relatórios nem commits do Git. Não é necessário
adicionar permissões de escrita ao conteúdo para publicá-los como artefatos.

## Comandos locais de revisão

```powershell
git status --short --branch
git diff --check
.\.venv\Scripts\python.exe infrastructure/wait_for_http.py --url http://127.0.0.1:8080 --timeout 10
```

Para repetir a suíte, preparar TB_USERNAME e TB_PASSWORD no ambiente conforme
`authentication-execution.md` e executar:

```powershell
.\.venv\Scripts\python.exe -m robot --include regression --outputdir results/ci-local tests/ui/authentication.robot
```

O actionlint foi baixado da release oficial, com checksum SHA256 conferido,
somente para reports/tools/actionlint (ignorado pelo Git). Comando utilizado:

```powershell
.\reports\tools\actionlint\actionlint.exe -shellcheck= -pyflakes= .github/workflows/authentication.yml
```

ShellCheck/Pyflakes não foram executados por esse comando; a sintaxe dos sete
blocos run foi verificada separadamente com `bash -n` do Git Bash. Parsing YAML
também foi feito com PyYAML já instalado, usando BaseLoader para preservar `on`.

## Evidências reais de 25/10/2026

| Verificação | Resultado |
| --- | --- |
| actionlint 1.7.11 | Código 0, sem diagnósticos |
| YAML | Parse passou; 3 eventos e 11 passos |
| Bash | Sintaxe dos 7 blocos run passou |
| Python | AST do helper HTTP válido |
| HTTP do laboratório existente | Status 200, helper código 0 |
| Helper com servidor controlado | 200: código 0; 503→200: código 0; 503 contínuo: código 1; timeout inválido: código 2 |
| Regressão local Windows | CT01 PASS, CT02 PASS, CT03 PASS; código 0 |
| Execução no GitHub/instalação limpa Linux | Não realizada; projeto sem remoto |

Resultados da regressão: `results/ci-local/output.xml`, report.html e log.html.
O helper foi exercitado por `reports/verify_readiness.py`, temporário e ignorado.
Não foram recriados ou apagados dados do laboratório local.

Validação estática e regressão Windows não comprovam instalação limpa Linux,
funcionamento dos serviços no runner ou upload. A primeira execução remota será
necessária para confirmar esses pontos. Dependências transitivas, patches de
Python/Node/PostgreSQL não estão congelados por hash; esta
preparação ainda não é uma garantia de reprodução bit a bit. As Actions externas
foram fixadas por SHA na revisão de publicação, descrita em `publication-security.md`.

## Investigar falhas

- Credencial ausente: revisar nome e disponibilidade do Secret para aquele evento.
- Instalação Python/Chromium: consultar o passo de instalação e dependências de OS.
- Instalador: examinar exit code e compose.log; não repetir instalação sobre um
  banco local persistente como tentativa de correção.
- Timeout HTTP: confirmar container ativo e logs; não confundir com falha de login.
- Robot: abrir a primeira keyword que falhou no log.html e comparar esperado/obtido.
- Artifact só com diagnóstico: falha ocorreu antes da suíte, portanto report.html
  pode não existir. Logs do job continuam sendo a fonte principal desse erro.

## Fontes oficiais consultadas

- [Browser Library: instalação](https://robotframework-browser.org/docs/start/installation/)
- [Actions: checkout v4](https://github.com/actions/checkout/tree/v4)
- [Actions: setup-python v5](https://github.com/actions/setup-python/tree/v5)
- [Actions: setup-node v4](https://github.com/actions/setup-node/tree/v4)
- [Actions: upload-artifact v4](https://github.com/actions/upload-artifact/tree/v4)
- [actionlint: instalação](https://github.com/rhysd/actionlint/blob/main/docs/install.md)

## Atividade e perguntas

Revise a ordem dos passos e localize quais ainda são tentados após falha. A
implementação e as verificações locais já foram executadas pelo agente.

1. Por que HTTP 200 é condição de prontidão, mas não substitui CT01?
2. Por que upload com always() não transforma um teste reprovado em aprovado?
3. O que a execução Linux ainda precisa demonstrar além do PASS local Windows?

Aguardar validação antes de commit, publicação no GitHub ou integração das branches.
