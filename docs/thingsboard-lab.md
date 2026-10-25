# Etapa 3 — preparação do laboratório ThingsBoard

## Arquitetura

O executor Robot rodará no Windows. A aplicação e seu banco rodarão em containers
Linux no Docker Desktop. O Compose agrupa os recursos sob `thingsboard-robot`.

```text
Robot / navegador no Windows
          |
    127.0.0.1:8080
          |
     thingsboard-ce ---- postgres:5432 ---- volume postgres-data
```

O hostname `postgres` existe na rede interna do Compose, não no Windows.
O banco não publica porta no host. Para a futura integração Python com banco,
será necessário definir o acesso explicitamente na etapa correspondente.
Somente HTTP está publicado; MQTT e outros protocolos poderão ser acrescentados
quando um requisito os exigir. O volume mantém o banco após recriar containers.

Base técnica consultada em 25/10/2026:
[instalação oficial CE para Windows](https://thingsboard.io/docs/installation/docker-windows/).
Usamos o modelo de fila em memória, ThingsBoard 4.3.1.7 e PostgreSQL 18.
O guia oficial informa mínimo de 4 GB de RAM para desenvolvimento/PoC.
A tag PostgreSQL fixa a versão principal, mas ainda permite alterações de patch;
não há garantia de imagens imutáveis até registrar seus digests.

## Arquivos e dependências

- `infrastructure/compose.yaml`: serviços, rede implícita, volume e verificação do banco.
- `infrastructure/.env.example`: nomes das configurações; não contém senha real.
- `infrastructure/.env`: cópia local ignorada pelo Git, criada pelo responsável.

É necessário Docker Desktop com containers Linux, Compose e acesso à internet
para baixar imagens. A senha do banco será lida pelo Compose e passada aos dois
serviços. Não use credenciais de outros ambientes neste laboratório.

## Procedimento de instalação executado pelo agente

O agente executa os comandos na raiz do repositório, um por vez. Confira `$LASTEXITCODE`
após cada comando Docker; interrompa a sequência se for diferente de zero.

1. Prepare a configuração local. Copie apenas se `.env` ainda não existir:

```powershell
if (-not (Test-Path infrastructure/.env)) {
    Copy-Item infrastructure/.env.example infrastructure/.env
}
notepad infrastructure/.env
```

Substitua a senha de exemplo. Se 8080 estiver ocupada, altere `TB_HTTP_PORT`.

2. Valide e baixe as imagens:

```powershell
docker compose --env-file infrastructure/.env -f infrastructure/compose.yaml config --quiet
docker compose --env-file infrastructure/.env -f infrastructure/compose.yaml pull
```

3. Somente na primeira instalação, inicialize o banco com os dados de demonstração:

```powershell
docker compose --env-file infrastructure/.env -f infrastructure/compose.yaml run --rm -e INSTALL_TB=true -e LOAD_DEMO=true thingsboard-ce
```

O serviço PostgreSQL será iniciado como dependência. Aguarde o instalador terminar
com código zero antes de subir a aplicação. Não repita a inicialização em banco
já instalado; em caso de erro, preserve os logs para investigar.

4. Inicie e inspecione:

```powershell
docker compose --env-file infrastructure/.env -f infrastructure/compose.yaml up -d
docker compose --env-file infrastructure/.env -f infrastructure/compose.yaml ps
docker compose --env-file infrastructure/.env -f infrastructure/compose.yaml logs --tail 100 thingsboard-ce
```

Abra `http://localhost:8080` (ou a porta configurada) no navegador. A instalação
com demonstração disponibiliza o administrador de tenant `tenant@thingsboard.org`
com senha `tenant`, conforme o guia oficial. Credenciais de demonstração servem
somente ao laboratório local. Não coloque senhas em casos de teste ou relatórios.

## Critérios de prontidão

- Instalação do banco concluída com código zero.
- PostgreSQL aparece como healthy.
- ThingsBoard permanece em execução sem reinícios recorrentes.
- Página de login visível e login manual de tenant concluído.

`running` indica processo ativo; não comprova prontidão da aplicação. O healthcheck
do banco verifica aceitação de conexões, não a instalação do schema ThingsBoard.
Nesta etapa, a verificação da aplicação é manual e não declara cobertura automatizada.

## Investigar e parar

- Variável ausente: confira o arquivo local e o argumento `--env-file`.
- Falha no pull: registre a mensagem e verifique rede, registry e espaço em disco.
- Porta ocupada: altere `TB_HTTP_PORT` e use a mesma porta no navegador.
- Banco unhealthy: consulte `logs --tail 100 postgres` com os mesmos argumentos Compose.
- Aplicação reiniciando: examine logs do ThingsBoard e o resultado do instalador.
- Senha alterada após criar o volume: a variável de inicialização do PostgreSQL não
  altera automaticamente a senha do banco existente. Não apague o volume como correção.

Para encerrar os containers preservando o banco:

```powershell
docker compose --env-file infrastructure/.env -f infrastructure/compose.yaml down
```

Não acrescente `--volumes`: isso removeria os dados persistidos do laboratório.

## Evidências e revisão

O Compose foi validado estaticamente usando `.env.example`, com `config --quiet`.
O agente está executando a instalação; os resultados efetivos ficam registrados
em `docs/lab-execution.md`. O procedimento acima também serve como referência
para compreender e reproduzir os comandos, sem exigir implementação pelo usuário.

Como atividade de aprendizado, revise as evidências registradas, sem executar
novamente a instalação ou compartilhar senhas.
Discuta:

1. Por que o banco saudável não prova que ThingsBoard está pronto?
2. O que persiste ao executar `down`, e por que isso afeta a repetibilidade dos testes?
3. Como separar dados de demonstração dos dados criados por futuras suítes?

A próxima etapa, após validar este laboratório, será definir requisitos e cenários
de autenticação e inspecionar a aplicação antes de escrever keywords e testes.
