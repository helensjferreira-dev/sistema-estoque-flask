from flask import Blueprint, render_template, jsonify, Response, session, request
from datetime import date, datetime, timedelta
from conn import conectar
from util.auth import login_required
from models.lotes import Lote
from services.produto_services import buscar_produto_por_id
from services.categoria_services import buscar_categoria_por_id
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
import io
import csv
import locale
import pytz



from openpyxl import Workbook

tz_brasilia = pytz.timezone("America/Sao_Paulo")

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

PDF_PRIMARY = colors.HexColor("#111827")
PDF_BORDER = colors.HexColor("#d9e2ec")
PDF_BG_LIGHT = colors.HexColor("#f8fafc")
PDF_DANGER = colors.HexColor("#991b1b")
PDF_WARNING = colors.HexColor("#92400e")
PDF_SUCCESS = colors.HexColor("#166534")


def adicionar_cabecalho_pdf(elementos, titulo_texto, styles):
    titulo_style = styles["Title"]
    titulo_style.textColor = PDF_PRIMARY
    titulo_style.fontSize = 20
    titulo_style.leading = 24

    normal_style = styles["Normal"]
    normal_style.alignment = TA_RIGHT
    normal_style.textColor = colors.HexColor("#334155")

    usuario = session.get("usuario", "Usuário não identificado")
    data_geracao = datetime.now(tz_brasilia).strftime("%d/%m/%Y %H:%M")

    elementos.append(Paragraph(titulo_texto, titulo_style))
    elementos.append(
        Paragraph(f"Gerado em {data_geracao} por {usuario}", normal_style)
    )
    elementos.append(Spacer(1, 18))

def adicionar_resumo_pdf(elementos, styles, itens):
    resumo_style = ParagraphStyle(
        "ResumoPDF",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#64748b"),
    )

    partes = []

    for label, valor in itens:
        partes.append(
            f'<font color="#334155"><b>{label}:</b></font> {valor}'
        )

    resumo_texto = " &nbsp;&nbsp;|&nbsp;&nbsp; ".join(partes)

    elementos.append(Spacer(1, 14))
    elementos.append(Paragraph(resumo_texto, resumo_style))


def estilo_tabela_pdf():
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PDF_PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, PDF_BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PDF_BG_LIGHT]),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
    ])

relatorio_routes = Blueprint('relatorio_routes', __name__)


@relatorio_routes.route('/relatorio/validade')
@login_required
def validade():
    return render_template("validade.html")


