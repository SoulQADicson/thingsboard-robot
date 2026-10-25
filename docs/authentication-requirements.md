# Etapa 4 — autenticação: requisitos e cenários

## Objetivo

Definir o primeiro incremento de automação do ThingsBoard CE 4.3.1.7 local.
O desenho inicial foi validado pelo responsável antes da implementação;
não são uma especificação oficial do produto. Observar o sistema não substitui
a decisão sobre o comportamento esperado. CT01, CT02 e CT03 estão implementados;
consulte [Execução](authentication-execution.md) para resultados. O restante deste
documento registra o desenho inicial e os cenários futuros.

## Análise observada em 25/10/2026

Containers permanecem ativos e PostgreSQL healthy. Inspeção em Chromium com
contexto novo, sem envio de tentativas inválidas, confirmou:

- A raiz redireciona para `/login`.
- Campos reais: `#username-input` (email) e `#password-input` (password).
- `button[type=submit]` permanece habilitado com campos vazios.
- Email `email-invalido` seguido de retirada de foco exibe `Formato de email inválido.`.
- HTML: email required=true e senha required=false. Isso não prova que o backend
  aceite senha vazia. Ambos têm maxLength=-1; limites de backend não investigados.
- A inspeção anterior confirmou `/home` e identidade de administrador de tenant
  após login válido, conforme `lab-execution.md`.

Inspeção temporária `reports/discover_auth.py` concluída com código zero, ignorada
pelo Git. Não conta como caso automatizado aprovado. Textos variam por idioma.

## Requisitos propostos e risco

| ID | Critério de aceitação | Prioridade |
| --- | --- | --- |
| AUTH-001 | Credenciais válidas permitem entrar e ver a identidade correta do tenant. | Alta |
| AUTH-002 | Senha incorreta não cria sessão nem permite acesso protegido; há feedback. | Alta |
| AUTH-003 | Dados ausentes ou email malformado não autenticam; há feedback na interface. | Média |
| AUTH-004 | Contexto novo sem sessão não acessa área protegida pela URL direta. | Alta |
| AUTH-005 | Logout encerra acesso no navegador; recarregar área protegida não restaura acesso. | Alta |
| AUTH-006 | API autentica credenciais válidas e rejeita senha incorreta; recurso protegido rejeita ausência de credencial. | Alta |

Prioridade alta considera acesso indevido e indisponibilidade do fluxo essencial.
AUTH-006 depende de inspeção do contrato instalado: endpoint, payload, status e
formato da credencial ainda não confirmados. Não implementar por suposição.

## Casos planejados

Cada caso começa em contexto isolado, sem aproveitar sessão de outro caso.

| Caso | Ação | Resultado esperado proposto |
| --- | --- | --- |
| UI-AUTH-001 | Entrar com tenant válido. | Área autenticada e identidade correta; URL sozinha não basta. |
| UI-AUTH-002 | Tenant válido e uma senha incorreta, uma vez. | Feedback de rejeição, formulário disponível e área protegida inacessível. |
| UI-AUTH-003 | Enviar ambos os campos vazios. | Feedback e ausência de sessão; não exigir botão desabilitado. |
| UI-AUTH-004 | Email válido e senha vazia; enviar. | Rejeição com feedback e ausência de sessão. |
| UI-AUTH-005 | Email malformado e retirada de foco. | Validação de formato na interface; não atribuir validação ao backend. |
| UI-AUTH-006 | Abrir `/home` sem autenticar. | Área protegida inacessível e fluxo de login apresentado. |
| UI-AUTH-007 | Entrar; sair pelo controle a inspecionar; reabrir área protegida. | Estado anônimo; recarregar não restaura acesso. |
| API-AUTH-001 | Após confirmar contrato, autenticar tenant válido. | Resposta conforme contrato e credencial utilizável em recurso protegido a confirmar. |
| API-AUTH-002 | Após confirmar contrato, enviar uma senha incorreta. | Rejeição conforme contrato e ausência de credencial válida. |
| API-AUTH-003 | Após confirmar contrato, acessar recurso protegido sem credencial. | Rejeição conforme contrato, sem dados protegidos. |

Primeiro incremento proposto: UI-AUTH-001, UI-AUTH-002 e UI-AUTH-006. Demais casos
permanecem no planejamento. Evitar tentativas inválidas repetidas com o tenant
compartilhado; bloqueio e rate limiting exigem regras e contas dedicadas.

## Arquitetura da próxima implementação

- `tests/ui/authentication.robot`: cenários e assertions do primeiro incremento.
- `resources/pages/login.resource`: ações e seletores confirmados.
- Resource compartilhado: navegador, contexto isolado e teardown mesmo em falha.
- `variables`: URL, navegador e timeout. Credenciais via ambiente, sem senha
  literal nos testes ou exposição em logs.
- Robot Framework e Browser Library executam UI; RequestsLibrary entra após
  confirmação do contrato. Evidências ficarão em `results`, ignoradas pelo Git.

Não há necessidade demonstrada de biblioteca Python própria ou acesso ao banco
para provar login. Não criar testes de integração apenas para preencher pastas;
um fluxo de isolamento entre tenants por API/UI exigirá requisito próprio.

Técnicas: partições válida/inválida, presente/ausente e email válido/malformado;
transições anônimo → autenticado → anônimo; regressão priorizada por risco.
Lacunas: comprimentos-limite, expiração, invalidação de tokens no servidor,
bloqueio, outros perfis e isolamento entre tenants. Não inventar limites ou tempos.

## Verificação e investigação

```powershell
Get-Content -Encoding UTF8 docs/authentication-requirements.md
Get-Content -Encoding UTF8 docs/traceability.md
docker compose --env-file infrastructure/.env -f infrastructure/compose.yaml ps --all
```

O primeiro incremento tem suíte executável conforme `authentication-execution.md`.
Os demais casos continuam planejados, sem execução declarada.
Aplicação inacessível: examinar containers e logs. Seletor falhando: inspecionar
DOM, idioma e unicidade. Divergência de comportamento: confirmar o requisito
antes de registrar defeito ou modificar a expectativa para fazer o teste passar.

## Revisão e atividade de aprendizado

Compare os riscos de UI-AUTH-001, UI-AUTH-002 e UI-AUTH-006. A implementação será
feita pelo agente; o primeiro incremento validado já foi concluído.

Perguntas QA Sênior:

1. Por que `/home` sem verificar identidade pode produzir falso positivo?
2. Qual defeito o acesso direto sem sessão detecta que a senha incorreta pode não detectar?
3. Quando uma divergência exige defeito do produto, correção do teste ou esclarecimento do requisito?
