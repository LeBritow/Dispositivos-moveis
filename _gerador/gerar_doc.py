# -*- coding: utf-8 -*-
# Gerador da Documentacao_TorreEV.pdf com layout limpo (reportlab).
# Uso: python3 gerar_doc.py   -> grava ../Documentacao_TorreEV.pdf
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, ListFlowable, ListItem, PageBreak)

PRIMARY = colors.HexColor('#0D47A1')
DARK = colors.HexColor('#002171')
GREY = colors.HexColor('#616161')
LGREY = colors.HexColor('#F5F5F5')
BORDER = colors.HexColor('#BDBDBD')
WHITE = colors.white

W, H = A4
ML = MR = 15 * mm
MT = 18 * mm
MB = 16 * mm
CW = W - ML - MR  # largura util (~510pt)

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Documentacao_TorreEV.pdf'))

ss = getSampleStyleSheet()

TITLE = ParagraphStyle('TITLE', parent=ss['Title'], fontSize=26, textColor=PRIMARY, alignment=1, leading=30, spaceAfter=14)
TSUB = ParagraphStyle('TSUB', parent=ss['Normal'], fontSize=13, textColor=DARK, alignment=1, leading=16, spaceAfter=2)
TSUB2 = ParagraphStyle('TSUB2', parent=ss['Normal'], fontSize=10.5, textColor=GREY, alignment=1, leading=15)
CELL = ParagraphStyle('CELL', parent=ss['Normal'], fontSize=8, leading=10.5, alignment=0, spaceAfter=0)
HEAD = ParagraphStyle('HEAD', parent=CELL, textColor=WHITE, fontName='Helvetica-Bold')
H2 = ParagraphStyle('H2', parent=ss['Heading2'], fontSize=12.5, textColor=WHITE, leading=16)
H3 = ParagraphStyle('H3', parent=ss['Heading3'], fontSize=11, textColor=DARK, spaceBefore=6, spaceAfter=3)
BODY = ParagraphStyle('BODY', parent=ss['Normal'], fontSize=9.5, leading=13.5, alignment=4, spaceAfter=4)
BUL = ParagraphStyle('BUL', parent=BODY, spaceAfter=3)
CODE = ParagraphStyle('CODE', parent=BODY, fontName='Courier', fontSize=8.2, leading=11, alignment=0, textColor=colors.HexColor('#263238'), spaceAfter=0)


def heading(t):
    return Table([[Paragraph(t, H2)]], colWidths=[CW],
                 style=TableStyle([
                     ('BACKGROUND', (0, 0), (-1, -1), PRIMARY),
                     ('LEFTPADDING', (0, 0), (-1, -1), 8),
                     ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                     ('TOPPADDING', (0, 0), (-1, -1), 5),
                     ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                 ]))


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(x, BUL), value='\u2022') for x in items],
        bulletType='bullet', start='\u2022', bulletFontName='Helvetica',
        bulletFontSize=9, bulletColor=PRIMARY, leftIndent=14)


def code_block(lines):
    body = '<br/>'.join(lines)
    t = Table([[Paragraph(body, CODE)]], colWidths=[CW],
              style=TableStyle([
                  ('BACKGROUND', (0, 0), (-1, -1), LGREY),
                  ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
                  ('LEFTPADDING', (0, 0), (-1, -1), 10),
                  ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                  ('TOPPADDING', (0, 0), (-1, -1), 7),
                  ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
              ]))
    return t


def bullets_styled(items):
    return bullets(items)


story = []

# ---------------- Capa ----------------
story.append(Spacer(1, 55 * mm))
story.append(Paragraph('TORRE EV', TITLE))
story.append(Paragraph('Painel do Síndico — Gestão de Recarga de Veículos Elétricos', TSUB))
story.append(Spacer(1, 3 * mm))
story.append(Table([[''], [''], ['']], colWidths=[CW],
                   style=TableStyle([
                       ('LINEBELOW', (0, 0), (-1, -1), 1, PRIMARY),
                       ('LINEBELOW', (0, 1), (-1, 1), 1, PRIMARY),
                       ('LINEBELOW', (0, 2), (-1, 2), 1, PRIMARY),
                   ])))