@relatorio_routes.route('/relatorio/validade/dados')
def validade_dados():
    from datetime import datetime

    hoje_brasilia = datetime.now(tz_brasilia).date()

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT l.idlote, l.numero, l.quantidade, l.data_validade, p.nome AS produto_nome, c.nome AS categoria_nome
        FROM LOTE l
        JOIN PRODUTO p ON l.idproduto = p.idproduto
        LEFT JOIN CATEGORIA c ON p.idcategoria = c.idcategoria
        WHERE l.quantidade > 0
        ORDER BY l.data_validade ASC
    """)
    rows = cur.fetchall()
    cur.close()

    dados = []
    for idlote, numero, quantidade, data_validade, produto_nome, categoria_nome in rows:
        dias_restantes = (data_validade - hoje_brasilia).days

        if dias_restantes <= 0:
            status = "Vencido"
        elif dias_restantes <= 30:
            status = "Próximo"
        else:
            status = "OK"

        dados.append({
            "id": idlote,
            "numero": numero,
            "quantidade": quantidade,
            "validade": data_validade.strftime("%d/%m/%Y"),
            "produto_nome": produto_nome,
            "categoria_nome": categoria_nome or "-",
            "dias_restantes": dias_restantes,
            "status": status
        })

    return jsonify({"dados": dados})




@relatorio_routes.route('/relatorio/estoque')
@login_required
def estoque():
    sql = """
        SELECT 
            P.IDPRODUTO,
            P.NOME AS produto_nome,
            C.NOME AS categoria_nome,
            P.ESTOQUE_MINIMO,
            COALESCE(SUM(
                CASE 
                    WHEN M.TIPO = 'entrada' THEN M.QUANTIDADE
                    WHEN M.TIPO = 'saida'   THEN -M.QUANTIDADE
                    ELSE 0
                END
            ), 0) AS estoque_atual
        FROM PRODUTO P
        LEFT JOIN CATEGORIA C ON C.IDCATEGORIA = P.IDCATEGORIA
        LEFT JOIN LOTE L ON L.IDPRODUTO = P.IDPRODUTO
        LEFT JOIN MOVIMENTACAO M ON M.IDLOTE = L.IDLOTE
        GROUP BY P.IDPRODUTO, P.NOME, C.NOME, P.ESTOQUE_MINIMO
        ORDER BY P.IDPRODUTO
    """
    conn = conectar()
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()

    dados = []
    for row in rows:
        idproduto, nome, categoria_nome, estoque_minimo, estoque_atual = row

        dados.append({
            "produto_id": idproduto,
            "produto_nome": nome,
            "categoria_nome": categoria_nome,
            "estoque_minimo": estoque_minimo,
            "estoque_atual": estoque_atual
        })

    return render_template("estoque.html", dados=dados)


@relatorio_routes.route('/relatorio/estoque/dados')
def estoque_dados():
    sql = """
        SELECT 
            P.IDPRODUTO,
            P.NOME AS produto_nome,
            C.NOME AS categoria_nome,
            P.ESTOQUE_MINIMO,
            COALESCE(SUM(
                CASE 
                    WHEN M.TIPO = 'entrada' THEN M.QUANTIDADE
                    WHEN M.TIPO = 'saida'   THEN -M.QUANTIDADE
                    ELSE 0
                END
            ), 0) AS estoque_atual
        FROM PRODUTO P
        LEFT JOIN CATEGORIA C ON C.IDCATEGORIA = P.IDCATEGORIA
        LEFT JOIN LOTE L ON L.IDPRODUTO = P.IDPRODUTO
        LEFT JOIN MOVIMENTACAO M ON M.IDLOTE = L.IDLOTE
        GROUP BY P.IDPRODUTO, P.NOME, C.NOME, P.ESTOQUE_MINIMO
        ORDER BY P.IDPRODUTO
    """
    conn = conectar()
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()

    dados = []
    for row in rows:
        idproduto, nome, categoria_nome, estoque_minimo, estoque_atual = row

        dados.append({
            "produto_id": idproduto,
            "produto_nome": nome,
            "categoria_nome": categoria_nome,
            "estoque_minimo": estoque_minimo,
            "estoque_atual": estoque_atual
        })

    return jsonify({"dados": dados})



@relatorio_routes.route('/relatorio/validade/export/csv')
def export_validade_csv():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT l.idlote, l.numero, l.quantidade, l.data_validade, p.nome, c.nome
        FROM LOTE l
        JOIN PRODUTO p ON l.idproduto = p.idproduto
        LEFT JOIN CATEGORIA c ON p.idcategoria = c.idcategoria
        WHERE l.quantidade > 0
        ORDER BY l.data_validade ASC
    """)
    rows = cur.fetchall()
    cur.close()

    dados = []
    for row in rows:
        dias_restantes = (row[3] - datetime.now(tz_brasilia).date()).days
        # Define status
        if dias_restantes <= 0:
            status = "Vencido"
        elif dias_restantes <= 30:
            status = "Próximo"
        else:
            status = "OK"

        dados.append({
            "id": row[0],
            "numero": row[1],
            "quantidade": row[2],
            "validade": row[3].strftime("%d/%m/%Y"),
            "produto_nome": row[4],
            "categoria_nome": row[5] or "-",
            "dias_restantes": dias_restantes,
            "status": status
        })

    # Resumo
    total_lotes = len(dados)
    vencidos = sum(1 for l in dados if l["dias_restantes"] <= 0)
    proximos = sum(1 for l in dados if 0 < l["dias_restantes"] <= 30)

    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")  # separador ; para abrir bem no Excel
    writer.writerow(["ID", "Produto", "Categoria", "Lote", "Quantidade", "Validade", "Dias restantes", "Status"])
    for l in dados:
        writer.writerow([
            l["id"], l["produto_nome"], l["categoria_nome"], l["numero"],
            l["quantidade"], l["validade"], l["dias_restantes"], l["status"]
        ])

    # Resumo no final
    writer.writerow([])
    writer.writerow([f"Total de lotes: {total_lotes}"])
    writer.writerow([f"Vencidos: {vencidos}"])
    writer.writerow([f"Próximos do vencimento (≤30 dias): {proximos}"])

    return Response(output.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=validade.csv"})



@relatorio_routes.route('/relatorio/validade/export/pdf')
def export_validade_pdf():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT l.idlote, l.numero, l.quantidade, l.data_validade, p.nome, c.nome
        FROM LOTE l
        JOIN PRODUTO p ON l.idproduto = p.idproduto
        LEFT JOIN CATEGORIA c ON p.idcategoria = c.idcategoria
        WHERE l.quantidade > 0
        ORDER BY l.data_validade ASC
    """)
    rows = cur.fetchall()
    cur.close()

    dados = []

    for row in rows:
        dias_restantes = (row[3] - datetime.now(tz_brasilia).date()).days

        if dias_restantes <= 0:
            status = "Vencido"
        elif dias_restantes <= 30:
            status = "Próximo"
        else:
            status = "OK"

        dados.append({
            "id": row[0],
            "numero": row[1],
            "quantidade": row[2],
            "validade": row[3].strftime("%d/%m/%Y"),
            "produto_nome": row[4],
            "categoria_nome": row[5] or "-",
            "dias_restantes": dias_restantes,
            "status": status
        })

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elementos = []

    adicionar_cabecalho_pdf(
        elementos,
        "Relatório de Validade",
        styles
    )

    tabela_dados = [
        ["ID", "Produto", "Categoria", "Lote", "Quantidade", "Validade", "Dias restantes", "Status"]
    ]

    for l in dados:
        status = l["status"]

        if status == "Vencido":
            status_pdf = "● Vencido"
        elif status == "Próximo":
            status_pdf = "● Próximo"
        else:
            status_pdf = "● OK"

        tabela_dados.append([
            l["id"],
            l["produto_nome"],
            l["categoria_nome"],
            l["numero"],
            l["quantidade"],
            l["validade"],
            l["dias_restantes"],
            status_pdf
        ])

    tabela = Table(tabela_dados, repeatRows=1)
    estilo = estilo_tabela_pdf()

    for i, l in enumerate(dados, start=1):
        if l["status"] == "Vencido":
            estilo.add("TEXTCOLOR", (6, i), (7, i), PDF_DANGER)
        elif l["status"] == "Próximo":
            estilo.add("TEXTCOLOR", (6, i), (7, i), PDF_WARNING)
        else:
            estilo.add("TEXTCOLOR", (6, i), (7, i), PDF_SUCCESS)

    tabela.setStyle(estilo)
    elementos.append(tabela)

    total_lotes = len(dados)
    vencidos = sum(1 for l in dados if l["status"] == "Vencido")
    proximos = sum(1 for l in dados if l["status"] == "Próximo")

    adicionar_resumo_pdf(
        elementos,
        styles,
        [
            ("Total de lotes", total_lotes),
            ("Vencidos", vencidos),
            ("Próximos", proximos),
        ],
    )

    doc.build(elementos)
    buffer.seek(0)

    return Response(
        buffer,
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment;filename=validade.pdf"}
    )

@relatorio_routes.route('/relatorio/validade/export/xlsx')
def export_validade_xlsx():
    import xlsxwriter
    from datetime import datetime
    import io

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT l.idlote, l.numero, l.quantidade, l.data_validade, p.nome, c.nome
        FROM LOTE l
        JOIN PRODUTO p ON l.idproduto = p.idproduto
        LEFT JOIN CATEGORIA c ON p.idcategoria = c.idcategoria
        WHERE l.quantidade > 0
        ORDER BY l.data_validade ASC
    """)
    rows = cur.fetchall()
    cur.close()

    dados = []
    for row in rows:
        dias_restantes = (row[3] - datetime.now(tz_brasilia).date()).days
        if dias_restantes <= 0:
            status = "Vencido"
        elif dias_restantes <= 30:
            status = "Próximo"
        else:
            status = "OK"

        dados.append({
            "id": row[0],
            "numero": row[1],
            "quantidade": row[2],
            "validade": row[3],  
            "produto_nome": row[4],
            "categoria_nome": row[5] or "-",
            "dias_restantes": dias_restantes,
            "status": status
        })

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Validade")

    # Formatos
    header_format = workbook.add_format({'bold': True, 'bg_color': '#1a2a4f', 'color': 'white', 'align': 'center'})
    alerta_format = workbook.add_format({'bg_color': '#f8d7da', 'color': '#721c24', 'align': 'center'})
    proximos_format = workbook.add_format({'bg_color': '#fff3cd', 'color': '#856404', 'align': 'center'})
    ok_format = workbook.add_format({'color': 'green', 'align': 'center'})
    normal_format = workbook.add_format({'align': 'center'})
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy', 'align': 'center'})

    # Cabeçalho
    headers = ["ID", "Produto", "Categoria", "Lote", "Quantidade", "Validade", "Dias restantes", "Status"]
    for col, h in enumerate(headers):
        worksheet.write(0, col, h, header_format)

    # Dados
    for row, l in enumerate(dados, start=1):
        worksheet.write(row, 0, l["id"], normal_format)
        worksheet.write(row, 1, l["produto_nome"], normal_format)
        worksheet.write(row, 2, l["categoria_nome"], normal_format)
        worksheet.write(row, 3, l["numero"], normal_format)
        worksheet.write(row, 4, l["quantidade"], normal_format)
        worksheet.write_datetime(row, 5, l["validade"], date_format)

        # Dias restantes + status com cores
        if l["status"] == "Vencido":
            worksheet.write(row, 6, l["dias_restantes"], alerta_format)
            worksheet.write(row, 7, l["status"], alerta_format)
        elif l["status"] == "Próximo":
            worksheet.write(row, 6, l["dias_restantes"], proximos_format)
            worksheet.write(row, 7, l["status"], proximos_format)
        else:
            worksheet.write(row, 6, l["dias_restantes"], ok_format)
            worksheet.write(row, 7, l["status"], ok_format)

    # Resumo gerencial
    total_lotes = len(dados)
    vencidos = sum(1 for l in dados if l["status"] == "Vencido")
    proximos = sum(1 for l in dados if l["status"] == "Próximo")

    resumo_row = len(dados) + 2
    worksheet.write(resumo_row, 0, f"Total de lotes: {total_lotes}")
    worksheet.write(resumo_row + 1, 0, f"Vencidos: {vencidos}")
    worksheet.write(resumo_row + 2, 0, f"Próximos do vencimento (≤30 dias): {proximos}")

    workbook.close()
    output.seek(0)

    return Response(output.read(),
                    mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers={"Content-Disposition": "attachment;filename=validade.xlsx"})




