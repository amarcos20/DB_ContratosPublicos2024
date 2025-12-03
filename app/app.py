import warnings
# Suprime avisos futuros (como o que está na primeira linha do seu código original)
warnings.filterwarnings("ignore", category=FutureWarning) 
from flask import render_template, Flask, request
import logging
import db # Importa as funções execute/fetchone do db.py

TABLE_SCHEMA = {
    'CONTRATOS': {
        'fields': [
            {'name': 'ID_CONTRATO', 'type': 'int', 'note': 'PK'},
            {'name': 'DATACELEBRACAOCONTRATO', 'type': 'date', 'note': ''},
            {'name': 'DATAPUBLICACAOCONTRATO', 'type': 'date', 'note': ''},
            {'name': 'PRAZOEXECUCAO', 'type': 'varchar', 'note': ''},
            {'name': 'PRECOCONTRATUAL', 'type': 'float', 'note': ''},
            {'name': 'OBJECTOCONTRATO', 'type': 'text', 'note': ''},
            {'name': 'PROCEDIMENTOCENTRALIZADO', 'type': 'boolean', 'note': 'Opcional (?)'},
            {'name': 'ID_TIPO_CONTRATO', 'type': 'int', 'note': 'FK'},
            {'name': 'ID_FUNDAMENTO', 'type': 'int', 'note': 'FK'},
            {'name': 'ID_TIPO_PROCEDIMENTO', 'type': 'int', 'note': 'FK'},
            {'name': 'ID_ACORDO', 'type': 'int', 'note': 'FK'},
            {'name': 'ID_LOCAL', 'type': 'int', 'note': 'FK'},
            {'name': 'ID_CPV', 'type': 'int', 'note': 'FK'},
            {'name': 'ID_ADJUDICANTE', 'type': 'int', 'note': 'FK'},
            {'name': 'ID_ADJUDICATARIO', 'type': 'int', 'note': 'FK'},
        ]
    },
    'ENTIDADES': {
        'fields': [
            {'name': 'ID_ENTIDADE', 'type': 'int', 'note': 'PK'},
            {'name': 'NIF', 'type': 'varchar', 'note': ''},
            {'name': 'NOME', 'type': 'varchar', 'note': ''},
        ]
    },
    'TIPO_CONTRATO': {
        'fields': [
            {'name': 'ID_TIPO_CONTRATO', 'type': 'int', 'note': 'PK'}, 
            {'name': 'TIPO_CONTRATO', 'type': 'varchar', 'note': ''}, 
            {'name': 'TIPOCONTRATO', 'type': 'varchar', 'note': ''}
        ]
    },
    'FUNDAMENTACAO': {
        'fields': [
            {'name': 'ID_FUNDAMENTO', 'type': 'int', 'note': 'PK'}, 
            {'name': 'ARTIGO', 'type': 'varchar', 'note': ''}, 
            {'name': 'NUMERO', 'type': 'int', 'note': 'Opcional (?)'}, 
            {'name': 'DETALHEFUNDAMENTACAO', 'type': 'text', 'note': 'Opcional (?)'},
            {'name': 'ALINEA', 'type': 'varchar', 'note': 'Opcional (?)'},
        ]
    },
    'TIPO_PROCEDIMENTO': {
        'fields': [
            {'name': 'ID_TIPO_PROCEDIMENTO', 'type': 'int', 'note': 'PK'}, 
            {'name': 'PROCEDIMENTO', 'type': 'varchar', 'note': ''}, 
            {'name': 'TIPOPROCEDIMENTO', 'type': 'varchar', 'note': ''}
        ]
    },
    'ACORDO': {
        'fields': [
            {'name': 'ID_ACORDO', 'type': 'int', 'note': 'PK'}, 
            {'name': 'DESCRACORDOQUADRO', 'type': 'text', 'note': 'Opcional (?)'}
        ]
    },
    'LOCAL_EXECUCAO': {
        'fields': [
            {'name': 'ID_LOCAL', 'type': 'int', 'note': 'PK'}, 
            {'name': 'PAIS', 'type': 'varchar', 'note': ''}, 
            {'name': 'LOCALEXECUCAO', 'type': 'varchar', 'note': ''}, 
            {'name': 'DISTRITO', 'type': 'varchar', 'note': 'Opcional (?)'}, 
            {'name': 'CONCELHO', 'type': 'varchar', 'note': 'Opcional (?)'}
        ]
    },
    'CPV': {
        'fields': [
            {'name': 'ID_CPV', 'type': 'int', 'note': 'PK'}, 
            {'name': 'CPV', 'type': 'varchar', 'note': ''}, 
            {'name': 'CODIGO_CPV', 'type': 'varchar', 'note': ''}, 
            {'name': 'DESCRICAO', 'type': 'text', 'note': 'Opcional (?)'}
        ]
    },
}