story.append(Spacer(1, 3 * mm))
story.append(Paragraph('Documentação Técnica do Projeto', TSUB))
story.append(Spacer(1, 8 * mm))
story.append(Paragraph('Estudo de Caso &amp; Desafio Prático<br/>Programação de Dispositivos Móveis<br/>Plataforma: MIT App Inventor', TSUB2))
story.append(Spacer(1, 22 * mm))
story.append(Paragraph('Integrantes: ____________________________________<br/>'
                       '____________________________________________________<br/>'
                       '____________________________________________________', BODY))
story.append(Spacer(1, 3 * mm))
story.append(Paragraph('Turma: ___________ &nbsp;&nbsp;&nbsp; Data: ___/___/______', BODY))
story.append(PageBreak())

# ---------------- Sumario ----------------
story.append(heading('Sumário'))
story.append(Spacer(1, 4))
for s in [
    '1. Definição do problema — dor resolvida e usuário final',
    '2. Visão geral da solução — funcionalidades e requisitos técnicos atendidos',
    '3. Telas da solução — estrutura, visual e navegação do aplicativo',
    '4. Diagrama de blocos — lógica do algoritmo no App Inventor',
    '5. Proposta de valor — por que a solução é eficiente para um condomínio antigo',
    '6. Roteiro de construção — passo a passo no MIT App Inventor',
]:
    story.append(Paragraph(s, BODY))
story.append(PageBreak())

# ---------------- 1 ----------------
story.append(heading('1. Definição do problema'))
story.append(Spacer(1, 4))
story.append(Paragraph('Contexto. A Residencial Parque das Torres é um condomínio antigo (construído no início dos anos 2000) com 120 apartamentos e 240 vagas de garagem. A rede elétrica foi dimensionada apenas para iluminação, portões e elevadores. Com a chegada de veículos elétricos (15 hoje, tendência de dobrar), a tentativa de recarga em tomadas comuns causou quedas de disjuntores, aumento da conta de energia e conflitos entre vizinhos.', BODY))
story.append(Paragraph('Dor específica escolhida (nicho): a incapacidade do síndico e da administração de monitorar e controlar as recargas na garagem comum. São três dores concretas dessa figura do condomínio:', BODY))
story.append(Spacer(1, 2))
story.append(bullets_styled([
    'Risco de sobrecarga na infraestrutura: medo de exceder o barramento principal, desligando elevadores e danificando equipamentos.',
    'Ausência de controle de uso: ninguém sabe quanto cada morador consome, nem quando há recargas simultâneas demais.',
    'Falta de histórico para cobrança: sem registro de kWh por morador, não há como cobrar com justiça pelo que cada um usou.',
]))
story.append(Spacer(1, 2))
story.append(Paragraph('Usuário final: o síndico do condomínio, que precisa de um painel simples de consulta e alerta no celular.', BODY))
story.append(PageBreak())

# ---------------- 2 ----------------
story.append(heading('2. Visão geral da solução'))
story.append(Spacer(1, 4))
story.append(Paragraph('O aplicativo Torre EV é um painel de controle para o síndico acompanhar, em tempo real, a situação da recarga de veículos elétricos na garagem comum. Ele soma a potência (kW) das recargas ativas, compara com o limite elétrico do condomínio e emite alertas visuais e sonoros apenas quando o status muda. O painel é atualizado automaticamente a cada 2 segundos (Clock1.Timer), sempre com os dados mais recentes do TinyDB. Todo o cadastro e o histórico ficam armazenados no TinyDB, não se perdendo ao fechar o app.', BODY))
story.append(Paragraph('Principais funcionalidades:', BODY))
story.append(Spacer(1, 2))
story.append(bullets_styled([
    'Login simples do síndico (senha padrão 1234, alterável via TinyDB) para acesso restrito ao painel.',
    'Cadastro de recarga: nome do morador e potência do carregador (kW), com validação de dados e de capacidade.',
    'Dashboard: soma automática de kW em uso, limite padrão de 22 kW, barra de carga e cartão de status com semáforo (verde/amarelo/vermelho); atualização automática a cada 2 segundos.',
    'Alertas por transição de status: notificação e voz somente quando o status muda (evita notificações repetitivas a cada segundo).',
    'Encerramento de recarga: cálculo de kWh (potência x duração) e registro no histórico com data/hora.',
    'Histórico de recargas em ListView, com nome do morador, kWh, duração e data.',
]))
story.append(Spacer(1, 2))
story.append(Paragraph('Requisitos técnicos atendidos (edital): condicional encadeada (se...senão), estruturas de repetição (para cada), procedimentos com retorno (função CalcularTotal), persistência local (TinyDB), armazenamento e manipulação de listas, componentes multimídia (TextoParaFala), sensores de data/hora (Clock) e design responsivo para celular.', BODY))
story.append(PageBreak())

