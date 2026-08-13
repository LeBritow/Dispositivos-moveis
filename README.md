# Torre EV — Painel do Síndico

> **Aplicativo de gestão de recarga de veículos elétricos em condomínio**
> Desenvolvido com **MIT App Inventor 2** para a disciplina de **Programação de Dispositivos Móveis**.

---

## Sobre o projeto

O **Torre EV** é um painel de controle para o síndico acompanhar, em **tempo real**, a recarga de
veículos elétricos na garagem comum. Ele soma a potência (kW) das recargas ativas, compara com o
limite elétrico do condomínio e emite alertas visuais e sonoros quando o status muda — tudo sem
exigir obra na rede elétrica.

**Estudo de caso:** "Residencial Parque das Torres" — condomínio antigo (120 apartamentos, 240 vagas)
cuja rede foi dimensionada apenas para iluminação, portões e elevadores.

| Problema | Solução |
|---|---|
| Risco de sobrecarga na infraestrutura | Aviso automático de sobrecarga (visual + sonoro) |
| Falta de controle de uso | Painel atualizado sozinho a cada 2 segundos |
| Sem histórico para cobrança | Registro de kWh por morador no TinyDB |

---

## Funcionalidades

- **Login do síndico** — senha padrão `1234` (armazenada no TinyDB, alterável).
- **Painel em tempo real** — atualização automática a cada 2 s (`Clock1.Timer`); soma de kW em uso,
  limite, vagas ocupadas e barra de carga.
- **Semáforo de status** — verde / amarelo / vermelho com alerta (notificação + voz) **somente na
  mudança de estado** (sem notificações repetitivas).
- **Cadastro de recarga** — nome do morador + potência em kW, aceitando ponto **ou vírgula** como
  decimal (ex.: `7.2` ou `7,2`), com validação de dados e de capacidade.
- **Encerramento de recarga** — cálculo de kWh (potência × duração) com registro no histórico.
- **Histórico completo** — nome do morador, kWh consumido, **duração (h)** e data/hora.

### Regra do semáforo

| Status | Condição |
|---|---|
| 🟢 Verde | total em uso **menor que 80%** do limite |
| 🟡 Amarelo | total em uso **entre 80% e 100%** do limite |
| 🔴 Vermelho | total em uso **acima** do limite — sobrecarga (alerta sonoro) |

---

## Telas do aplicativo

| # | Tela | Função |
|---|---|---|
| 1 | **Screen1 — Login** | Protege o acesso ao painel com senha |
| 2 | **Screen2 — Painel** | Dashboard: status, kW em uso, limite, vagas, ações |
| 3 | **Screen3 — Cadastro** | Nova recarga com validação encadeada |
| 4 | **Screen4 — Histórico** | Lista das recargas encerradas |

**Navegação:** `Screen1 → Screen2` (login) · `Screen2 → Screen3` (nova recarga) · `Screen2 → Screen4` (histórico)

---

## Como usar

### 1. Importar o projeto

1. Acesse [ai2.appinventor.mit.edu](https://ai2.appinventor.mit.edu).
2. Clique em **Projetos → Importar projeto (.aia)**.
3. Selecione o arquivo **`TorreEV.aia`** deste repositório.

### 2. Testar no celular

1. No App Inventor, clique em **Conectar → AI Companion**.
2. No celular, abra o app **MIT AI2 Companion** e escaneie o QR code.
3. Faça login com a senha `1234` e teste o fluxo completo:

```
Login (1234) → Nova Recarga → Salvar → Painel (atualiza sozinho)
→ Encerrar → Histórico
```

> **Dica para testar a sobrecarga:** cadastre potências cuja soma ultrapasse o limite
> (22 kW) ou reduza o valor de `limiteKw` no TinyDB.

---

## Tecnologias

| Item | Detalhe |
|---|---|
| Plataforma | MIT App Inventor 2 (Blockly) |
| Linguagem gerada | YAIL (Kawa / Scheme) |
| Persistência | TinyDB (local no aparelho) |
| Multimídia | TextToSpeech (alertas por voz) |
| Sensores | Clock (data/hora e temporizador) |
| Versão | YaVersion 237 |

---

## Estrutura do repositório

```
├── TorreEV.aia                 # Projeto pronto para importar no App Inventor
├── Documentacao_TorreEV.pdf    # Documentação técnica (9 páginas)
├── Projeto_Carros_Eletricos.pdf# Edital / enunciado do desafio
├── CONTEXTO_PROJETO.md         # Histórico técnico completo das decisões e correções
└── _gerador/
    ├── aia_bytes.py            # Bytes exatos do .aia (base64)
    ├── gerar_aia.py            # Regenera o TorreEV.aia byte a byte
    └── gerar_doc.py            # Regenera a Documentacao_TorreEV.pdf
```

### Regenerando os artefatos

```bash
cd _gerador
python3 gerar_aia.py    # recria ../TorreEV.aia (byte idêntico)
python3 gerar_doc.py    # recria ../Documentacao_TorreEV.pdf
```

Dependências Python: `reportlab` (documentação) e bibliotecas padrão (`zipfile`, `base64`).

---

## Disciplina

**Programação de Dispositivos Móveis** — Projeto "Torre EV" · Painel do Síndico · MIT App Inventor 2