# 1. Configuração e Inicialização do Flask
# Configura o logger para mostrar informações na consola
logging.basicConfig(level=logging.INFO) 

# ... (Imports e inicialização do Flask e logging permanecem os mesmos) ...

# 1. Cria a instância da aplicação Flask
APP = Flask(__name__) 
def get_dict_result(query, args=None):
    """Executa fetchone e converte o resultado do sqlite3.Row em dict."""
    result_row = db.fetchone(query, args)
    return dict(result_row) if result_row else None

# --- ROTAS BASE E QUERIES ---
def get_dict_result(query, args=None):
    """Executa fetchone e converte o resultado do sqlite3.Row em dict (assumindo db.fetchone devolve sqlite3.Row)."""
    # ❗ No código real, esta função deve usar db.fetchone
    result_row = db.fetchone(query, args)
    return dict(result_row) if result_row else None

# --- ROTAS BASE E QUERIES ---

@APP.route('/t')
def tabelas():
    """Rota de índice das tabelas."""
    # Prepara a lista de tabelas para o template tabelas.html
    table_list = [
        # Filtra apenas por PK e FK para a descrição na listagem
        {'name': name.upper(), 'fields': [f['name'] for f in data['fields'] if f.get('note') == 'PK' or f.get('note') == 'FK']}
        for name, data in TABLE_SCHEMA.items()
    ]
    return render_template('tabelas.html', tables=table_list)

@APP.route('/t/<table_name>')
def table_detail(table_name):
    """Rota de detalhe de uma tabela específica com as 5 primeiras linhas."""
    upper_name = table_name.upper()
    
    # 1. Obter a estrutura da tabela
    schema = TABLE_SCHEMA.get(upper_name)
    if not schema:
        return render_template('tabela_detalhe.html', table_name=upper_name, columns=[], data=[], fields=[])

    # 2. Obter as 5 primeiras linhas da base de dados
    columns = []
    data = []
    
    try:
        # ❗ QUERY SQL SIMPLES SEM MOCK DATA
        query = f'SELECT * FROM {upper_name} LIMIT 5'
        rows = db.execute(query) # Assume db.execute devolve uma lista de sqlite3.Row ou tuplos
        
        if rows:
            # Assume que a primeira linha (se não for sqlite3.Row) tem atributos de keys para colunas
            # Se db.execute devolve sqlite3.Row, pode-se usar rows[0].keys()
            # Se db.execute devolve tuplos, deve usar os nomes do schema ou ajustar db.execute
            
            # Tentativa de obter colunas (Ajuste se o seu db.execute for diferente)
            try:
                # Se db.execute devolve sqlite3.Row (dicionário-like)
                columns = list(rows[0].keys())
            except AttributeError:
                # Se db.execute devolve apenas tuplos, usamos as colunas do SCHEMA
                columns = [f['name'] for f in schema['fields']]

            data = [list(row) for row in rows] # Converte para lista de listas para o Jinja

    except Exception as e:
        logging.error(f"Erro inesperado ao consultar a tabela {upper_name}: {e}")
        pass

    return render_template('tabela_detalhe.html', 
                           table_name=upper_name, 
                           columns=columns, 
                           data=data, 
                           fields=schema['fields'])

@APP.route('/consultas')
@APP.route('/queries')
def lista_consultas():
    """Rota para exibir a lista de todas as consultas disponíveis."""
    # Não precisa de passar dados, pois a lista de links está no HTML
    return render_template('lista_consultas.html')
