# Torre EV — Contexto Completo do Projeto

> Este arquivo é o **histórico/conversa do projeto**. Se você copiar esta pasta para
> outro computador, leia este arquivo primeiro — ele contém tudo o que foi feito,
> as decisões, as correções e como regenerar os artefatos.

- **Disciplina:** Programação de Dispositivos Móveis
- **Plataforma:** MIT App Inventor 2 (ai2)
- **Projeto:** Torre EV — Painel do Síndico (gestão de recarga de veículos elétricos em condomínio)
- **Estudo de caso:** "Residencial Parque das Torres" (condomínio antigo, 120 aptos, 240 vagas)

---

## 1. Arquivos da pasta do projeto

| Arquivo | Papel |
|---|---|
| `TorreEV.aia` | **App final pronto para importar** no App Inventor (4 telas) |
| `Documentacao_TorreEV.pdf` | Documentação técnica (9 páginas) alinhada ao app atual |
| `App_condominio.aia` | Material de referência do aluno (exemplo de app) |
| `Projeto_Carros_Eletricos.pdf` | Edital/enunciado do desafio |
| `_gerador/aia_bytes.py` | Bytes exatos do `TorreEV.aia` (embutidos, base64) |
| `_gerador/gerar_aia.py` | Regenera o `TorreEV.aia` byte a byte (fonte da verdade = `aia_bytes.py`) |
| `_gerador/gerar_doc.py` | Regenera a `Documentacao_TorreEV.pdf` |
| `CONTEXTO_PROJETO.md` | Este arquivo |

### Como regenerar
```bash
cd _gerador
python3 gerar_aia.py    # grava ../TorreEV.aia (byte idêntico)
python3 gerar_doc.py    # grava ../Documentacao_TorreEV.pdf
```
Dependências Python: `reportlab` (doc) e bibliotecas padrão (`zipfile`, `base64`). Validação do PDF usa `pypdf`.

---

## 2. O aplicativo (especificação atual)

> [!] **Os nomes mudaram.** Telas e componentes foram renomeados (ver 3.15). As seções
> 3.x anteriores citam os nomes antigos de propósito — descrevem o que estava na tela
> quando cada bug aconteceu. A tabela de-para está na **seção 6**.

- **Package:** `appinventor.ai_gustavobrito170.TorreEV` · **Tela principal:** Screen1 · **YaVersion 237**
- **4 telas:**
  - **Screen1 — Login:** senha (padrão `1234`), TextBox com `Password: True`, botão Entrar, erro no Label1, Notifier.
  - **Screen2 — Painel:** cartões `CardStatus`/`CardUso`/`CardAcoes`, `Slider1` **interativo para ajustar o limite** (faixa 5–60 kW, salva em `limiteKw`, atualiza `Label6` ao mover), `Label4` (kW em uso), `Label6` (limite), `Label7` (vagas), `ListPicker1` (recargas ativas), botões Nova Recarga/Encerrar/Histórico, `Clock1` (Timer 2000 ms → `AtualizarPainel` automático), `TextToSpeech1`.
  - **Screen3 — Cadastro:** nome + kW (aceita ponto **ou vírgula** como decimal, ex. `7,2`), validação encadeada com `EhNumero(texto)` e limite **dinâmico** (`limite` do TinyDB), `CalcularTotal` (procedure com retorno).
  - **Screen4 — Histórico:** `ListView1` com nome, kWh, **duração (h)** e data.
- **TinyDB (tags):**
  - `senha` → padrão `"1234"`
  - `limiteKw` → padrão `22` (o limite do condomínio é **22 kW**, não 30)
  - `recargasAtivas` → lista de recargas `[nome, kw, duracao, inicio, dataInicio]`
  - `historico` → lista de recargas encerradas `[nome, kwh, horas, dataHoraFormatada]`

### Lógica-chave (Screen2)
- `AtualizarPainel` soma kW das ativas e atualiza labels/cartão; **rodada automaticamente a cada 2 s pelo `Clock1.Timer`** (TimerEnabled True, TimerInterval 2000). Não mexe mais no Slider (ele é o controle de limite, ver abaixo).
- **`Slider1.PositionChanged`:** ao mover o Slider, o valor vira o novo `limite` (evento usa o parâmetro `thumbValue`), grava em `TinyDB1.StoreValue("limiteKw", limite)` e atualiza `Label6` (`"limite: X kW"`). O `AtualizarPainel` seguinte (≤ 2 s) reavalia o semáforo com o novo limite. Faixa fixa no `.scm`: `MinValue 5`, `MaxValue 60`, `Value 22`, `Enabled True`.
- **Semáforo:** verde < 80% do limite · amarelo ≥ 80% · vermelho > limite.
- **Alertas só por transição de status** — variável global `statusAnt` **persiste** (não é zerada no Initialize); Notifier/TTS disparam apenas quando o status muda. Estado de emergência = cartão vermelho + "SOBRECARGA!".
- **ListPicker sem "reset" a cada atualização:** os nomes das recargas ativas ficam em `nomesAnt` (lista); `ListPicker1.Elements`/`Selection` só são reescritos quando `nomes != nomesAnt` — preserva a seleção do síndico durante os ticks do timer.

### Lógica-chave (Screen3)
- `EhNumero(texto)` (procedure com argumento): `é número?(texto) OU é número?(substituir "," por "." em texto)` — aceita `"7"`, `"7.2"`, `"7,2"`.
- Validação IF1: nome vazio **ou** `não(EhNumero(kW))` **ou** potência < 1 **ou** potência > `limite` (dinâmico, do TinyDB — não é mais `22` fixo no bloco).
- IF2: `(CalcularTotal + potênciaNormalizada) > limite` impede exceder a capacidade.
- A potência é salva **normalizada** (`substituir "," por "."`) em `recargasAtivas`.

### Versões dos componentes no `.scm`
Form 32 · Vertical/HorizontalArrangement 4 · Label 5 · TextBox 14 · Button 7 · Slider 2 · ListPicker 8 · ListView 3 · TinyDB 3 · Notifier 6 · **TextToSpeech 5** · **Clock 3**

