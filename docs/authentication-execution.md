# Etapa 5 — implementação e execução de CT01, CT02 e CT03

## Arquivos e responsabilidades

| Arquivo | Função |
| --- | --- |
| `tests/ui/authentication.robot` | Os três cenários, tags, setup e teardown. |
| `resources/browser.resource` | Importa Browser e variáveis; cria navegador, contexto isolado e página; captura falha e fecha recursos. |
| `resources/pages/login.resource` | Locators reais, preenchimento e validação da rejeição. |
| `resources/pages/authenticated.resource` | Assertions de identidade, área autenticada, dispositivos e negação de acesso. |
| `variables/environment.py` | Lê ambiente, valida configuração e encapsula senhas em Secret. |
| `docs/traceability.md` | Relaciona requisitos, IDs históricos, CTs e resultado observado. |

Não foram adicionadas dependências. Usamos Robot Framework 7.5, Browser 20.6.0
e Chromium já preparados. Não foi necessário criar uma Custom Library Python;
o módulo Python é um arquivo de variáveis, não uma biblioteca de keywords.

## Como as camadas se conectam

```text
authentication.robot
  Resource ../../resources/pages/authenticated.resource
    Resource login.resource
      Resource ../browser.resource
        Variables ../variables/environment.py
        Library Browser
```

Caminhos de importação são relativos ao arquivo que declara o import. Variáveis
são importadas antes da Library porque seus valores configuram o timeout dela.

Exemplo: CT01 chama `Entrar Com Credenciais    ${USERNAME}    ${PASSWORD}`.
O Robot encontra essa keyword no Resource importado, associa os dois valores a
`[Arguments]    ${usuario}    ${senha}` e executa `Fill Text`, `Fill Secret` e
`Click`. Os casos descrevem o fluxo; os Resources centralizam ações e seletores.

A Browser Library recebe as keywords do Robot e comunica-se com seu processo
Node/Playwright, que controla Chromium. O Playwright resolve locators, verifica
condições de interação e executa as ações. Não se usa Selenium neste fluxo.

## Isolamento, esperas e assertions

Suite Setup inicia um navegador. Test Setup cria um contexto novo (cookies e
localStorage separados) e uma página em branco para cada caso. O contexto usa
`en-US` para tornar a mensagem de rejeição previsível neste laboratório.

Test Teardown tenta capturar uma imagem se houve falha e fecha o contexto em
`FINALLY`. Suite Teardown fecha todos os navegadores, inclusive se algum caso
falhou. O contexto de CT01 não é reutilizado por CT02 ou CT03.

`Wait For Elements State` espera condições observáveis. `Get Url` e `Get Text`
com `==` fazem assertions com repetição até o prazo configurado (15s por padrão).
Não há Sleep. Aumentar o timeout sem investigar não corrige seletor incorreto.

Locators foram inspecionados na instância real: IDs dos campos, botão submit,
`.error-toast .toast-text`, `.tb-user-display-name` e `table[role="table"]`.

- CT01 valida `/home`, identidade e acesso a `/entities/devices`, com tabela
  visível e identidade preservada. Não depende dos nomes ou quantidade de demos.
- CT02 faz uma tentativa inválida, verifica `Invalid username or password`,
  formulário e negação ao abrir `/home` depois da rejeição.
- CT03 abre `/home` diretamente em contexto sem sessão e verifica login visível
  e ausência de identidade/tabela protegida.

São verificações de controle de acesso pela UI. Não comprovam proteção de todos
os endpoints, invalidação de tokens, outros perfis ou isolamento entre tenants.
Esses pontos permanecem fora do escopo e exigem testes próprios.

## Configuração e execução pelo terminal

Na raiz, em PowerShell. O laboratório deve estar ativo. Estes comandos solicitam
a senha sem gravá-la no código ou no histórico como literal:

```powershell
$env:TB_BASE_URL = 'http://127.0.0.1:8080'
$env:TB_USERNAME = 'tenant@thingsboard.org'
$credential = Get-Credential -UserName $env:TB_USERNAME -Message 'Credenciais do tenant do laboratorio'
$env:TB_PASSWORD = $credential.GetNetworkCredential().Password
try {
    .\.venv\Scripts\python.exe -m robot --outputdir results/authentication tests/ui/authentication.robot
    $robotExit = $LASTEXITCODE
    Write-Output "Codigo Robot: $robotExit"
} finally {
    Remove-Item Env:TB_PASSWORD -ErrorAction SilentlyContinue
    Remove-Variable credential -ErrorAction SilentlyContinue
}
```

O arquivo de variáveis requer TB_USERNAME e TB_PASSWORD, inclusive para executar
esta suíte completa. TB_INVALID_PASSWORD é opcional: se ausente, gera uma senha
aleatória em memória e garante que difere da válida. Nenhuma senha está no fonte.
O `.env` da infraestrutura configura o banco e não é carregado por estes testes.