@APP.route('/')
def index():
    """Rota principal (Dashboard)."""
    stats = db.fetchone('''
        SELECT 
            COUNT(idcontrato) AS n_contratos 
        FROM CONTRATOS
    ''')
    
    queries_list = [f'query_{i}' for i in range(1, 16)]
    return render_template('index.html', stats=stats, queries=queries_list)

# --- 1. Queries de Visão Geral e Estatística (Q1 a Q5) ---

# NO FICHEIRO app.py, NA ROTA query_1
@APP.route('/queries/query_1')
def query_1():
    """Q1: Contagem Total e Valor Total/Médio dos Contratos"""
    resultados_row = db.fetchone('''
        SELECT 
            COUNT(idcontrato) AS ContagemTotal,
            ROUND(SUM(precoContratual), 2) AS ValorTotal,
            ROUND(AVG(precoContratual), 2) AS ValorMedio
        FROM CONTRATOS
    ''')
    # ❗ Converte o sqlite3.Row em dict para o template
    resultados = dict(resultados_row) if resultados_row else None
    
    return render_template('resultado_agregacao.html', 
                            titulo="Query 1: Contagem e Valor Total/Médio dos Contratos", 
                            resultado=resultados)

@APP.route('/queries/query_2')
def query_2():
    """Q2: Contrato com Valor Máximo (Detalhe do Contrato)"""
    resultados = get_dict_result('''
        SELECT 
            idcontrato, objectoContrato, precoContratual
        FROM CONTRATOS
        ORDER BY precoContratual DESC
        LIMIT 1
    ''')
    return render_template('resultado_agregacao.html', 
                            titulo="Query 2: Contrato com o Valor Máximo", 
                            resultado=resultados)

@APP.route('/queries/query_3')
def query_3():
    """Q3: Contagem por Distrito de Execução"""
    resultados = db.execute('''
        SELECT 
            L.DISTRITO, COUNT(C.idcontrato) AS NumContratos
        FROM CONTRATOS C
        JOIN LOCAL L ON C.localExecucao = L.ID_LOCAL
        WHERE L.DISTRITO IS NOT NULL
        GROUP BY L.DISTRITO
        ORDER BY NumContratos DESC
    ''')
    return render_template('resultado_tabela.html', 
                            titulo="Query 3: Contagem de Contratos por Distrito", 
                            colunas=['DISTRITO', 'NumContratos'], 
                            resultados=resultados)

# --- 2. Queries de Classificação e Agrupamento (Q6 a Q10) ---

@APP.route('/queries/query_4')
def query_4():
    """Q4: Top 5 Tipos de Contrato"""
    resultados = db.execute('''
        SELECT 
            TT.TIPO_CONTRATO, COUNT(C.idcontrato) AS NumContratos
        FROM CONTRATOS C
        JOIN TIPO_CONTRATO TT ON C.tipocontrato = TT.ID_TIPO_CONTRATO
        GROUP BY TT.TIPO_CONTRATO
        ORDER BY NumContratos DESC
        LIMIT 5
    ''')
    return render_template('resultado_tabela.html', 
                            titulo="Query 4: Top 5 Tipos de Contrato", 
                            colunas=['Tipo Contrato', 'NumContratos'], 
                            resultados=resultados)

@APP.route('/queries/query_5')
def query_5():
    """Q5: Contagem por Tipo de Procedimento"""
    resultados = db.execute('''
        SELECT 
            TP.TIPO_PROCEDIMENTO, COUNT(C.idcontrato) AS NumContratos
        FROM CONTRATOS C
        JOIN TIPO_PROCEDIMENTO TP ON C.tipoprocedimento = TP.ID_TIPO_PROCEDIMENTO
        GROUP BY TP.TIPO_PROCEDIMENTO
        ORDER BY NumContratos DESC
    ''')
    return render_template('resultado_tabela.html', 
                            titulo="Query 5: Contagem por Tipo de Procedimento", 
                            colunas=['Procedimento', 'NumContratos'], 
                            resultados=resultados)