### Formato dos blocos (importante para quem editar `.bky` na mão)
- `controls_openAnotherScreen` usa `<value name="SCREEN">...` **sem** mutation.
- `controls_if` usa mutation `elseif`/`else` + inputs `IF0/DO0...ELSE`.
- Mutations são serializadas como `></mutation>` (não self-closing).
- JSON do `.scm` usa espaços (`"MaxValue": "22"`).
- Blocos `global_declaration`/eventos top-level: `inline="false"` explícito + `x`/`y` (posicionamento em grade).
- `procedures_defreturn` **não tem `STACK`**: para procedure com retorno e corpo, usar `controls_do_then_return` dentro do `<value name="RETURN">` (o gerador YAIL ignora `STACK` desde 2013 — ver 3.7).

### Paleta de cores do app
Fundo `#F5F5F5` · Primário `#0D47A1` · Escuro `#002171` · Acima/cards brancos · Verde `#4CAF50` · Vermelho `#D32F2F` · Verde-salvar `#388E3C` · Cinza-botões `#EEEEEE`

---

## 3. Histórico do que foi feito (linha do tempo)

### 3.1 Primeira versão (sessão anterior)
1. Gerado `TorreEV.aia` completo via script Python (`gerar_aia.py`) — 4 telas, login, painel, cadastro, histórico.
2. **Correção:** limite trocado de **30 kW → 22 kW** em todo o app (edital diz 22).
3. **Simplicação:** removidos campos/botões desnecessários (ex.: Button4, TextBox3, Label4 antigo, "Ajustar Limite").
4. PDF atualizado e validado.

### 3.2 Reestruturação (sessão atual — pedido "app não ficou legal, tem bugs e visual ruim")
1. Usuário confirmou via perguntas: **visual das telas feio, blocos bagunçados/sobrepostos, lógica com bugs** (sem bug específico).
2. **Visual novo:** cards brancos, paleta azul-escuro, botões coloridos, senha mascarada, Slider como barra de carga.
3. **Blocos em grade:** posições calculadas `x=40+(col%3)*330`, `y=40+(linha//3)*230` — sem sobreposição nem amontoados.
4. **Lógica corrigida (bugs):**
   - Alertas repetitivos a cada segundo → **alerta só na transição de status** (global `statusAnt`).
   - Faltava `inline="false"` explícito nos blocos top-level → adicionado.
   - Validação encadeada no cadastro (nome vazio → kW inválido → excede limite).
5. **Validação final: 0 erros** (JSON/XML válidos, UUIDs únicos por tela, MaxValue 22, Slider desabilitado, senha com Password, blocos em grade, ids únicos, componentes presentes).
6. PDF reescrito para refletir o novo visual/lógica; checagens passaram.

### 3.3 Correção do PDF (pedido "documento mal formatado")
1. Problemas: cabeçalho/página no topo das páginas (rodapé não era rodapé), fundo colorido de títulos só no texto (não de largura total), caixas de código uma por linha, balas mal alinhadas, setas `→` sem glifo na fonte.
2. **Layout novo (reportlab):** rodapé real com "Página N" (só em páginas >1), barra de cabeçalho no topo, títulos em barra azul de largura total (Table), bloco de código em **caixa única** com borda, bullets com recuo correto (ListFlowable), setas trocadas por `>`, `×`→`x`, `≥`→`>=`.
3. Validação: 9 páginas, sem estouro de margem, sem setas `→`, conteúdo correto.

### 3.4 Portabilidade (sessão atual)
1. Criada pasta `_gerador` na pasta do projeto com os geradores (temp `/var/folders/.../opencode` é **apagado** a cada sessão — nunca deixar arquivos importantes lá).
2. `aia_bytes.py` embute os bytes exatos do `.aia` → regeneração **byte idêntica** garantida.
3. Este `CONTEXTO_PROJETO.md` criado para levar a conversa para outro computador.

### 3.5 Correções de bugs e melhorias no app (sessão atual)
1. **Potência decimal:** `TextBox2` perdeu `NumbersOnly: True` — agora aceita `7.2` e `7,2`.
2. **Painel em tempo real:** `Clock1` (Screen2) configurado com `TimerEnabled: True`, `TimerInterval: 2000` e evento `Clock1.Timer` chamando `AtualizarPainel` — o painel se atualiza sozinho a cada 2 s.
3. **Alerta não repete ao voltar:** removido o `set statusAnt = ""` do `Screen2.Initialize` (era a causa de repetir alerta/TTS a cada retorno). `statusAnt` agora persiste.
4. **ListPicker preserva seleção:** adicionado global `nomesAnt` + `controls_if` (`nomes != nomesAnt`) em `AtualizarPainel`; `Elements`/`Selection` só são reescritos quando a lista de nomes muda.
5. **Validação com limite dinâmico:** condição IF1 do cadastro deixou de usar o `22` fixo do bloco (`blk242`) e passou a usar `limite` global (TinyDB); adicionada procedure `EhNumero(texto)` para validar número (aceita vírgula); mensagem de erro passou a ser dinâmica (`"Potencia invalida (1 a " + limite + " kW)"`).
6. **Potência normalizada:** nos blocos IF2 e de salvamento (`ADD1`), o valor digitado é normalizado com `substituir "," por "."` antes de somar/armazenar (evita que `"7,2"` vire texto inválido).
7. **Histórico com duração:** `text_join` do Screen4 passou de 6 para **8 itens**: `"Morador: " + nome + " | " + kWh + " kWh | " + horas + " h | " + data` (item[3] = horas agora exibido).
8. Verificação pós-edição: XML dos 4 `.bky` válido (ids únicos), JSON dos 4 `.scm` válido, `TorreEV.aia` rezipado e `aia_bytes.py` **regenerado** (byte idêntico ao `.aia` editado — conferido com `gerar_aia.py`).

