# Matriz de rastreabilidade

Desenho inicial validado pelo responsável. CT01, CT02 e CT03 foram implementados
e executados em 25/10/2026; demais casos permanecem planejados. IDs UI-AUTH foram
preservados: CT03 corresponde a UI-AUTH-006. `—` indica arquivo ainda inexistente.
Inspeções exploratórias não contam como aprovação automatizada.

| Requisito | Descrição | Risco/prioridade | ID do caso | Camada | Cenário/técnica | Tags | Arquivo do teste | Evidência/resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AUTH-001 | Acesso válido | Alta | CT01 / UI-AUTH-001 | UI | Identidade e recurso protegido | ui, auth, smoke, regression, CT01, AUTH-001, UI-AUTH-001 | tests/ui/authentication.robot | PASS; results/authentication/log.html |
| AUTH-002 | Senha incorreta | Alta | CT02 / UI-AUTH-002 | UI | Rejeição e acesso negado | ui, auth, negative, regression, security, CT02, AUTH-002, UI-AUTH-002 | tests/ui/authentication.robot | PASS; results/authentication/log.html |
| AUTH-003 | Campos vazios | Média | UI-AUTH-003 | UI | Ausência de dados | ui, auth, negative, regression, AUTH-003, UI-AUTH-003 | — | Não executado |
| AUTH-003 | Senha vazia | Média | UI-AUTH-004 | UI | Ausência parcial | ui, auth, negative, regression, AUTH-003, UI-AUTH-004 | — | Não executado |
| AUTH-003 | Email malformado | Média | UI-AUTH-005 | UI | Partição inválida | ui, auth, negative, regression, AUTH-003, UI-AUTH-005 | — | Não executado |
| AUTH-004 | URL protegida sem sessão | Alta | CT03 / UI-AUTH-006 | UI | Controle de acesso sem sessão | ui, auth, security, regression, CT03, AUTH-004, UI-AUTH-006 | tests/ui/authentication.robot | PASS; results/authentication/log.html |
| AUTH-005 | Logout | Alta | UI-AUTH-007 | UI | Transição de estado | ui, auth, regression, AUTH-005, UI-AUTH-007 | — | Não executado |
| AUTH-006 | API credenciais válidas | Alta | API-AUTH-001 | API | Contrato pendente | api, auth, smoke, AUTH-006, API-AUTH-001 | — | Não executado |
| AUTH-006 | API senha incorreta | Alta | API-AUTH-002 | API | Contrato pendente | api, auth, negative, regression, AUTH-006, API-AUTH-002 | — | Não executado |
| AUTH-006 | Recurso sem credencial | Alta | API-AUTH-003 | API | Contrato pendente | api, auth, security, regression, AUTH-006, API-AUTH-003 | — | Não executado |

Cada caso deve ter identificação estável e ligação com seu requisito. Considerar
cenários positivos, negativos, limites, transições de estado e regressão conforme
o risco. Registrar resultados apenas após execução, com referência à evidência.
Ao implementar os demais casos, preencher o caminho real do arquivo. Suas tags são propostas.
Limites de tamanho, expiração, bloqueio e isolamento entre tenants são lacunas;
não há casos de integração definidos nesta etapa.

Detalhes, limitações e histórico da execução em
[Execução de autenticação](authentication-execution.md). O resumo estruturado está
em `results/authentication/output.xml`; artefatos são locais e ignorados pelo Git.

CT01, CT02 e CT03 também passaram na execução GitHub Actions 40232265170 em Linux;
consulte [evidências remotas](ci-first-run.md). Demais casos continuam não executados.
