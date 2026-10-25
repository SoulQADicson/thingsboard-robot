# Etapa 6 — preparação do Git Flow

Atualização: bootstrap autorizado concluído em `69b89f9`; main e develop foram
criadas com essa baseline. A etapa 7 ocorre em feature/ci-authentication, derivada
de develop, ainda sem commit das alterações. Não houve push ou merge. As seções
abaixo preservam a análise e o plano da preparação inicial, já executado após
autorização. Consulte `ci-authentication.md` para a etapa atual.

## Objetivo e estado observado

Criar histórico rastreável do framework antes de implementar CI/CD. Em
25/10/2026, o agente verificou: repositório inicializado, HEAD em `main`, nenhum
commit, nenhum arquivo rastreado e nenhum remoto configurado. O comando
`git log -1 --oneline` respondeu que main ainda não possui commits; isso é
esperado neste estado, não uma perda de histórico.

Não foram criadas branches adicionais. Sem commit inicial, main ainda é uma
branch não materializada em uma referência de commit; criar develop a partir
dela requer primeiro um commit. Não criar históricos órfãos para contornar isso.

## Responsabilidades das branches

| Branch | Papel no laboratório |
| --- | --- |
| `main` | Baseline estável e revisada. Recebe o primeiro commit de bootstrap autorizado. |
| `develop` | Integração das próximas alterações, derivada da baseline inicial. |
| `feature/*` | Trabalho delimitado, criado a partir de develop; por exemplo, `feature/ci-authentication`. |

O bootstrap inicial registra o trabalho já existente; não é uma simulação de
desenvolvimento que ocorreu em branches feature. A partir dele, cada alteração
nova segue feature → develop → main, mediante revisão e autorização para merges.

Um commit registra um snapshot local. Uma branch é uma referência móvel a um
commit; criar develop após o bootstrap fará main e develop apontarem inicialmente
para o mesmo commit. Push publica no remoto e não é consequência automática de
commit. Nenhum remoto será configurado ou conteúdo publicado nesta etapa.

## Escopo concreto proposto para o primeiro commit

Mensagem: `chore: bootstrap ThingsBoard automation framework`.

| Conteúdo | Motivo para versionar |
| --- | --- |
| `AGENTS.md`, `.gitignore`, `README.md` | Diretrizes, exclusões e orientação de uso. |
| `requirements.txt` | Dependências diretas conhecidas. |
| `tests`, `resources`, `variables` | Suíte de autenticação, keywords e configuração sem senhas literais. |
| `infrastructure` | Compose, modelo .env.example e verificador de ambiente; sem .env real. |
| `docs` | Arquitetura, requisitos, matriz e evidências descritas das execuções. |
| `data`, `libraries`, `.github/workflows` | Placeholders das camadas ainda não implementadas. |

Não versionar `.venv`, `.env`, relatórios, capturas ou scripts temporários em
`reports`. A matriz registra referências a resultados locais; esses artefatos não
estarão disponíveis em um clone. A publicação automática ficará para o CI/CD.

Os três casos UI passaram na última execução registrada em
`authentication-execution.md`. Esta etapa só altera documentação, portanto não
declara nova execução nem precisa repetir a suíte. Ainda não existe workflow.

## Verificações de revisão executadas

```powershell
git status --short --branch
git branch --list
git log -1 --oneline
git remote -v
git ls-files
git ls-files --others --exclude-standard
git check-ignore .venv/ infrastructure/.env results/authentication/output.xml playwright-log.txt
```

`git ls-files` vazio confirma ausência de arquivos rastreados; a listagem com
`--others --exclude-standard` mostra candidatos, respeitando .gitignore. A
confirmação de arquivos ignorados não é uma auditoria universal de segredos.
Antes do commit, o agente revisará também o conteúdo exato do staging.

## Ações após autorização explícita

O agente fará staging dos caminhos revisados, conferirá `git diff --cached
--check`, `git diff --cached --stat` e o conteúdo staged, criará o commit local
em main e executará `git switch -c develop`. Se houver alteração inesperada,
interromperá antes de incluí-la. Não haverá push ou merge.

Depois verificará `git log --oneline --decorate --all`, `git branch --list` e
`git status`. As duas branches devem existir, apontar inicialmente para o mesmo
commit e o checkout deve estar em develop. Não afirmar essa condição antes de
executar as ações.

Uma feature será criada a partir de develop na etapa autorizada de CI/CD. Antes
disso, será necessário definir o repositório GitHub e a preparação reproduzível
do executor, incluindo ThingsBoard e navegadores.

## Investigar erros

- `not a valid object name: main`: confirme se o primeiro commit existe.
- Identidade ausente no commit: configurar nome/email com valores confirmados,
  preferindo escopo local; não inventar identidade nem alterar configuração global.
- Arquivo sensível no staging: retirar somente o caminho específico antes do
  commit e investigar a regra de ignore; não usar reset destrutivo.
- Arquivo inesperado: revisar conteúdo e origem antes de adicioná-lo.
- `git diff` vazio com arquivos untracked: é esperado; diff comum mostra alterações
  rastreadas, não o conteúdo de arquivos novos ainda fora do staging.

## Atividade de revisão e perguntas

Leia o escopo proposto e identifique o que estará disponível para quem clonar o
repositório e o que dependerá da preparação do ambiente. A execução Git cabe ao agente.

1. Por que git diff vazio não demonstra que o workspace está sem alterações?
2. Por que main e develop podem começar no mesmo commit, mas ter papéis distintos?
3. Por que um commit local não disponibiliza o framework para um runner do GitHub?

O `AGENTS.md` determina: “Não realize commits, pushes ou merges sem minha
autorização.” Por isso, o bootstrap aguarda autorização explícita. Este documento
e o escopo estão preparados para revisão antes desse pedido.