### 3.6 Correção de erro de runtime no login (sessão atual)
1. **Bug:** ao abrir o app, erro de runtime `Wrong number of arguments for GetValue` com `["senha"]` — o bloco `TinyDB1.GetValue` do `Screen1.Initialize` tinha `<value name="ARG1">1234</value>` (texto **sujo direto dentro do `<value>`**, sem um bloco `math_number`). O builder gera então `(GetValue "senha")` com 1 argumento em vez de 2.
2. **Causa raiz:** valor padrão de `valueIfTagNotThere` sem bloco filho; validações antigas de "ids únicos"/"value com bloco" usavam `root.iter('block')` **sem o namespace** do Blockly (`https://developers.google.com/blockly/xml`) — passavam em silêncio (0 blocos encontrados).
3. **Correções no `Screen1.bky`:**
   - `<value name="ARG1">1234</value>` → `<value name="ARG1"><block type="math_number" inline="true" id="blk18"><field name="NUM">1234</field></block></value>`.
   - mutation do `controls_if` corrigida de `elseif="1" else="1"` (mas sem `IF1`/`DO1` — estrutura quebrada) para `else="1"` apenas.
4. **Bug próprio do `screen` corrigido junto:** o gate `nomes != nomesAnt` da Screen2 tinha o getter `blk67` (nomes) **reutilizado em 2 novos lugares** com o mesmo id → ids duplicados. Renomeados para `blk404` (comparação) e `blk407` (atribuição de `nomesAnt`); `blk67` original permanece no setter do `ListPicker.Elements`.
5. **Mutations `controls_if` normalizadas** (eram maior que o número real de ramos → ramos elseif mortos com condição `#f`): `blk89`/`blk108`/`blk120` (transições de status) perderam o `elseif="1"`; `blk121` `elseif="2"`→`elseif="1"`; `blk190` (Encerrar) `elseif="1" else="1"`→`else="1"`; `blk299` (Screen3) `elseif="3"`→`elseif="2"`. Verificado que cada `controls_if` agora tem exatamente os ramos declarados.
6. **Validação agora com namespace correto:** checar `value`/`statement` via `{%s}value % NS` e ids via `root.iter('{%s}block' % NS)` — captura `value` vazio e ids duplicados de verdade.

### 3.7 Erro de runtime `+` com `false` no cadastro (sessão atual)
1. **Bug relatado:** ao salvar uma recarga (ex.: 8.8 kW), erro de runtime `The operation + cannot accept the arguments: [false], ["8.8"]` e **nada era salvo**.
2. **Investigação:** o erro é o `math_add` do IF2 do Screen3: `(CalcularTotal() + potênciaNormalizada) > limite`. O segundo argumento `"8.8"` era o `substituir "," por "."` (correto); o **primeiro argumento era `false`**, ou seja, `CalcularTotal()` retornava `false`/valor não numérico.
3. **Causa raiz (estrutural):** a procedure `CalcularTotal` (bloco `procedures_defreturn`) usava o formato **antigo (2012)** com `<statement name="STACK">` contendo o `set total = 0` e o `for-each` da soma. O gerador YAIL do App Inventor **ignora o `STACK` de `procedures_defreturn` desde 2013** (`[lyn, 01/15/2013] Edited to remove STACK (no longer necessary with DO-THEN-RETURN)`) — confirmado no fonte `generators/yail/procedures.js` e comparando com um `.bky` real exportado pelo AI2 (projeto de referência `kio4/p46.aia`), cujo `defreturn` só tem `RETURN`, sem `STACK`. O App Inventor moderno tem `bodyInputName: 'RETURN'` e **nenhum input `STACK`** no bloco de procedure com retorno. Consequência: o corpo do cálculo era descartado e a procedure retornava o valor do global `total` (ou `false` se não numérico) — a soma nunca era calculada, o IF2/IF3 nunca passavam e **nada era salvo**.
4. **Correção no `Screen3.bky` (`blk272`):** removido o `<statement name="STACK">` do `procedures_defreturn`; o corpo (`set global total = 0` + `for-each` somando `list-select-item(item, 2)`) e o retorno (`global total`) foram movidos para um bloco **`controls_do_then_return`** dentro do `<value name="RETURN">`:
   - `<value name="RETURN">` → `<block type="controls_do_then_return" id="blkCT1">` com `<statement name="STM">` (2 blocos: set + for-each) e `<value name="VALUE">` (getter `global total`, `blk271`).
   - Gera YAIL: `(def (p$CalcularTotal) (begin (set-var! g$total 0) (for-each ...) (get-var g$total)))` — **sempre retorna número** (0 ou a soma real).
   - A outra procedure `EhNumero` (`blk500`) já estava no formato correto (só `RETURN`, sem `STACK`) — não exigiu mudança.
5. **Verificação:** XML válido (97 blocos, ids únicos), `blk272` sem `STACK` e com `RETURN`→`controls_do_then_return` (STM 2 blocos + VALUE getter), demais validadores (mutations de `controls_if`, JSON dos `.scm`, Sem TextBox3/Button4/NumbersOnly, Clock1, etc.) passando; `.aia` rezipado, `aia_bytes.py` **regenerado** e `TorreEV.aia` da pasta byte idêntico por conteúdo (9 arquivos).
6. **Formato correto para "procedure com retorno + corpo":** em vez de `<statement name="STACK">` dentro de `procedures_defreturn`, usar um bloco `controls_do_then_return` dentro do `<value name="RETURN">` (com `<statement name="STM">` e `<value name="VALUE">`). Este é o padrão do AI2 desde 2013.

