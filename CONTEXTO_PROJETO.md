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

- **Package:** `appinventor.ai_gustavobrito170.TorreEV` · **Tela principal:** Screen1 · **YaVersion 237**
- **4 telas:**
  - **Screen1 — Login:** senha (padrão `1234`), TextBox com `Password: True`, botão Entrar, erro no Label1, Notifier.
  - **Screen2 — Painel:** cartões `CardStatus`/`CardUso`/`CardAcoes`, `Slider1` desabilitado como barra de carga, `Label4` (kW em uso), `Label6` (limite), `Label7` (vagas), `ListPicker1` (recargas ativas), botões Nova Recarga/Encerrar/Histórico, `Clock1` (Timer 2000 ms → `AtualizarPainel` automático), `TextToSpeech1`.
  - **Screen3 — Cadastro:** nome + kW (aceita ponto **ou vírgula** como decimal, ex. `7,2`), validação encadeada com `EhNumero(texto)` e limite **dinâmico** (`limite` do TinyDB), `CalcularTotal` (procedure com retorno).
  - **Screen4 — Histórico:** `ListView1` com nome, kWh, **duração (h)** e data.
- **TinyDB (tags):**
  - `senha` → padrão `"1234"`
  - `limiteKw` → padrão `22` (o limite do condomínio é **22 kW**, não 30)
  - `recargasAtivas` → lista de recargas `[nome, kw, duracao, inicio, dataInicio]`
  - `historico` → lista de recargas encerradas `[nome, kwh, horas, dataHoraFormatada]`

### Lógica-chave (Screen2)
- `AtualizarPainel` soma kW das ativas, atualiza labels + Slider; **rodada automaticamente a cada 2 s pelo `Clock1.Timer`** (TimerEnabled True, TimerInterval 2000).
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

---

## 4. Aprendizados / armadilhas (IMPORTANTE para a próxima sessão)

1. **A pasta do projeto tem nome com normalização Unicode incomum:** no shell o diretório se chama `Programaçõa de Dispositivos Móveis` (com "õ" — aparece assim), e uma ferramenta de escrita que use a grafia "Programação..." cria uma **pasta duplicada**. Regra: para a pasta do projeto, **usar sempre `bash` com caminhos relativos `./`** a partir do diretório de trabalho; gravar arquivos em `/tmp` e `cp` para a pasta.
2. **O temp do opencode (`/var/folders/lj/.../opencode`) é apagado entre sessões.** Arquivos importantes devem morar na pasta do projeto.
3. **Editar arquivo sem antes ler dá erro silencioso** — a ferramenta de edição não persiste a mudança se o arquivo não foi lido antes. Sempre ler antes de editar.
4. **Saída do terminal pode vir corrompida** (linhas duplicadas). Padrão confiável: `python ... > arquivo.txt` e ler com a ferramenta de leitura em arquivos curtos.
5. **Heredocs no shell podem dar problema** com conteúdo grande/acentuado; preferir arquivos em `/tmp` + `cp`.
6. Validações que SEMPRE rodar após mexer no `.aia`: JSON dos `.scm`; XML dos `.bky` **com o namespace Blockly** (`root.iter('{%s}block' % NS)`); ids de blocos únicos por tela; todo `<value>` com exatamente 1 `<block>` filho (sem texto solto — ex.: `ARG1` do GetValue); presença de `"MaxValue": "22"`, "kW em uso de", `"TimerEnabled": "True"` e `"TimerInterval": "2000"` no Clock1; ausência de `TextBox3`/`Button4`; ausência de `NumbersOnly` no TextBox2; presença de `EhNumero` e de `limite` (não `22` fixo) na validação do Screen3; lógica `statusAnt`/`nomesAnt`.

---

## 5. Instruções para quem retomar o trabalho

1. **Importar:** App Inventor → Projetos → Importar projeto (.aia) → selecionar `TorreEV.aia`.
2. **Verificar:** abrir Screen2 → blocos → confirmar `AtualizarPainel`, a transição de status com `statusAnt` (persistente) e o evento `Clock1.Timer`; Screen3 → confirmar `EhNumero` e validação com `limite`; Screen4 → linha com " | kWh | h | ". Pode-se também verificar que `TextBox2` não tem `NumbersOnly`.
3. **Testar no celular:** AI Companion; fluxo: login (1234) → Nova Recarga → Salvar → voltar ao painel → Encerrar → Histórico.
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