# ---------------- 3 ----------------
story.append(heading('3. Telas da solução'))
story.append(Spacer(1, 4))
story.append(Paragraph('O aplicativo é organizado em 4 telas, garantindo navegação fluida e coerente. O visual usa cartões brancos sobre fundo cinza-claro, títulos e botões em azul-escuro (paleta #0D47A1/#002171) e destaque vermelho para situações de emergência.', BODY))
story.append(Spacer(1, 4))
tbl = Table([
    [Paragraph('Tela', HEAD), Paragraph('Função', HEAD), Paragraph('Componentes principais', HEAD)],
    [Paragraph('1. Screen1 (Login)', CELL), Paragraph('Protege o acesso ao painel. O síndico digita a senha; se correta, abre o dashboard.', CELL),
     Paragraph('CardLogin, TextBox1 (senha, Password), Button1 Entrar, Label1 (erro), Notifier1', CELL)],
    [Paragraph('2. Screen2 (Painel)', CELL), Paragraph('Tela central: cartão de status (verde/amarelo/vermelho), barra de carga, total em kW, limite, vagas e botões de ação.', CELL),
     Paragraph('CardStatus, CardUso, CardAcoes, Slider1 (barra de carga, desabilitado), ListPicker1 (recargas ativas), Buttons Nova Recarga/Encerrar/Histórico, Notifier1, TextToSpeech1, Clock1', CELL)],
    [Paragraph('3. Screen3 (Cadastro)', CELL), Paragraph('Registra nova recarga com validação de dados e de capacidade.', CELL),
     Paragraph('CardCad, TextBox1 (nome), TextBox2 (kW, aceita ponto ou vírgula), Button1 Salvar, Button2 Voltar, Notifier1', CELL)],
    [Paragraph('4. Screen4 (Histórico)', CELL), Paragraph('Lista o histórico de recargas encerradas.', CELL),
     Paragraph('CardHist, ListView1, Button1 Voltar', CELL)],
], colWidths=[30 * mm, 70 * mm, 74 * mm])
tbl.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LGREY]),
    ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(tbl)
story.append(Spacer(1, 6))
story.append(Paragraph('Navegação: Screen1 &gt; Screen2 (login) · Screen2 &gt; Screen3 (nova recarga) &gt; volta · Screen2 &gt; Screen4 (histórico) &gt; volta.', BODY))
story.append(PageBreak())