Opções de ambiente: TB_BROWSER (chromium), TB_HEADLESS (true/false), TB_UI_TIMEOUT
(15s), TB_BASE_URL (origem HTTP sem caminho). Para observar o navegador local,
use `$env:TB_HEADLESS='false'` antes da execução e remova a variável ao terminar.

Exemplos de filtros, com as credenciais já presentes no ambiente:

```powershell
.\.venv\Scripts\python.exe -m robot --include smoke --outputdir results/smoke tests/ui/authentication.robot
.\.venv\Scripts\python.exe -m robot --include security --outputdir results/security tests/ui/authentication.robot
.\.venv\Scripts\python.exe -m robot --test 'CT03*' --outputdir results/ct03 tests/ui/authentication.robot
```

CT01 tem smoke e regression; CT02 e CT03 têm regression e security.
Filtros acima são exemplos de uso, não execuções adicionais declaradas.
Código zero indica aprovação; um valor não zero exige leitura do resultado.

## Resultado real em 25/10/2026

Execução final: `results/authentication/output.xml`, Robot 7.5, Python 3.12.1,
Chromium headless, locale en-US, ThingsBoard CE 4.3.1.7 local.

| Caso | ID rastreável preservado | Resultado | Duração do caso |
| --- | --- | --- | --- |
| CT01 — Login válido | UI-AUTH-001 / AUTH-001 | PASS | 6,04s |
| CT02 — Senha incorreta | UI-AUTH-002 / AUTH-002 | PASS | 3,50s |
| CT03 — Rota protegida sem sessão | UI-AUTH-006 / AUTH-004 | PASS | 2,48s |

Resultado final: 3 testes, 3 aprovados, 0 falhas; código de saída 0.
IDs UI-AUTH não foram renumerados: CT03 corresponde ao cenário UI-AUTH-006,
enquanto UI-AUTH-003 continua sendo o cenário futuro de campos vazios.

Houve falhas durante o desenvolvimento: primeiro, importação da Library antes
das variáveis; depois, prazo padrão de assertion insuficiente para redirecionar
(CT02 passou, CT01 e CT03 falharam). Corrigimos a ordem e configuramos repetição
condicional com UI_TIMEOUT, sem mudar o esperado. A tentativa intermediária
está em `results/authentication-attempt-02`; o diretório principal tem o resultado final.
Na descoberta também foram descartados um link ambíguo e o seletor `mat-table`:
o DOM real usa `table[role="table"]`.

Senhas são Secret do Robot e preenchidas com Fill Secret. Uma busca pela senha
incorreta gerada não a encontrou nos artefatos textuais finais. A inspeção do XML
também não encontrou a senha válida como mensagem ou argumento literal isolado.
Isso é uma verificação limitada, não uma garantia universal: não habilitar debug
do Playwright ou captura de rede com segredos sem revisar seu conteúdo.

## Como interpretar report.html e log.html

- `results/authentication/report.html`: resumo da execução, totais e estatísticas
  por tags; selecione um teste para seguir ao detalhe no log.
- `results/authentication/log.html`: árvore suíte → teste → keywords; expanda
  uma keyword para ver argumentos, assertion, mensagens e duração.
- `results/authentication/output.xml`: resultado estruturado para ferramentas e CI.
- `results/authentication/browser`: capturas e outros artefatos referenciados
  pelo log. Preserve a pasta completa ao compartilhar evidências.

Os arquivos de resultados são locais e ignorados pelo Git. Nova execução no mesmo
outputdir substitui relatórios anteriores; use outra pasta se precisar preservá-los.

## Encontrar a causa de uma falha

1. Comece pela primeira keyword que falhou no log, não apenas pela linha vermelha
   do caso. Distingua erro de importação/setup de assertion funcional.
2. Veja esperado, obtido e captura. Timeout de locator pode indicar seletor,
   locale ou página errados, além de lentidão ou indisponibilidade.
3. Para erro de acesso, confirme usuário/ambiente sem imprimir senha; compare
   rejeição observada com requisito e estado do contexto.
4. Para aplicação inacessível, consulte `docker compose --env-file infrastructure/.env
   -f infrastructure/compose.yaml ps --all` e os logs. Não reinstale o banco.
5. Corrija a causa e execute novamente; não remova assertions para obter PASS.

Nenhum commit ou push realizado. Git Flow e CI/CD aguardam validação.

## Atividade de revisão e três perguntas

Abra report.html, localize CT02 e expanda `Login Deve Ser Rejeitado` no log para
identificar a mensagem comparada. Não precisa implementar ou reexecutar nada.

1. Por que New Page no mesmo contexto não isolaria a autenticação entre CT01 e CT03?
2. Qual a diferença entre autoespera de Click e a assertion de identidade após o login?
3. Se CT02 falhar por ausência da mensagem, quais evidências distinguem mudança de locator, erro de infraestrutura e defeito do produto?