### 3.8 Slider como controle do limite + esclarecimento de "salvar não atualiza histórico" (sessão atual)
1. **Relato:** "cliquei em salvar e não atualizou o histórico nem nada" e "para que serve o slider? eu mexo e não acontece nada".
2. **Esclarecimento de comportamento (não era bug):** salvar uma recarga **não adiciona ao Histórico** — o histórico (Screen4) só ganha registro ao **Encerrar** uma recarga no painel. Ao salvar, o Painel (Label4 kW/vagas) atualiza via `OtherScreenClosed` + `Clock1.Timer` (≤ 2 s). O slider antigo era **puramente visual** (`Enabled: "False"`, dirigido por `AtualizarPainel`) — mover não fazia nada por design. O "não salvava" real era o bug do `+` (3.7) — corrigido; é preciso **reimportar o novo `TorreEV.aia` e reconstruir** o app no celular para o fix valer.
3. **Mudança (feature):** `Slider1` passou a ser o **controle do limite** no Screen2:
   - `.scm`: `Enabled: "True"`, `MinValue: "5"`, `MaxValue: "60"`, `Value: "22"`.
   - Novo evento `Slider1.PositionChanged` (`component_event`, mutation com `event_name="PositionChanged"` e parâmetro `thumbValue` — serializado como atributo `param_name0` na mutation, formato do AI2 moderno): `set global limite = thumbValue` → `TinyDB1.StoreValue("limiteKw", limite)` → `set Label6.Text = "limite: " + limite + " kW"`.
   - `Screen2.Initialize` ganhou `set Slider1.Value = global limite` (após carregar o limite do TinyDB) para o slider refletir o limite salvo.
   - **Removidos de `AtualizarPainel`** os 2 blocos que escreviam no slider (`set Slider1.MaxValue = limite` e `set Slider1.Value = choose(...)`), para não "brigar" com o arraste do usuário (o `AtualizarPainel` roda a cada 2 s e sobrescreveria o valor).
4. **Verificação:** XML válido, ids únicos (229 blocos no Screen2.bky), `blk59`/`blk66` removidos, `blkS1` (evento) com DO = `blkS2`(set limite) → `blkS4`(StoreValue) → `blkS7`(Label6), `blk224` DO = set limite → `blkS12`(set Slider1.Value) → `AtualizarPainel`; `.aia` rezipado, `aia_bytes.py` **regenerado** e `TorreEV.aia` da pasta byte idêntico por conteúdo (9 arquivos; `project.properties` inalterado).
5. **Marcador de versão (`v4`):** usuário relatou que nada era registrado mesmo após as correções — sintoma típico de **build/projeto antigo rodando no celular** (o app roda pelo site AI2 + AI Companion, ou seja, o que vale é o **projeto aberto no navegador**, não o `.aia` da pasta). Para diagnóstico definitivo, o Screen2 agora exibe **`PAINEL DO SINDICO - v4`** (Label1) e `Title: "Torre EV - Painel v4"` no `.scm`. Se o celular não mostrar "v4", o projeto aberto no AI2 é uma versão antiga → **importar o `TorreEV.aia` de novo** (Importar projeto) e testar por ele.

### 3.9 CAUSA RAIZ: blocos irmãos dentro de `<statement>` (sessão atual)
1. **Bug relatado:** ao clicar em Salvar, erro de runtime `Cannot find the component: Label5` repetindo (aviso de supressão de 5 s). O projeto no AI2 já era o **v4**, então não era build antigo.
2. **Investigação:** `Label5` existe no `Screen2.scm` (subtítulo do `CardStatus`) e é escrito por `blk84`/`blk105`/`blk119`, sempre **depois** de `Label4`/`Label6`/`Label7` no `AtualizarPainel`. O erro parar exatamente em `Label5` só faz sentido se os blocos anteriores **não estivessem sendo executados**.
3. **Causa raiz (estrutural, afeta as 4 telas):** todos os `.bky` gerados encadeavam comandos sequenciais como **blocos irmãos** dentro do mesmo `<statement>`:
   ```xml
   <statement name="DO"><block id="A"/><block id="B"/><block id="C"/></statement>
   ```
   O loader do Blockly (`Blockly.Xml.domToBlockHeadless_`) percorre os filhos de `value`/`statement` e **sobrescreve** a variável `childBlockElement` a cada `<block>` encontrado — ou seja, **só o último irmão é carregado** e os anteriores são descartados em silêncio. O formato correto é aninhar com `<next>`:
   ```xml
   <statement name="DO"><block id="A"><next><block id="B"><next><block id="C"/></next></block></next></block></statement>
   ```
   O projeto tinha **0 tags `<next>`** e **48 blocos descartados** (Screen1: 1 · Screen2: 40 · Screen3: 5 · Screen4: 2).
4. **Sintomas que isso explica** (todos já relatados antes e atribuídos a outras causas):
   - `AtualizarPainel` virava só o `controls_if` final → `Label4`/`Label6`/`Label7`/`ListPicker1` nunca atualizavam, `total`/`nomes` nunca eram recalculados. No estado normal (`ok`) o único componente que ele tocava era o **`Label5`**.
   - Salvar no Screen3 executava **só** o `controls_closeScreen`; o `lists_add_items` e o `TinyDB1.StoreValue` eram descartados → **"cliquei em salvar e não aconteceu nada"** (3.8) e **"nada era registrado"** (3.8.5) nunca foram build antigo.
   - `Screen2.Initialize` só chamava `AtualizarPainel`, sem carregar o `limite` do TinyDB nem posicionar o Slider.
5. **Correção:** transformação mecânica dos 4 `.bky`, encadeando os irmãos com `<next>` (14 statements, 48 blocos reconectados), preservando os atributos originais byte a byte — inclusive o `xmlns` das `mutation`, que se perderia se o arquivo fosse reserializado por um parser XML comum.
6. **Bug secundário corrigido junto (`Clock1` atravessando telas):** `Clock1` tinha `TimerEnabled: True` sem nenhum bloco que o desligasse, e `TimerAlwaysFires` ausente no `.scm` (**padrão do App Inventor = True**). O timer continuava disparando `AtualizarPainel` a cada 2 s **enquanto o usuário estava no Screen3/Screen4**, onde `Label4`/`Label5`/etc. não existem. Depois do fix do `<next>` isso passaria a dar `Cannot find the component: Label4`. Correções:
   - `Button1.Click` (→Screen3) e `Button3.Click` (→Screen4) ganharam `set Clock1.TimerEnabled = false` **antes** do `open another screen` (`blkTM1`–`blkTM4`).
   - `Screen2.Initialize` e `Screen2.OtherScreenClosed` ganharam `set Clock1.TimerEnabled = true` como primeiro bloco (`blkTM5`–`blkTM8`).
   - `.scm`: `Clock1` recebeu `"TimerAlwaysFires": "False"` como segunda camada (necessária porque, no AI Companion, as telas dividem a mesma activity e o `onPause` não é confiável).