# ---------------- 4 ----------------
story.append(heading('4. Diagrama de blocos'))
story.append(Spacer(1, 4))
story.append(Paragraph('Os blocos abaixo descrevem o algoritmo implementado em cada tela, com destaque para a lógica condicional encadeada (se...então...senão), o procedimento com retorno e o uso do TinyDB. Os prints das telas de código devem ser anexados a esta seção após a construção do protótipo.', BODY))
story.append(Paragraph('4.1 Screen1 — verificação de senha', H3))
story.append(code_block([
    'when Screen1.Initialize',
    '    call TinyDB1.GetValue tag "senha" valueIfTagNotThere "1234"',
    'when Button1.Click',
    '    if TextBox1.Text = senha',
    '        then: open another screen "Screen2"',
    '        else: Notifier1.ShowAlert "Senha incorreta"',
]))
story.append(Paragraph('4.2 Screen2 — monitoramento com alerta por transição de status', H3))
story.append(code_block([
    'when Screen2.Initialize',
    '    global limite = TinyDB1.GetValue "limiteKw" valueIfTagNotThere 22',
    '    global rec = TinyDB1.GetValue "recargasAtivas" (lista vazia se nao houver)',
    '    call AtualizarPainel',
    'when Clock1.Timer  (a cada 2 segundos)',
    '    call AtualizarPainel   -> painel sempre atualizado',
    'procedure AtualizarPainel',
    '    total = soma dos valores kW das recargas ativas (funcao CalcularTotal)',
    '    Label4.Text = total + " kW em uso de " + limite + " kW"',
    '    Label6.Text = "Limite: " + limite + " kW"',
    '    Label7.Text = "Vagas ocupadas: " + length(rec)',
    '    Slider1.ThumbPosition = total',
    '    se nomes das recargas ativas mudou (nomes != nomesAnt)',
    '        entao: atualiza ListPicker.Elements e mantem a selecao atual',
    '    se total > limite (sobrecarga)',
    '        then: se statusAnt diferente de "sobrecarga"',
    '            CardStatus vermelho, Label2 "SOBRECARGA!", Notifier1.ShowAlert, TextToSpeech1.Speak',
    '    else if total >= 0.8 x limite (atencao)',
    '        then: se statusAnt diferente de "atencao"',
    '            CardStatus amarelo, Label2 "ATENCAO", Notifier1.ShowAlert, TextToSpeech1.Speak',
    '    else (ok)',
    '        then: se statusAnt diferente de "ok"',
    '            CardStatus verde, Label2 "OK", Notifier1.ShowAlert "Carga normal"',
    '    statusAnt recebe o novo status (so alerta na mudanca de estado)',
]))
story.append(Paragraph('Nova recarga: o botão abre a ListPicker com as recargas ativas; escolher uma e Encerrar remove da lista, calcula kWh = kW x duração (Clock1), guarda no TinyDB tag "historico" e atualiza o painel.', BODY))
story.append(PageBreak())

# ---------------- 4 cont ----------------
story.append(heading('4. Diagrama de blocos (continuação)'))
story.append(Spacer(1, 4))
story.append(Paragraph('4.3 Screen3 — cadastro com validação encadeada', H3))
story.append(code_block([
    'when Screen3.Initialize',
    '    global limite = TinyDB1.GetValue "limiteKw" valueIfTagNotThere 22',
    '    global recargas = TinyDB1.GetValue "recargasAtivas"',
    'when Button1.Click (Salvar)',
    '    if TextBox1.Text = ""',
    '        then: Notifier1.ShowAlert "Informe o nome do morador"',
    '    else if TextBox2.Text = "" ou NÃO(EhNumero(TextBox2.Text)) ou potência < 1 ou potência > limite',
    '        then: Notifier1.ShowAlert "Potencia invalida (1 a " + limite + " kW)"',
    '    else if (CalcularTotal(recargas) + potência) > limite',
    '        then: Notifier1.ShowAlert "Nao permitido: excederia o limite"',
    '    else',
    '        adiciona [nome, potência, duracao, inicio] em "recargasAtivas" (TinyDB)',
    '        Notifier1.ShowAlert "Recarga cadastrada"',
    '        open another screen "Screen2"',
    'procedure EhNumero(texto)',
    '    retorna (é número? texto) OU (é número? substitui "," por "." em texto)',
    '    -> aceita "7" e "7,2" como potências válidas',
    'procedure CalcularTotal(lista)',
    '    retorna a soma das potencias (2o item de cada sublista)',
]))
story.append(Spacer(1, 4))
story.append(Paragraph('4.4 Screen4 — exibição do histórico', H3))
story.append(code_block([
    'when Screen4.Initialize',
    '    global historico = TinyDB1.GetValue "historico"',
    '    for each item em historico:',
    '        monta linha "Morador: " + item(1) + " | " + item(2) + " kWh | "',
    '                      + item(3) + " h | " + item(4)',
    '        adiciona em exibicao',
    '    ListView1.Elements = exibicao',
]))
story.append(PageBreak())