@APP.route('/queries/query_6')
def query_6():
    """Q6: Top 10 CPV (Código de Classificação)"""
    resultados = db.execute('''
        SELECT 
            P.DESCRICAO, P.CODIGO_CPV, COUNT(C.idcontrato) AS NumContratos
        FROM CONTRATOS C
        JOIN CPV P ON C.cpv = P.ID_CPV
        GROUP BY P.DESCRICAO, P.CODIGO_CPV
        ORDER BY NumContratos DESC
        LIMIT 10
    ''')
    return render_template('resultado_tabela.html', 
                            titulo="Query 6: Top 10 Códigos CPV (Descrição)", 
                            colunas=['Descrição CPV', 'Código CPV', 'NumContratos'], 
                            resultados=resultados)


@APP.route('/queries/query_7')
def query_7():
    """Q7: Duração Média (prazoExecucao) por Tipo de Contrato"""
    resultados = db.execute('''
        SELECT 
            TT.TIPO_CONTRATO, 
            COUNT(C.idcontrato) AS NumContratosValidos                     -- ❗ Adicionado Contagem
        FROM CONTRATOS C
        JOIN TIPO_CONTRATO TT ON C.tipocontrato = TT.ID_TIPO_CONTRATO
        WHERE C.prazoExecucao IS NOT NULL AND C.prazoExecucao > 0
        GROUP BY TT.TIPO_CONTRATO
        ORDER BY PrazoMedioDias DESC
    ''')
    return render_template('resultado_tabela.html', 
                            titulo="Query 7: Prazo Médio de Execução por Tipo de Contrato (Dias)", 
                            colunas=['Tipo Contrato', 'Prazo Médio (dias)'], 
                            resultados=resultados)

# --- 3. Queries de Entidades e Detalhes (Q11 a Q15) ---

@APP.route('/queries/query_8')
def query_8():
    """Q8: Top 10 Adjudicantes por Valor Contratado"""
    resultados = db.execute('''
        SELECT 
            E.NOME AS NomeAdjudicante, 
            E.NIF, 
            ROUND(SUM(C.precoContratual), 2) AS ValorTotalContratado
        FROM CONTRATOS C
        JOIN ENTIDADES E ON C.adjudicante = E.ID_ENTIDADE
        WHERE C.adjudicante IS NOT NULL                          -- ❗ Garantir que só contamos IDs válidos
        GROUP BY E.NOME, E.NIF
        ORDER BY ValorTotalContratado DESC
        LIMIT 10
    ''')
    return render_template('resultado_tabela.html', 
                            titulo="Query 8: Top 10 Adjudicantes por Valor", 
                            colunas=['Nome Adjudicante', 'NIF', 'Valor Contratado (€)'], 
                            resultados=resultados)

@APP.route('/queries/query_9')
def query_9():
    """Q9: Pesquisa por Objeto (Input de Pesquisa)"""
    termo = request.args.get('termo', 'Todos') 
    
    resultados = db.execute('''
        SELECT 
            idcontrato, objectocontrato, precoContratual
        FROM CONTRATOS
        WHERE objectocontrato LIKE ?
        LIMIT 20
    ''', [f'%{termo}%'])

    return render_template('resultado_pesquisa.html', 
                            titulo=f"Query 9: Contratos com Objeto Contendo '{termo}'", 
                            colunas=['ID Contrato', 'Objeto', 'Preço'], 
                            resultados=resultados, 
                            termo_pesquisado=termo)



@APP.route('/queries/query_10')
def query_10():
    """Q10: Entidades Registadas sem NIF (Validação de Dados)"""
    resultados = db.execute('''
        SELECT 
            ID_ENTIDADE, NOME
        FROM ENTIDADES
        WHERE NIF IS NULL OR NIF = 'RGPD'
        LIMIT 10
    ''')
    return render_template('resultado_tabela.html', 
                            titulo="Query 10: Entidades Registadas sem NIF", 
                            colunas=['ID Entidade', 'Nome', 'NIF'], 
                            resultados=resultados)