7. **Validação:** XML válido nas 4 telas · nenhum bloco perdido (18/229→237/97/32, os 8 novos são os do Clock) · ids únicos · **todo `<statement>`, `<value>` e `<next>` com exatamente 1 `<block>` filho** · JSON dos 4 `.scm` válido · ordem de execução conferida percorrendo a cadeia `next` · `.aia` rezipado e `aia_bytes.py` regenerado.
8. **Regra permanente:** ver itens 6 a 8 da seção 4.

### 3.10 Encerrar não funcionava: instante de data no TinyDB (sessão atual)
1. **Bug relatado:** selecionar a recarga no `ListPicker`, tocar em **Encerrar** e nada acontecer. Às vezes aparecia `The operation Duration cannot accept the arguments: ["java.util.GregorianCalendar[time=...]"], [java.util.GregorianCalendar[time=...]]`.
2. **A pista está nas aspas da mensagem:** o **1º** argumento vem entre aspas (`["java.util..."]`) — é **texto**; o **2º** não (`[java.util...]`) — é um instante de verdade. O `Clock1.Duration` exige dois instantes.
3. **Causa raiz:** o `Screen3` gravava o início da recarga como `Clock1.Now`, que é um **objeto de data** (`java.util.Calendar`). O **TinyDB só persiste texto, número, booleano e lista** — ele serializa o resto via `toString()`. Na volta, `recargasAtivas[i][3]` era a string `"java.util.GregorianCalendar[time=1786654040813,...]"`, e o `Duration` do `Screen2` recusava o argumento. Como o erro acontecia **antes** do `ShowAlert` de confirmação, a impressão era de que o botão não fazia nada.
4. **Correção:**
   - `Screen3` passou a gravar `Clock1.GetMillis(Clock1.Now)` — um **número** de milissegundos, que o TinyDB persiste sem perda (`blkMS1`, envolvendo o `blk290` original).
   - `Screen2` trocou o `Clock1.Duration` (`blk147`) por `math_subtract`: `GetMillis(Now) − inicio`.
   - **Guarda para registro antigo:** o subtraendo é um `controls_choose` — `se é número?(inicio) então inicio senão GetMillis(Now)`. Recarga gravada no formato velho encerra com duração 0 em vez de quebrar o app, e sai da lista de ativas. Autolimpa sem precisar apagar os dados do Companion.
5. **Verificação:** XML válido nas 4 telas · ids únicos (Screen2 237→243, Screen3 97→98) · todo `statement`/`value`/`next` com 1 bloco filho · nenhum `method_name="Duration"` restante · `.aia` rezipado e `aia_bytes.py` regenerado.
6. **Regra permanente:** ver item 10 da seção 4.

### 3.11 Histórico "vazio": texto branco em fundo branco (sessão atual)
1. **Bug relatado:** depois de encerrar com sucesso, o Screen4 não mostrava nada.
2. **Dedução antes de investigar:** no `Button2.Click` (Encerrar) o `StoreValue("historico")` vem **antes** do `StoreValue("recargasAtivas")`. Se a recarga saiu da lista de ativas, o histórico foi gravado. Logo o problema era de exibição, não de dados — e os blocos do Screen4 (`Screen4.Initialize` monta `exibicao` e joga em `ListView1.Elements`) estavam corretos.
3. **Causa raiz:** o componente `ListView` do App Inventor tem, de fábrica, **fundo preto e texto branco** (`DEFAULT_BACKGROUND_COLOR = COLOR_BLACK`, `DEFAULT_TEXT_COLOR = COLOR_WHITE`). O `.scm` definia `BackgroundColor: "&HFFFFFFFF"` e **não definia `TextColor`** — sobrou branco sobre branco. Os registros estavam na tela o tempo todo, ilegíveis. O `ListPicker1` do Screen2 tinha as duas cores definidas; o `ListView1` só uma.
4. **Correção:** `ListView1` (Screen4) recebeu `"TextColor": "&HFF212121"` e `"TextSize": "16"`.
5. **Regra permanente:** ver item 11 da seção 4.

### 3.12 `Cannot find the component: Label4` — o Clock esquecido do Screen3 (sessão atual)
1. **Bug relatado:** ao testar recarga perto do limite, o alerta por voz funcionou, mas passou a aparecer `Cannot find the component: Label4` repetindo.
2. **A correção de 3.9.6 estava intacta** (`Clock1.TimerEnabled = false` antes de abrir Screen3/Screen4, `true` no `Initialize`/`OtherScreenClosed`) — mas cobria só o Clock do **Screen2**.
3. **Causa raiz:** o **Screen3 tem um `Clock1` próprio**, e o `.scm` dele não definia **nenhuma** propriedade — valendo os padrões do App Inventor: `TimerEnabled: True`, `TimerInterval: 1000`, `TimerAlwaysFires: True`. O Screen3 usa o Clock apenas para carimbar a hora (`GetMillis`/`Now`); o timer estava ligado por acidente.
   Como o **App Inventor despacha eventos por nome de componente** e os dois relógios se chamam `Clock1`, o tique do Screen3 acionava o handler `Clock1.Timer` **do Screen2**, rodando `AtualizarPainel` com o Screen3 na frente — onde `Label4` não existe.
4. **A mensagem de erro confirma o mecanismo:** a falha para em `Label4`, o **primeiro componente visual** do `AtualizarPainel`. Tudo antes dele resolve porque não é componente visual da tela: `global total`/`nomes`/`limite`/`nomesAnt` são do Screen2 (capturados lexicamente pelo handler) e `TinyDB1` existe nas duas telas. Só a busca de componente visual passa pela tela ativa.
5. **Correção:** `Clock1` do Screen3 recebeu `"TimerEnabled": "False"` e `"TimerAlwaysFires": "False"`. Nada nos blocos.
6. **Segundo sintoma do mesmo relato — registro novo sumindo do histórico:** o Screen4 tinha `Scrollable: "True"` com `ListView1` de altura `Automatic` (`-2`). Numa tela rolável a altura disponível é ilimitada, então o `ListView` não consegue se medir nem rolar internamente: ele fixa um tamanho e **corta os itens seguintes** — os antigos aparecem, os novos não. Configuração correta aplicada: `Screen4.Scrollable: "False"`, `VerticalArrangement1.Height: "-1"` e `ListView1.Height: "-1"` (Fill parent), deixando o próprio `ListView` rolar por dentro.
7. **Regra permanente:** ver itens 12 e 13 da seção 4.

