# Revisão para publicação pública

## Escopo

Portfólio educacional ThingsBoard, Robot Framework e Playwright com dados
fictícios. Publicação pública autorizada pelo responsável, sem merge entre branches.
Credenciais reais, relatórios locais e ferramentas temporárias não fazem parte
do conteúdo versionado.

## Controles aplicados

- Contexto profissional no AGENTS generalizado para laboratório educacional.
- Baseline local ainda não publicada recriada com email GitHub noreply. O email
  pessoal não fica nos metadados dos commits que serão enviados. Uma cópia de
  recuperação foi preservada localmente sob reports, ignorada pelo Git; não
  publicar bundles, reflogs ou usar push --mirror.
- Senhas de testes recebidas por ambiente e tratadas como Secret; banco local
  configurado por .env ignorado. .env.example contém apenas placeholder.
- Revisão dos caminhos candidatos: .venv, .env real, results e reports excluídos.
- Gitleaks executado com saída redigida sobre os arquivos candidatos e sobre o
  histórico alcançável pelas branches públicas; resultados ficam apenas em reports.
- Actions externas fixadas por SHA consultado nos repositórios oficiais, com
  indicação da versão principal. Token com contents: read e checkout sem persistir
  credenciais. Não usar pull_request_target para executar código de terceiros.
- Secret de login do CI configurado como repository secret, não como arquivo
  nem argumento literal no shell. A conta é a de demonstração no banco efêmero.

O email noreply preserva atribuição ao perfil GitHub. O nome público do perfil,
IDs de commit e documentação técnica continuam públicos. Logs e artefatos do CI
devem conter apenas dados fictícios do laboratório; revisar antes de compartilhar
capturas ou introduzir novos ambientes. Gitleaks não garante ausência de todo tipo
de dado sensível ou vulnerabilidade.

## Estado e evidências

As verificações de arquivos e baseline `69b89f9` passaram sem achados de credenciais.
Publicação pública concluída, com secret scanning e push protection habilitados.
A primeira execução Linux passou, e os artefatos baixados também passaram na
varredura. Detalhes e links em [Primeira execução](ci-first-run.md).
Se a CLI solicitar autenticação, o responsável autoriza pelo fluxo oficial do
GitHub; nunca enviar senha ou token por chat.

Depois da criação, conferir visibilidade pública, branches enviadas, email
noreply dos commits e proteção de segredos disponível no repositório. Não fazer
force push nem sobrescrever repositório preexistente como parte desta publicação.