@APP.route('/queries/query_11')
def query_11():
    """Q11: valor total de todos os contratos em cada distrito e lista os 10 distritos com o maior valor total."""
    resultados = db.execute('''
      SELECT
    LE.DISTRITO,
    COUNT(C.IDCONTRATO) AS TotalContratos,
    SUM(C.PRECOCONTRATUAL) AS ValorTotalContratado
FROM
    CONTRATOS C
JOIN
    LOCAL LE ON C.localExecucao = LE.ID_LOCAL
WHERE
    LE.DISTRITO IS NOT NULL
GROUP BY
    LE.DISTRITO
ORDER BY
    ValorTotalContratado DESC
LIMIT 10;
    ''')
    return render_template('resultado_tabela.html', 
                            titulo="Query 11: valor total de todos os contratos em cada distrito e lista os 10 distritos com o maior valor total.", 
                            colunas=['Distrito', 'TotalContratos', 'ValorTotalContratado'], 
                            resultados=resultados)
@APP.route('/queries/query_12')
def query_12():
    """Q12: preço médio de contrato para cada tipo de procedimento, útil para identificar quais procedimentos tendem a ser mais caros"""
    resultados = db.execute('''
        SELECT
    TP.TIPO_PROCEDIMENTO,
    COUNT(C.IDCONTRATO) AS TotalContratos,
    ROUND(AVG(C.PRECOCONTRATUAL), 2) AS PrecoMedioContrato
FROM
    CONTRATOS C
JOIN
    TIPO_PROCEDIMENTO TP ON C.tipoprocedimento = TP.ID_TIPO_PROCEDIMENTO
GROUP BY
    TP.TIPO_PROCEDIMENTO
HAVING
    COUNT(C.IDCONTRATO) >= 50 -- Apenas tipos com pelo menos 50 contratos
ORDER BY
    PrecoMedioContrato DESC;
    ''')
    return render_template('resultado_tabela.html', 
                            titulo="Query 12: preço médio de contrato para cada tipo de procedimento, útil para identificar quais procedimentos tendem a ser mais caros", 
                            colunas=['TIPO_PROCEDIMENTO', 'TotalContratos', 'PrecoMedioContrato'], 
                            resultados=resultados)
# No seu app.py