### 3.13 Formatação da linha do histórico (sessão atual)
1. **Motivo:** os números saíam crus — `18.000000001 kWh | 2.5083333 h` — e a potência não aparecia. Num teste de 2 minutos a linha virava um monte de zeros, ruim para a demonstração (UX/UI vale 20% da nota).
2. **Formato novo** (`text_join` `blk323` do Screen4, 8 → 11 itens):
   `Bia | 18.00 kWh | 2h 30min | 7.2 kW | 13/08/2026 20:45`
3. **Nada mudou no que é gravado.** A potência é **derivada** de `kWh ÷ horas` (matematicamente idêntica ao kW cadastrado, já que `kwh = kw × horas`). Guardar um 5º campo faria os registros antigos, de 4 campos, estourarem `select list item` — os registros existentes continuam funcionando sem migração.
4. **Detalhes que exigiram cuidado:**
   - **Minutos:** arredondar para minutos **antes** de separar h/min (`round(horas × 60)`, depois `floor(÷60)` e o resto). Fazendo `floor` na fração direto, uma recarga de 2 min (0,0333 h) sairia como `0h 1min`.
   - **Divisão por zero:** o registro legado tem `horas = 0`; a potência passa por um `controls_choose` (`se horas > 0 então kWh/horas senão 0`).
   - **Separadores em ASCII** (`|`), seguindo a convenção do resto do app, cujos textos não têm acento nenhum.
5. **Blocos usados** (nomes conferidos no fonte `blocklyeditor/src/blocks/math.js` do App Inventor, não de memória): `math_single` com `<field name="OP">` ∈ `ROUND`/`CEILING`/`FLOOR`, e `math_format_as_decimal` com `<value name="NUM">` e `<value name="PLACES">`.
6. **Armadilha encontrada no caminho:** a primeira versão gerou **ids duplicados** (`blkF30`, `blkF40`…) porque os ids eram montados por concatenação de índices. Trocado por contador sequencial — ver item 14 da seção 4.
7. **Verificação:** XML válido nas 4 telas · ids únicos (Screen4 32→75 blocos) · `mutation items="11"` batendo com os 11 `ADD` · todo `statement`/`value`/`next` com 1 bloco filho · `.bky` 100% ASCII · `aia_bytes.py` regenerado.

### 3.14 Botão voltar do celular saía do app (sessão atual)
1. **Bug relatado:** no Histórico, o botão voltar do aparelho fechava o aplicativo em vez de retornar ao painel.
2. **Descartado primeiro:** a suspeita de que o ajuste de layout de 3.12.6 tivesse empurrado o botão "Voltar" para fora da tela. Não é o caso — o App Inventor implementa Fill parent em arranjo vertical com **peso** (`ViewUtil.setChildHeightForVerticalLayout`: `height = 0; weight = 1`), então o `ListView` fica só com o espaço que sobra e o `Button1` continua visível.
3. **Causa raiz:** nenhuma tela tinha handler para o evento `BackPressed` do `Form`. Sem handler, o `Form.onBackPressed()` cai em `super.onBackPressed()` e quem decide o que acontece é o Android — não o app.
   ```java
   public void onBackPressed() {
     if (!BackPressed()) {                 // false quando nao ha handler
       AnimationUtil.ApplyCloseScreenAnimation(this, closeAnimType);
       super.onBackPressed();
     }
   }
   ```
4. **Correção:** `Screen3.BackPressed` e `Screen4.BackPressed` (`blkBP1`/`blkBP3`), cada um com um `controls_closeScreen`. Com o handler presente o `BackPressed()` devolve **true** e o `super.onBackPressed()` nunca roda — por isso o `close screen` dentro dele é obrigatório, senão o botão voltar não faria nada.
5. **Ganho secundário:** o botão voltar passa a fechar a tela pelo **mesmo caminho** do botão "Voltar" da tela, disparando o `OtherScreenClosed` do Screen2 — que é quem religa o `Clock1` (3.9.6). Antes, sair pelo botão do aparelho podia deixar o painel com o timer desligado, sem atualização automática.
6. **Screen1 e Screen2 ficaram sem handler de propósito:** voltar no login e no painel deve seguir o comportamento padrão do Android.
7. **Regra permanente:** ver item 15 da seção 4.

### 3.15 Renomeação de telas e componentes (sessão atual)
1. **Motivo:** os prints dos blocos vão para a documentação em LaTeX, e `Button2.Click` / `set Label4.Text` não explicam nada para quem corrige. Feito **antes** dos prints, de propósito — depois teriam que ser refeitos.
2. **50 componentes renomeados** (10 no Screen1, 21 no Painel, 13 no Cadastro, 6 no Historico) e **3 telas**: `Screen2`→`Painel`, `Screen3`→`Cadastro`, `Screen4`→`Historico`. Padrão: português sem acento, PascalCase, tipo na frente (`BotaoEncerrar`, `LabelKwEmUso`, `CampoPotencia`).
3. **`Screen1` continua `Screen1`** — é a tela principal (`main=` no `project.properties`) e o App Inventor não permite renomear.
4. **Renomear tela não existe na interface do AI2.** A recomendação da comunidade é criar tela nova, copiar componentes, copiar blocos pela BackPack e apagar a antiga. Aqui foi feito direto no `.aia`, que é mais seguro: renomear os arquivos `.scm`/`.bky`, o `$Name` do Form, o `instance_name`/`COMPONENT_SELECTOR` dos eventos de tela e o **texto** dos blocos `open another screen`.
5. **Ganho estrutural:** os dois `Clock1` homônimos (Screen2 e Screen3) viraram `RelogioPainel` e `RelogioCarimbo`. Como o App Inventor despacha eventos **por nome de componente**, era exatamente essa coincidência que causava o bug 3.12. Agora a classe do problema deixa de existir, em vez de depender de o timer estar desligado.
6. **Verificação:** JSON e XML válidos nas 4 telas · toda referência de bloco tem componente correspondente no designer · nenhum nome duplicado por tela · ids de bloco únicos · **nenhum nome genérico restante** (`Button\d+`, `Label\d+`, etc., exceto `Screen1`) · as 3 aberturas de tela apontam para telas que existem · `main=` e `lastopened=` intactos.
7. **Pendência conhecida:** o `_gerador/gerar_doc.py` (o gerador antigo, em reportlab) cita `Screen2`/`Screen3`/`Screen4` em 16 lugares e ficou desatualizado. Ele foi mantido por decisão do Henrique; o PDF novo será o LaTeX.
8. **Tabela de-para:** seção 6.

