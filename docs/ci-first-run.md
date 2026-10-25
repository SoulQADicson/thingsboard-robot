# Primeira execução pública do CI — 25/10/2026

Repositório público: [SoulQADicson/thingsboard-robot](https://github.com/SoulQADicson/thingsboard-robot).
Nenhum merge foi realizado: main/develop contêm a baseline `69b89f9` e o pipeline
está em feature/ci-authentication.

## Resultado verificado

[Execução 40232265170](https://github.com/SoulQADicson/thingsboard-robot/actions/runs/40232265170),
commit `f8e560e`, branch feature/ci-authentication: success.

| Caso | Resultado | Duração |
| --- | --- | --- |
| CT01 — Login válido | PASS | 6,15s |
| CT02 — Senha incorreta | PASS | 1,95s |
| CT03 — Acesso direto sem sessão | PASS | 1,20s |

Robot 7.5, Python 3.12.15 em Linux; suíte em 10,85s, sem contar preparação do job.
Instalação limpa de dependências/Chromium, inicialização do banco, espera HTTP,
testes, coleta, upload e encerramento do laboratório concluíram com sucesso.

Artefato `authentication-40232265170-1`, disponível na execução com retenção de
sete dias. Extrair o ZIP inteiro e abrir authentication/report.html ou log.html.
Resultados e diagnósticos foram baixados localmente em reports/github-first-run,
fora do versionamento. O output.xml confirmou os três PASS. Gitleaks sobre o
artefato baixado não detectou credenciais reconhecidas.

## Verificações de publicação

- Visibilidade PUBLIC e branch padrão main confirmadas pela API do GitHub.
- Main, develop e feature enviadas sem force push ou merge.
- Autor e committer das duas revisões publicadas usam GitHub noreply.
- TB_PASSWORD configurado como repository secret; valor não registrado aqui.
- Secret scanning e push protection habilitados; consulta retornou zero alertas.
- Arquivos candidatos e histórico publicável passaram na varredura Gitleaks.
- Backup anterior, .env real, ambiente virtual, relatórios e ferramentas locais
  permaneceram fora do repositório publicado.

Essas evidências reduzem os riscos revisados, sem garantir ausência de toda
vulnerabilidade. O histórico de preparação permanece nos demais guias; esta
página registra o resultado remoto efetivamente observado.

Para acompanhar novas execuções, use a aba Actions. Falhas na preparação devem
ser investigadas nos logs do passo e em infrastructure/compose.log; falhas de
assertion ficam detalhadas no log.html. Uma nova revisão pode gerar outra
execução, cujo resultado deve ser consultado separadamente.