@relatorio_routes.route('/relatorio/estoque/export/csv')
def export_estoque_csv():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            P.IDPRODUTO,
            COALESCE(SUM(
                CASE 
                    WHEN M.TIPO = 'entrada' THEN M.QUANTIDADE
                    WHEN M.TIPO = 'saida'   THEN -M.QUANTIDADE
                    ELSE 0
                END
            ), 0) AS estoque_atual
        FROM PRODUTO P
        LEFT JOIN LOTE L ON L.IDPRODUTO = P.IDPRODUTO
        LEFT JOIN MOVIMENTACAO M ON M.IDLOTE = L.IDLOTE
        GROUP BY P.IDPRODUTO
        ORDER BY P.IDPRODUTO
    """)
    rows = cur.fetchall()
    cur.close()

    dados = []
    for row in rows:
        idproduto, estoque_atual = row[0], row[1]
        produto, _ = buscar_produto_por_id(idproduto)
        categoria = None
        if produto and produto.get("idcategoria"):
            categoria, _ = buscar_categoria_por_id(produto["idcategoria"])

        # Normalizar valores
        estoque_minimo = produto.get("estoque_minimo") if produto else 0
        estoque_minimo = estoque_minimo if estoque_minimo is not None else 0
        estoque_atual = int(estoque_atual) if estoque_atual is not None else 0

        dados.append({
            "produto_id": idproduto,
            "produto_nome": produto.get("nome") if produto else "não encontrado",
            "categoria_nome": categoria.get("nome") if categoria else "não encontrado",
            "estoque_minimo": estoque_minimo,
            "estoque_atual": estoque_atual
        })

    # Calcular resumo
    total_produtos = len(dados)
    em_falta = sum(1 for item in dados if item["estoque_atual"] == 0)
    baixos = sum(
        1 for item in dados
        if item["estoque_atual"] > 0 and item["estoque_atual"] < item["estoque_minimo"]
    )
    ok = total_produtos - em_falta - baixos

    # Gerar CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Produto", "Categoria", "Estoque Mínimo", "Estoque Atual", "Status"])
    for item in dados:
        if item["estoque_atual"] == 0:
            status = "Em falta"
        elif item["estoque_atual"] < item["estoque_minimo"]:
            status = "Baixo"
        else:
            status = "OK"
        writer.writerow([
            item["produto_id"], item["produto_nome"], item["categoria_nome"],
            item["estoque_minimo"], item["estoque_atual"], status
        ])

    # Adicionar resumo no final
    writer.writerow([])
    writer.writerow([f"Total de produtos: {total_produtos}"])
    writer.writerow([f"Em falta: {em_falta}"])
    writer.writerow([f"Baixo: {baixos}"])
    writer.writerow([f"OK: {ok}"])

    return Response(output.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=estoque.csv"})



@relatorio_routes.route('/relatorio/estoque/export/pdf')
def export_estoque_pdf():

    sql = """
        SELECT 
            P.IDPRODUTO,
            COALESCE(SUM(
                CASE 
                    WHEN M.TIPO = 'entrada' THEN M.QUANTIDADE
                    WHEN M.TIPO = 'saida'   THEN -M.QUANTIDADE
                    ELSE 0
                END
            ), 0) AS estoque_atual
        FROM PRODUTO P
        LEFT JOIN LOTE L ON L.IDPRODUTO = P.IDPRODUTO
        LEFT JOIN MOVIMENTACAO M ON M.IDLOTE = L.IDLOTE
        GROUP BY P.IDPRODUTO
        ORDER BY P.IDPRODUTO
    """
    conn = conectar()
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()

    dados = []
    for row in rows:
        idproduto, estoque_atual = row[0], row[1]
        produto, _ = buscar_produto_por_id(idproduto)
        categoria = None
        if produto and produto.get("idcategoria"):
            categoria, _ = buscar_categoria_por_id(produto["idcategoria"])

        # Normalizar valores
        estoque_minimo = produto.get("estoque_minimo") if produto else 0
        estoque_minimo = estoque_minimo if estoque_minimo is not None else 0
        estoque_atual = int(estoque_atual) if estoque_atual is not None else 0

        dados.append({
            "produto_id": idproduto,
            "produto_nome": produto.get("nome") if produto else "não encontrado",
            "categoria_nome": categoria.get("nome") if categoria else "não encontrado",
            "estoque_minimo": estoque_minimo,
            "estoque_atual": estoque_atual
        })

    # Buffer PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()
    elementos = []

    # Cabeçalho
    adicionar_cabecalho_pdf(elementos, "Relatório de Estoque", styles)


    # Tabela
    tabela_dados = [["ID", "Produto", "Categoria", "Estoque Mínimo", "Estoque Atual", "Status"]]
    for item in dados:
        if item["estoque_atual"] == 0:
            status =  "● Em falta"
        elif (item["estoque_minimo"] > 0 and item["estoque_atual"] < item["estoque_minimo"]):
            status =  "● Baixo"
        else:
            status = "● OK"

        tabela_dados.append([
            item["produto_id"],
            item["produto_nome"],
            item["categoria_nome"],
            item["estoque_minimo"],
            item["estoque_atual"],
            status
        ])

    tabela = Table(tabela_dados, repeatRows=1)
    estilo = estilo_tabela_pdf()

    # Destaque em vermelho para estoque baixo
    for i, item in enumerate(dados, start=1):
        if item["estoque_atual"] == 0:
            estilo.add("TEXTCOLOR", (4, i), (5, i), PDF_DANGER)

        elif (
            item["estoque_minimo"] > 0
            and item["estoque_atual"] < item["estoque_minimo"]
        ):
            estilo.add("TEXTCOLOR", (4, i), (5, i), PDF_WARNING)

        else:
            estilo.add("TEXTCOLOR", (4, i), (5, i), PDF_SUCCESS)

    tabela.setStyle(estilo)
    elementos.append(tabela)

    elementos.append(Spacer(1, 20))

    # Resumo gerencial
    total_produtos = len(dados)
    em_falta = sum(1 for item in dados if item["estoque_atual"] == 0)
    baixos = sum(1 for item in dados if item["estoque_atual"] > 0 and item["estoque_atual"] < item["estoque_minimo"])
    ok = total_produtos - em_falta - baixos

    perc_falta = (em_falta / total_produtos * 100) if total_produtos > 0 else 0
    perc_baixo = (baixos / total_produtos * 100) if total_produtos > 0 else 0

    adicionar_resumo_pdf(
    elementos,
    styles,
    [
        ("Total de produtos", total_produtos),
        ("Em falta", f"{em_falta} ({perc_falta:.1f}%)"),
        ("Baixo", f"{baixos} ({perc_baixo:.1f}%)"),
        ("OK", ok),
    ],
)

    doc.build(elementos)
    buffer.seek(0)

    return Response(buffer, mimetype='application/pdf',
                    headers={"Content-Disposition": "attachment;filename=estoque.pdf"})


@relatorio_routes.route('/relatorio/estoque/export/xlsx')
def export_estoque_xlsx():
    import xlsxwriter
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            P.IDPRODUTO,
            COALESCE(SUM(
                CASE 
                    WHEN M.TIPO = 'entrada' THEN M.QUANTIDADE
                    WHEN M.TIPO = 'saida'   THEN -M.QUANTIDADE
                    ELSE 0
                END
            ), 0) AS estoque_atual
        FROM PRODUTO P
        LEFT JOIN LOTE L ON L.IDPRODUTO = P.IDPRODUTO
        LEFT JOIN MOVIMENTACAO M ON M.IDLOTE = L.IDLOTE
        GROUP BY P.IDPRODUTO
        ORDER BY P.IDPRODUTO
    """)
    rows = cur.fetchall()
    cur.close()

    dados = []
    for row in rows:
        idproduto, estoque_atual = row[0], row[1]
        produto, _ = buscar_produto_por_id(idproduto)
        categoria = None
        if produto and produto.get("idcategoria"):
            categoria, _ = buscar_categoria_por_id(produto["idcategoria"])

        # Normalizar valores
        estoque_minimo = produto.get("estoque_minimo") if produto else 0
        estoque_minimo = estoque_minimo if estoque_minimo is not None else 0
        estoque_atual = int(estoque_atual) if estoque_atual is not None else 0

        dados.append({
            "produto_id": idproduto,
            "produto_nome": produto.get("nome") if produto else "não encontrado",
            "categoria_nome": categoria.get("nome") if categoria else "não encontrado",
            "estoque_minimo": estoque_minimo,
            "estoque_atual": estoque_atual
        })

    # Criar arquivo em memória
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Estoque")

    # Formatos
    header_format = workbook.add_format({'bold': True, 'bg_color': '#1a2a4f', 'color': 'white', 'align': 'center'})
    alerta_format = workbook.add_format({'bg_color': '#f8d7da', 'color': '#721c24'})
    ok_format = workbook.add_format({'bg_color': '#d4edda', 'color': '#155724'})
    normal_format = workbook.add_format({'align': 'center'})

    # Cabeçalho
    headers = ["ID", "Produto", "Categoria", "Estoque Mínimo", "Estoque Atual", "Status"]
    for col, h in enumerate(headers):
        worksheet.write(0, col, h, header_format)

    # Dados
    for row, item in enumerate(dados, start=1):
        if item["estoque_atual"] == 0:
            status = "Em falta"
            worksheet.write(row, 4, item["estoque_atual"], alerta_format)
            worksheet.write(row, 5, status, alerta_format)
        elif item["estoque_atual"] < item["estoque_minimo"]:
            status = "Baixo"
            worksheet.write(row, 4, item["estoque_atual"], alerta_format)
            worksheet.write(row, 5, status, alerta_format)
        else:
            status = "OK"
            worksheet.write(row, 4, item["estoque_atual"], ok_format)
            worksheet.write(row, 5, status, ok_format)

        worksheet.write(row, 0, item["produto_id"], normal_format)
        worksheet.write(row, 1, item["produto_nome"], normal_format)
        worksheet.write(row, 2, item["categoria_nome"], normal_format)
        worksheet.write(row, 3, item["estoque_minimo"], normal_format)

    # Resumo
    total_produtos = len(dados)
    em_falta = sum(1 for item in dados if item["estoque_atual"] == 0)
    baixos = sum(1 for item in dados if item["estoque_atual"] > 0 and item["estoque_atual"] < item["estoque_minimo"])
    ok = total_produtos - em_falta - baixos

    worksheet.write(len(dados)+2, 0, f"Total de produtos: {total_produtos}")
    worksheet.write(len(dados)+3, 0, f"Em falta: {em_falta}")
    worksheet.write(len(dados)+4, 0, f"Baixo: {baixos}")
    worksheet.write(len(dados)+5, 0, f"OK: {ok}")

    workbook.close()
    output.seek(0)

    return Response(output.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers={"Content-Disposition": "attachment;filename=estoque.xlsx"})