---

## 4. Aprendizados / armadilhas (IMPORTANTE para a próxima sessão)

1. **A pasta do projeto tem nome com normalização Unicode incomum:** no shell o diretório se chama `Programaçõa de Dispositivos Móveis` (com "õ" — aparece assim), e uma ferramenta de escrita que use a grafia "Programação..." cria uma **pasta duplicada**. Regra: para a pasta do projeto, **usar sempre `bash` com caminhos relativos `./`** a partir do diretório de trabalho; gravar arquivos em `/tmp` e `cp` para a pasta.
2. **O temp do opencode (`/var/folders/lj/.../opencode`) é apagado entre sessões.** Arquivos importantes devem morar na pasta do projeto.
3. **Editar arquivo sem antes ler dá erro silencioso** — a ferramenta de edição não persiste a mudança se o arquivo não foi lido antes. Sempre ler antes de editar.
4. **Saída do terminal pode vir corrompida** (linhas duplicadas). Padrão confiável: `python ... > arquivo.txt` e ler com a ferramenta de leitura em arquivos curtos.
5. **Heredocs no shell podem dar problema** com conteúdo grande/acentuado; preferir arquivos em `/tmp` + `cp`.
6. **NUNCA colocar blocos irmãos dentro de um `<statement>`** — o Blockly carrega **só o último** e descarta o resto sem avisar. Comandos em sequência se encadeiam com `<next>` aninhado (ver 3.9). Vale para `statement` e `value`: **exatamente 1 `<block>` filho direto em cada um**. Este foi o bug mais caro do projeto e a causa real de vários sintomas que foram atribuídos a build antigo.
7. **Não reserializar os `.bky` com um parser XML genérico** (`ElementTree`, `minidom`): as `mutation` declaram `xmlns="http://www.w3.org/1999/xhtml"` e o parser as reescreve com prefixo (`<ns1:mutation>`), o que faz o App Inventor **não reconhecer a mutation** e quebrar o bloco. Editar preservando o texto original das tags.
8. **`Clock` com `TimerEnabled` continua disparando em outras telas** (`TimerAlwaysFires` tem padrão **True**). Se o evento do timer mexe em componentes da tela, desligue o timer antes de `open another screen` e religue no `Initialize`/`OtherScreenClosed` — senão dá `Cannot find the component: X` a cada tick (ver 3.9.6).
10. **O TinyDB não guarda objeto de data.** Ele persiste texto, número, booleano e lista; qualquer outra coisa vira `toString()` e volta como string. Nunca grave `Clock1.Now` — grave `Clock1.GetMillis(Clock1.Now)` e calcule a diferença por subtração (ver 3.10). O sintoma é `Duration cannot accept the arguments`, com o argumento vindo do banco **entre aspas** na mensagem de erro.
11. **Ao mudar a cor de fundo de um componente, defina também a cor do texto.** O `ListView` nasce preto com texto branco; mudar só o fundo para branco deixa a lista invisível e parece "lista vazia" (ver 3.11). Vale para `ListView`, `ListPicker` e `Button`.
12. **Componente com o mesmo nome em telas diferentes é armadilha:** o App Inventor despacha eventos por **nome**, então o `Clock1` de uma tela pode acionar o handler `Clock1.Timer` de outra. Um `Clock` usado só para pegar a hora deve ter `TimerEnabled: "False"` explícito — o padrão do componente é **ligado**, a cada 1000 ms (ver 3.12). Ao auditar, liste as propriedades de **todos** os Clocks das 4 telas, não só o do Screen2.
13. **`ListView` não funciona em tela `Scrollable`.** Numa tela rolável a altura é ilimitada, o `ListView` não se mede nem rola por dentro, e itens somem sem erro nenhum. Use `Scrollable: "False"` na tela e `Height: "-1"` (Fill parent) no arranjo e no `ListView` (ver 3.12.6).
14. **Ao gerar blocos novos, use contador sequencial para os ids** (`blkF001`, `blkF002`…), nunca concatenação de índices — isso já produziu colisão silenciosa (ver 3.13.6). E **confira o nome do tipo de bloco no fonte do App Inventor** (`blocklyeditor/src/blocks/*.js`) antes de escrever, em vez de deduzir: tipo errado não dá erro de XML, o bloco só some.
15. **Toda tela secundária precisa de `BackPressed` → `close screen`.** Sem o handler, o botão voltar do aparelho cai no comportamento padrão do Android e pode sair do app; e a tela não fecha pelo caminho do bloco `close screen`, então o `OtherScreenClosed` da tela de origem não dispara — no Torre EV isso deixaria o `Clock1` do painel desligado (ver 3.14).
9. Validações que SEMPRE rodar após mexer no `.aia`: JSON dos `.scm`; XML dos `.bky` **com o namespace Blockly** (`root.iter('{%s}block' % NS)`); ids de blocos únicos por tela; todo `<value>` com exatamente 1 `<block>` filho (sem texto solto — ex.: `ARG1` do GetValue); presença de `"MaxValue": "22"`, "kW em uso de", `"TimerEnabled": "True"` e `"TimerInterval": "2000"` no Clock1; ausência de `TextBox3`/`Button4`; ausência de `NumbersOnly` no TextBox2; presença de `EhNumero` e de `limite` (não `22` fixo) na validação do Screen3; lógica `statusAnt`/`nomesAnt`; **nenhum `procedures_defreturn` com `<statement name="STACK">`** (usar `controls_do_then_return` — ver 3.7). Slider (Screen2): `Enabled: "True"`, `MinValue: "5"`, `MaxValue: "60"`, evento `PositionChanged` presente (mutation `event_name="PositionChanged"` + parâmetro `thumbValue`), e `AtualizarPainel` **sem** blocos de `set Slider1.MaxValue/Value` (ver 3.8).