QUERY_TITLES = {
    'query_1': "Contagem e Valor Total/Médio dos Contratos",
    'query_2': "Contrato com o Valor Máximo",
    'query_3': "Contagem de Contratos por Distrito",
    'query_4': "Top 5 Tipos de Contrato",
    'query_5': "Contagem por Tipo de Procedimento",
    'query_6': "Top 10 Códigos CPV (Descrição)",
    'query_7': "Prazo Médio de Execução por Tipo de Contrato (Dias)",
    'query_8': "Top 10 Adjudicantes por Valor",
    'query_9': "Pesquisa por Objeto (Requer Parâmetro 'termo')",
    'query_10': "Entidades Registadas sem NIF",
    'query_11': "Valor Total de Contratos por Distrito (Top 10)",
    'query_12': "Preço Médio de Contrato por Tipo de Procedimento"
}
SQL_QUERIES = {
    'query_1': """
        SELECT
            COUNT(idcontrato) AS ContagemTotal,
            ROUND(SUM(precoContratual), 2) AS ValorTotal,
            ROUND(AVG(precoContratual), 2) AS ValorMedio
        FROM CONTRATOS
    """,
    'query_2': """
        SELECT
            idcontrato, objectoContrato, precoContratual
        FROM CONTRATOS
        ORDER BY precoContratual DESC
        LIMIT 1
    """,
    'query_3': """
        SELECT
            L.DISTRITO, COUNT(C.idcontrato) AS NumContratos
        FROM CONTRATOS C
        JOIN LOCAL L ON C.localExecucao = L.ID_LOCAL
        WHERE L.DISTRITO IS NOT NULL
        GROUP BY L.DISTRITO
        ORDER BY NumContratos DESC
    """,
    'query_4': """
        SELECT
            TT.TIPO_CONTRATO, COUNT(C.idcontrato) AS NumContratos
        FROM CONTRATOS C
        JOIN TIPO_CONTRATO TT ON C.tipocontrato = TT.ID_TIPO_CONTRATO
        GROUP BY TT.TIPO_CONTRATO
        ORDER BY NumContratos DESC
        LIMIT 5
    """,
    'query_5': """
        SELECT
            TP.TIPO_PROCEDIMENTO, COUNT(C.idcontrato) AS NumContratos
        FROM CONTRATOS C
        JOIN TIPO_PROCEDIMENTO TP ON C.tipoprocedimento = TP.ID_TIPO_PROCEDIMENTO
        GROUP BY TP.TIPO_PROCEDIMENTO
        ORDER BY NumContratos DESC
    """,
    'query_6': """
        SELECT
            P.DESCRICAO, P.CODIGO_CPV, COUNT(C.idcontrato) AS NumContratos
        FROM CONTRATOS C
        JOIN CPV P ON C.cpv = P.ID_CPV
        GROUP BY P.DESCRICAO, P.CODIGO_CPV
        ORDER BY NumContratos DESC
        LIMIT 10
    """,
    'query_7': """
        -- Código corrigido para calcular a média (AVG)
        SELECT
            TT.TIPO_CONTRATO,
            ROUND(AVG(C.prazoExecucao), 2) AS PrazoMedioDias,
            COUNT(C.idcontrato) AS NumContratosValidos
        FROM CONTRATOS C
        JOIN TIPO_CONTRATO TT ON C.tipocontrato = TT.ID_TIPO_CONTRATO
        WHERE C.prazoExecucao IS NOT NULL AND C.prazoExecucao > 0
        GROUP BY TT.TIPO_CONTRATO
        ORDER BY PrazoMedioDias DESC
    """,
    'query_8': """
        SELECT
            E.NOME AS NomeAdjudicante,
            E.NIF,
            ROUND(SUM(C.precoContratual), 2) AS ValorTotalContratado
        FROM CONTRATOS C
        JOIN ENTIDADES E ON C.adjudicante = E.ID_ENTIDADE
        WHERE C.adjudicante IS NOT NULL
        GROUP BY E.NOME, E.NIF
        ORDER BY ValorTotalContratado DESC
        LIMIT 10
    """,
    'query_9': """
        -- Esta query usa um parâmetro de pesquisa (objectocontrato LIKE ?)
        SELECT
            idcontrato, objectocontrato, precoContratual
        FROM CONTRATOS
        WHERE objectocontrato LIKE ?
        LIMIT 20
    """,
    'query_10': """
        SELECT
            ID_ENTIDADE, NOME
        FROM ENTIDADES
        WHERE NIF IS NULL OR NIF = 'RGPD'
        LIMIT 10
    """,
    'query_11': """
        SELECT
            LE.DISTRITO,
            COUNT(C.IDCONTRATO) AS TotalContratos,
            SUM(C.PRECOCONTRATUAL) AS ValorTotalContratado
        FROM
            CONTRATOS C
        JOIN
            LOCAL LE ON C.localExecucao = LE.ID_LOCAL
        WHERE
            LE.DISTRITO IS NOT NULL
        GROUP BY
            LE.DISTRITO
        ORDER BY
            ValorTotalContratado DESC
        LIMIT 10;
    """,
    'query_12': """
        SELECT
            TP.TIPO_PROCEDIMENTO,
            COUNT(C.IDCONTRATO) AS TotalContratos,
            ROUND(AVG(C.PRECOCONTRATUAL), 2) AS PrecoMedioContrato
        FROM
            CONTRATOS C
        JOIN
            TIPO_PROCEDIMENTO TP ON C.tipoprocedimento = TP.ID_TIPO_PROCEDIMENTO
        GROUP BY
            TP.TIPO_PROCEDIMENTO
        HAVING
            COUNT(C.IDCONTRATO) >= 50
        ORDER BY
            PrecoMedioContrato DESC;
    """
}
@APP.route('/queries/code/<string:query_id>')
def exibir_codigo_sql(query_id):
    """
    Função que busca o código SQL no dicionário e o exibe no template.
    """
    if query_id in SQL_QUERIES:
        sql_code = SQL_QUERIES[query_id]
        # Use a variável do nome que definiu no seu app (APP ou app)
        title = QUERY_TITLES.get(query_id, f"Código SQL para {query_id}")
        return render_template(
            'exibir_codigo.html', 
            title=title,
            sql_code=sql_code
        )