@relatorio_routes.route('/relatorio/movimentacoes/pagina')
@login_required
def pagina_relatorio_movimentacoes():
    return render_template("rel_movimentacao.html")


@relatorio_routes.route('/relatorio/movimentacoes')
@login_required
def relatorio_movimentacoes():
    from datetime import date, datetime, timedelta
    import pytz

    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")
    produto = request.args.get("produto")
    tipo = request.args.get("tipo")
    usuario = request.args.get("usuario")

    # Se não vier filtro de datas, define últimos 30 dias
    if not data_inicio or not data_fim:
        hoje = date.today()
        data_fim = hoje.isoformat()
        data_inicio = (hoje - timedelta(days=30)).isoformat()

    conn = conectar()
    cur = conn.cursor()

    sql = """
        SELECT m.IDMOVIMENTACAO, m.DATA_MOVIMENTOCAO, m.TIPO, m.QUANTIDADE, m.VALOR_UNITARIO,
               m.MOTIVO, p.NOME AS PRODUTO, c.NOME AS CATEGORIA, u.NOME AS USUARIO,
               l.IDLOTE, COALESCE(l.QUANTIDADE,0) AS ESTOQUE_LOTE
        FROM MOVIMENTACAO m
        JOIN LOTE l ON l.IDLOTE = m.IDLOTE
        JOIN PRODUTO p ON p.IDPRODUTO = l.IDPRODUTO
        JOIN CATEGORIA c ON c.IDCATEGORIA = p.IDCATEGORIA
        JOIN USUARIO u ON u.IDUSUARIO = m.IDUSUARIO
        WHERE m.DATA_MOVIMENTOCAO BETWEEN %s AND %s
    """

    params = [data_inicio, data_fim]

    if produto:
        sql += " AND p.NOME ILIKE %s"
        params.append(f"%{produto}%")
    if tipo:
        sql += " AND m.TIPO = %s"
        params.append(tipo)
    if usuario:
        sql += " AND u.NOME ILIKE %s"
        params.append(f"%{usuario}%")

    sql += " ORDER BY m.DATA_MOVIMENTOCAO DESC"

    cur.execute(sql, tuple(params))
    rows = cur.fetchall()
    cur.close()

    dados = []
    tz_brasilia = pytz.timezone("America/Sao_Paulo")

    for row in rows:
        idmov, data_mov, tipo, qtd, valor_unit, motivo, produto_nome, categoria_nome, usuario_nome, idlote, estoque_lote = row

        # Normaliza valores
        qtd = int(qtd) if qtd is not None else 0
        valor_unit = float(valor_unit) if valor_unit is not None else 0.0
        estoque_lote = int(estoque_lote) if estoque_lote is not None else 0

        # Ajuste de timezone (se for datetime)
        if isinstance(data_mov, datetime):
            if data_mov.tzinfo is None:  
                data_mov = data_mov.replace(tzinfo=pytz.UTC)
            data_brasilia = data_mov.astimezone(tz_brasilia)
            data_fmt = data_brasilia.isoformat()
        else:
            
            data_fmt = data_mov.isoformat()

        dados.append({
            "idmovimentacao": idmov,
            "data_movimentacao": data_fmt,
            "tipo": tipo,
            "quantidade": qtd,
            "valor_unitario": valor_unit,
            "motivo": motivo,
            "produto": produto_nome,
            "categoria": categoria_nome,
            "usuario": usuario_nome,
            "idlote": idlote,
            "estoque_lote": estoque_lote
        })

    return jsonify({"dados": dados, "data_inicio": data_inicio, "data_fim": data_fim})