---

## 5. Instruções para quem retomar o trabalho

1. **Importar:** App Inventor → Projetos → Importar projeto (.aia) → selecionar `TorreEV.aia`.
2. **Verificar:** abrir Screen2 → blocos → confirmar `AtualizarPainel`, a transição de status com `statusAnt` (persistente), o evento `Clock1.Timer` e o novo **`Slider1.PositionChanged`** (mover o slider muda o limite e o `Label6`); Screen3 → confirmar `EhNumero` e validação com `limite`; Screen4 → linha com " | kWh | h | ". Pode-se também verificar que `TextBox2` não tem `NumbersOnly`.
3. **Testar no celular:** AI Companion; fluxo: login (1234) → Nova Recarga → Salvar → voltar ao painel (Label4/vagas sobem) → **arrastar o Slider** (limite/`Label6` mudam e ficam salvos) → Encerrar → Histórico. Lembrar: **histórico só recebe registros no Encerrar**; salvar apenas adiciona à recarga ativa.
4. **Para testar sobrecarga:** cadastrar potências cuja soma ultrapasse 22 kW (ou reduzir `limiteKw` no TinyDB).
5. **Para editar a geração:** editar os arquivos em `_gerador` (bytes em `aia_bytes.py` são a fonte para o `.aia`; para mudar o app de verdade, editar o `.aia` no App Inventor e re-embutir os bytes).
6. **Re-embutir bytes após mudar o `.aia` no App Inventor:**
   ```python
   import zipfile, base64
   z = zipfile.ZipFile('TorreEV.aia')
   out = ['ARQUIVOS = {']
   for n in sorted(z.namelist()):
       out.append('    %r: %r,' % (n, base64.b64encode(z.read(n)).decode()))
   out.append('}')
   open('_gerador/aia_bytes.py', 'w').write('\n'.join(out))
   ```

---

## 6. Tabela de-para dos nomes (renomeação de 3.15)

As seções 3.1 a 3.14 citam os **nomes antigos** de propósito: elas registram o que estava
na tela quando cada bug aconteceu. Use esta tabela para traduzir.

### Telas

| Antes | Depois | Papel |
|---|---|---|
| `Screen1` | `Screen1` (não muda) | Login |
| `Screen2` | `Painel` | Dashboard do síndico |
| `Screen3` | `Cadastro` | Nova recarga |
| `Screen4` | `Historico` | Recargas encerradas |

### Screen1 — Login

| Antes | Depois |
|---|---|
| `VerticalArrangement1` | `LayoutLogin` |
| `Label1` | `TituloApp` |
| `Label2` | `SubtituloApp` |
| `Label3` | `EspacoTopo` |
| `Label5` | `RotuloSenha` |
| `TextBox1` | `CampoSenha` |
| `Button1` | `BotaoEntrar` |
| `Label4` | `LabelErro` |
| `TinyDB1` | `BancoLocal` |
| `Notifier1` | `Aviso` |

### Painel (ex-Screen2)

| Antes | Depois |
|---|---|
| `VerticalArrangement1` | `LayoutPainel` |
| `Label1` | `TituloPainel` |
| `Label2` | `StatusTexto` |
| `Label5` | `StatusDetalhe` |
| `Label8` / `Label10` | `Espaco1` / `Espaco2` |
| `Label9` | `RotuloCarga` |
| `Label4` | `LabelKwEmUso` |
| `Label6` | `LabelLimite` |
| `Label7` | `LabelVagas` |
| `Slider1` | `SliderLimite` |
| `ListPicker1` | `SeletorRecarga` |
| `HorizontalArrangement3` | `LinhaBotoes` |
| `Button1` | `BotaoNovaRecarga` |
| `Button2` | `BotaoEncerrar` |
| `Button3` | `BotaoHistorico` |
| `TinyDB1` | `BancoLocal` |
| `Notifier1` | `Aviso` |
| `TextToSpeech1` | `Voz` |
| `Clock1` | `RelogioPainel` |

`CardStatus`, `CardUso` e `CardAcoes` já tinham nome bom e não mudaram.

### Cadastro (ex-Screen3)

| Antes | Depois |
|---|---|
| `VerticalArrangement1` | `LayoutCadastro` |
| `Label1` | `TituloCadastro` |
| `CardCad` | `CardCadastro` |
| `Label2` | `RotuloNome` |
| `TextBox1` | `CampoNome` |
| `Label3` | `RotuloPotencia` |
| `TextBox2` | `CampoPotencia` |
| `Button1` | `BotaoSalvar` |
| `Button2` | `BotaoVoltar` |
| `TinyDB1` | `BancoLocal` |
| `Notifier1` | `Aviso` |
| `Clock1` | `RelogioCarimbo` |

### Historico (ex-Screen4)

| Antes | Depois |
|---|---|
| `VerticalArrangement1` | `LayoutHistorico` |
| `Label1` | `TituloHistorico` |
| `ListView1` | `ListaHistorico` |
| `Button1` | `BotaoVoltar` |
| `TinyDB1` | `BancoLocal` |

### Blocos citados nas seções 3.x

Os ids (`blk84`, `blk190`, `blk323`…) **não mudaram** — continuam válidos para localizar
um bloco no `.bky`. Só os nomes de componente dentro deles mudaram.