# ---------------- 5 ----------------
story.append(heading('5. Proposta de valor'))
story.append(Spacer(1, 4))
story.append(bullets_styled([
    'Zero obra na rede elétrica: o condomínio de 20 anos não precisa de retrofit imediato no barramento. O app gerencia a demanda em kW e impede que as recargas ultrapassem o limite de 22 kW, reduzindo o risco de incêndio e de queda dos disjuntores.',
    'Prevenção de desastres e de conflitos: o alerta sonoro e visual de sobrecarga avisa o síndico em tempo real, permitindo ação imediata antes que os elevadores parem ou um cabo sobrecarregue o barramento.',
    'Transparência para todos os atores: com o histórico de kWh por morador registrado no TinyDB, o síndico consegue cobrar exatamente o que cada um consumiu — atendendo o desejo de "pagar pelo que usei".',
    'Usabilidade: interface com cartões, semáforo de status e alertas apenas na mudança de estado — simples o bastante para o síndico usar no dia a dia sem treinamento.',
]))
story.append(Spacer(1, 6))
story.append(Paragraph('Semáforo de status (regra de negócio):', H3))
story.append(bullets_styled([
    'Verde: total em uso menor que 80% do limite (22 kW).',
    'Amarelo: total em uso entre 80% e 100% do limite — atenção.',
    'Vermelho: total em uso acima do limite — sobrecarga (alerta sonoro).',
]))
story.append(PageBreak())

# ---------------- 6 ----------------
story.append(heading('6. Roteiro de construção no MIT App Inventor'))
story.append(Spacer(1, 4))
story.append(Paragraph('Passo a passo para montar o protótipo (ou importar o TorreEV.aia em "Importar projeto (.aia)"):', BODY))
story.append(Spacer(1, 2))
story.append(bullets_styled([
    '1. Criar o projeto e as 4 telas (Screen1 a Screen4); em "Propriedades da Tela", configurar Title e Screen1 como tela inicial.',
    '2. Na Screen1 (Login): TextBox1 (senha, Password marcado), Button1 Entrar, Label1 de erro e Notifier1. Implementar os blocos de 4.1.',
    '3. Na Screen2 (Painel): VerticalArrangements para os cartões CardStatus/CardUso/CardAcoes (BackgroundColor branco), Slider1 como barra de carga (Enabled desmarcado), ListPicker1, botões, Notifier1, TextToSpeech1, Clock1 e TinyDB1. Implementar 4.2.',
    '4. Na Screen3 (Cadastro): TextBox1 (nome), TextBox2 (kW, aceita ponto ou vírgula), Button1 Salvar, Button2 Voltar e Notifier1. Implementar 4.3.',
    '5. Na Screen4 (Histórico): ListView1, Button1 Voltar e carregar o histórico na Initialize. Implementar 4.4.',
    '6. Conectar o celular com o app AI Companion e testar o fluxo completo: login, cadastro, sobrecarga simulada e histórico.',
]))
story.append(Spacer(1, 6))
story.append(Paragraph('Dica: para testar o alerta de sobrecarga, cadastre recargas cuja soma ultrapasse 22 kW ou reduza temporariamente o valor em "limiteKw" no TinyDB.', BODY))


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(PRIMARY)
        canvas.setLineWidth(0.7)
        canvas.line(ML, H - MT + 8, W - MR, H - MT + 8)
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(GREY)
        canvas.drawString(ML, H - MT + 12, 'Documentação Técnica — Torre EV (Painel do Síndico)')
    if doc.page > 1:
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(GREY)
        canvas.drawCentredString(W / 2, 12 * mm, 'Página %d' % doc.page)
    canvas.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=ML, rightMargin=MR,
                        topMargin=MT, bottomMargin=MB, title='Torre EV - Documentação Técnica',
                        author='Programação de Dispositivos Móveis')
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print('PDF gerado:', OUT)