@relatorio_routes.route('/relatorio/movimentacoes/export/csv')
def export_movimentacoes_csv():
    import csv
    import io
    from datetime import datetime, timedelta

    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    # últimos 30 dias
    if not data_inicio or not data_fim:
        hoje = datetime.today()
        data_fim = hoje.strftime("%Y-%m-%d")
        data_inicio = (hoje - timedelta(days=30)).strftime("%Y-%m-%d")

    conn = conectar()
    cur = conn.cursor()
    sql = """
        SELECT m.IDMOVIMENTACAO, m.DATA_MOVIMENTOCAO, m.TIPO, m.QUANTIDADE, m.VALOR_UNITARIO,
               m.MOTIVO, p.NOME AS PRODUTO, c.NOME AS CATEGORIA, u.NOME AS USUARIO,
               l.IDLOTE, COALESCE(l.QUANTIDADE,0) AS ESTOQUE_LOTE
        FROM MOVIMENTACAO m
        JOIN LOTE l ON l.IDLOTE = m.IDLOTE
        JOIN PRODUTO p ON p.IDPRODUTO = l.IDPRODUTO
        JOIN CATEGORIA c ON c.IDCATEGORIA = p.IDCATEGORIA
        JOIN USUARIO u ON u.IDUSUARIO = m.IDUSUARIO
        WHERE m.DATA_MOVIMENTOCAO BETWEEN %s AND %s
        ORDER BY m.DATA_MOVIMENTOCAO DESC
    """
    cur.execute(sql, (data_inicio, data_fim))
    rows = cur.fetchall()
    cur.close()
    try:
        conn.close()
    except Exception:
        pass

    # Monta CSV em memória
    text_buffer = io.StringIO(newline="")
    writer = csv.writer(text_buffer, delimiter=";")

    # Cabeçalho (sem Status)
    writer.writerow([
        "ID", "Data", "Produto", "Categoria", "Tipo", "Quantidade",
        "Valor Unitário", "Motivo", "Usuário", "Lote", "Estoque Lote"
    ])

    entradas, saidas, valor_total = 0, 0, 0
    for row in rows:
        idmov, data, tipo, qtd, valor, motivo, produto, categoria, usuario, idlote, estoque_lote = row

        # Normalização
        qtd = int(qtd) if qtd is not None else 0
        valor = float(valor) if valor is not None else 0.0
        estoque_lote = int(estoque_lote) if estoque_lote is not None else 0

        qtd_fmt = f"{qtd:,}".replace(",", ".")
        valor_fmt = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if valor else "-"

        # Data como string
        try:
            data_fmt = data.strftime("%d/%m/%Y %H:%M")
        except Exception:
            data_fmt = "-" if data is None else str(data)

        writer.writerow([
            idmov, data_fmt, produto, categoria, tipo or "-",
            qtd_fmt, valor_fmt, (motivo or "-"), usuario,
            idlote, estoque_lote
        ])

        # Resumo
        if (tipo or "").lower() == "entrada":
            entradas += qtd
        elif (tipo or "").lower() == "saida":
            saidas += qtd
        if valor:
            valor_total += valor * qtd

    # Linha em branco + resumo
    writer.writerow([])
    writer.writerow([f"Entradas: {entradas:,}".replace(",", ".")])
    writer.writerow([f"Saídas: {saidas:,}".replace(",", ".")])
    writer.writerow([f"Saldo líquido: {(entradas - saidas):,}".replace(",", ".")])
    writer.writerow(["Valor total movimentado: " +
                     f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")])

    # Converte para bytes com UTF-8
    csv_bytes = text_buffer.getvalue().encode("utf-8-sig")

    return Response(
        csv_bytes,
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment;filename=movimentacoes.csv"}
    )



@relatorio_routes.route('/relatorio/movimentacoes/export/pdf')
def export_movimentacoes_pdf():
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    import io
    from datetime import datetime, timedelta

    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    # últimos 30 dias
    if not data_inicio or not data_fim:
        hoje = datetime.today()
        data_fim = hoje.strftime("%Y-%m-%d")
        data_inicio = (hoje - timedelta(days=30)).strftime("%Y-%m-%d")

    conn = conectar()
    cur = conn.cursor()
    sql = """
        SELECT m.IDMOVIMENTACAO, m.DATA_MOVIMENTOCAO, m.TIPO, m.QUANTIDADE, m.VALOR_UNITARIO,
               m.MOTIVO, p.NOME AS PRODUTO, c.NOME AS CATEGORIA, u.NOME AS USUARIO,
               l.IDLOTE, COALESCE(l.QUANTIDADE,0) AS ESTOQUE_LOTE
        FROM MOVIMENTACAO m
        JOIN LOTE l ON l.IDLOTE = m.IDLOTE
        JOIN PRODUTO p ON p.IDPRODUTO = l.IDPRODUTO
        JOIN CATEGORIA c ON c.IDCATEGORIA = p.IDCATEGORIA
        JOIN USUARIO u ON u.IDUSUARIO = m.IDUSUARIO
        WHERE m.DATA_MOVIMENTOCAO BETWEEN %s AND %s
        ORDER BY m.DATA_MOVIMENTOCAO DESC
    """
    cur.execute(sql, (data_inicio, data_fim))
    rows = cur.fetchall()
    cur.close()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    styles = getSampleStyleSheet()
    elementos = []

    # Título
    adicionar_cabecalho_pdf(
    elementos,
    "Relatório de Movimentações",
    styles
)

    # Cabeçalho da tabela
    tabela_dados = [["ID", "Data", "Produto", "Categoria", "Tipo", "Quantidade",
                     "Valor Unitário", "Motivo", "Usuário", "Lote", "Estoque Lote"]]

    entradas, saidas, valor_total = 0, 0, 0
    for row in rows:
        idmov, data, tipo, qtd, valor, motivo, produto, categoria, usuario, idlote, estoque_lote = row

        # Normalização
        qtd = int(qtd) if qtd is not None else 0
        valor = float(valor) if valor is not None else 0.0
        estoque_lote = int(estoque_lote) if estoque_lote is not None else 0

        qtd_fmt = f"{qtd:,}".replace(",", ".")
        valor_fmt = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if valor else "-"

        tabela_dados.append([
            idmov,
            data.strftime("%d/%m/%Y %H:%M"),
            produto,
            categoria,
            tipo,
            qtd_fmt,
            valor_fmt,
            motivo or "-",
            usuario,
            idlote,
            estoque_lote
        ])

        if tipo.lower() == "entrada":
            entradas += qtd
        elif tipo.lower() == "saida":
            saidas += qtd
        if valor:
            valor_total += valor * qtd

    tabela = Table(tabela_dados, repeatRows=1)
    estilo = estilo_tabela_pdf()
    for i, row in enumerate(tabela_dados[1:], start=1):
        tipo = row[4]

        if str(tipo).lower() == "entrada":
            estilo.add("TEXTCOLOR", (4, i), (4, i), PDF_SUCCESS)
        elif str(tipo).lower() == "saida":
            estilo.add("TEXTCOLOR", (4, i), (4, i), PDF_DANGER)
    tabela.setStyle(estilo)
    elementos.append(tabela)
    elementos.append(Spacer(1, 20))

    # Resumo
    adicionar_resumo_pdf(
    elementos,
    styles,
    [
        ("Entradas", f"{entradas:,}".replace(",", ".")),
        ("Saídas", f"{saidas:,}".replace(",", ".")),
        ("Saldo líquido", f"{(entradas - saidas):,}".replace(",", ".")),
        (
            "Valor movimentado",
            f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        ),
    ],
)

    doc.build(elementos)
    buffer.seek(0)

    return Response(buffer, mimetype='application/pdf',
                    headers={"Content-Disposition": "attachment;filename=movimentacoes.pdf"})


@relatorio_routes.route('/relatorio/movimentacoes/export/xlsx')
def export_movimentacoes_xlsx():
    import xlsxwriter
    from datetime import datetime, timedelta
    import io

    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    # Default: últimos 30 dias
    if not data_inicio or not data_fim:
        hoje = datetime.today()
        data_fim = hoje.strftime("%Y-%m-%d")
        data_inicio = (hoje - timedelta(days=30)).strftime("%Y-%m-%d")

    conn = conectar()
    cur = conn.cursor()
    sql = """
        SELECT m.IDMOVIMENTACAO, m.DATA_MOVIMENTOCAO, m.TIPO, m.QUANTIDADE, m.VALOR_UNITARIO,
               m.MOTIVO, p.NOME AS PRODUTO, c.NOME AS CATEGORIA, u.NOME AS USUARIO,
               l.IDLOTE, COALESCE(l.QUANTIDADE,0) AS ESTOQUE_LOTE
        FROM MOVIMENTACAO m
        JOIN LOTE l ON l.IDLOTE = m.IDLOTE
        JOIN PRODUTO p ON p.IDPRODUTO = l.IDPRODUTO
        JOIN CATEGORIA c ON c.IDCATEGORIA = p.IDCATEGORIA
        JOIN USUARIO u ON u.IDUSUARIO = m.IDUSUARIO
        WHERE m.DATA_MOVIMENTOCAO BETWEEN %s AND %s
        ORDER BY m.DATA_MOVIMENTOCAO DESC
    """
    cur.execute(sql, (data_inicio, data_fim))
    rows = cur.fetchall()
    cur.close()

    # Arquivo em memória
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Movimentações")

    # Formatos
    header_format = workbook.add_format({'bold': True, 'bg_color': '#1a2a4f', 'color': 'white', 'align': 'center'})
    normal_format = workbook.add_format({'align': 'center'})
    entrada_format = workbook.add_format({'align': 'center', 'color': 'green'})
    saida_format = workbook.add_format({'align': 'center', 'color': 'red'})

    # Cabeçalho 
    headers = ["ID", "Data", "Produto", "Categoria", "Tipo", "Quantidade",
               "Valor Unitário", "Motivo", "Usuário", "Lote", "Estoque Lote"]
    for col, h in enumerate(headers):
        worksheet.write(0, col, h, header_format)

    # Dados
    entradas, saidas, valor_total = 0, 0, 0

    for row_idx, item in enumerate(rows, start=1):
        idmov, data, tipo, qtd, valor, motivo, produto, categoria, usuario, idlote, estoque_lote = item

        # Normalização
        qtd = int(qtd) if qtd is not None else 0
        valor = float(valor) if valor is not None else 0.0
        estoque_lote = int(estoque_lote) if estoque_lote is not None else 0

        qtd_fmt = f"{qtd:,}".replace(",", ".")
        valor_fmt = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if valor else "-"

        # Data como string 
        try:
            data_fmt = data.strftime("%d/%m/%Y %H:%M")
        except Exception:
            data_fmt = str(data)

        # Formato de tipo
        tipo_format = entrada_format if tipo.lower() == "entrada" else saida_format

        # Escreve linha
        worksheet.write(row_idx, 0, idmov, normal_format)
        worksheet.write(row_idx, 1, data_fmt, normal_format)
        worksheet.write(row_idx, 2, produto, normal_format)
        worksheet.write(row_idx, 3, categoria, normal_format)
        worksheet.write(row_idx, 4, tipo, tipo_format)
        worksheet.write(row_idx, 5, qtd_fmt, normal_format)
        worksheet.write(row_idx, 6, valor_fmt, normal_format)
        worksheet.write(row_idx, 7, motivo or "-", normal_format)
        worksheet.write(row_idx, 8, usuario, normal_format)
        worksheet.write(row_idx, 9, idlote, normal_format)
        worksheet.write(row_idx, 10, estoque_lote, normal_format)

        # Resumo
        if tipo.lower() == "entrada":
            entradas += qtd
        elif tipo.lower() == "saida":
            saidas += qtd
        if valor:
            valor_total += valor * qtd

    # Resumo
    base = len(rows) + 2
    worksheet.write(base + 0, 0, f"Entradas: {entradas:,}".replace(",", "."))
    worksheet.write(base + 1, 0, f"Saídas: {saidas:,}".replace(",", "."))
    worksheet.write(base + 2, 0, f"Saldo líquido: {(entradas - saidas):,}".replace(",", "."))
    worksheet.write(base + 3, 0, "Valor total movimentado: " +
                    f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    workbook.close()
    output.seek(0)

    return Response(
        output.read(),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment;filename=movimentacoes.xlsx"}
    )

