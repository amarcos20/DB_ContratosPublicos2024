import warnings
# Suprime avisos futuros (como o que está na primeira linha do seu código original)
warnings.filterwarnings("ignore", category=FutureWarning) 

from flask import render_template, Flask, request
import logging
import db # Importa as funções execute/fetchone do db.py

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

@APP.route('/')
def index():
    """Rota principal (Dashboard)."""
    stats = db.fetchone('''
        SELECT 
            COUNT(idcontrato) AS n_contratos, 
            ROUND(AVG(precoContratual), 2) AS valor_medio_contrato,
            MAX(prazoExecucao) AS prazo_maximo
        FROM CONTRATOS
    ''')
    
    queries_list = [f'query_{i}' for i in range(1, 16)]
    return render_template('index.html', stats=stats, queries=queries_list)

# --- 1. Queries de Visão Geral e Estatística (Q1 a Q5) ---

# NO FICHEIRO app.py, NA ROTA query_1
@APP.route('/queries/query_1')
def query_1():
    """Q1 & Q2: Contagem Total e Valor Total/Médio dos Contratos"""
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

@APP.route('/queries/query_2', methods=['GET'])
def query_2_entidade():
    """Q2: Pesquisa de Contratos por Entidade (Adjudicante/Adjudicatário)"""
    
    # 1. Obter todas as entidades para o dropdown
    entidades = db.execute('''
        SELECT ID_ENTIDADE, NOME FROM ENTIDADES ORDER BY NOME
    ''')
    
    # 2. Obter os filtros do utilizador
    entidade_id = request.args.get('entidade_id')
    tipo_entidade = request.args.get('tipo', 'adjudicante') # Default é adjudicante
    
    resultados = []
    entidade_nome = ""
    
    if entidade_id:
        # A coluna de JOIN muda dinamicamente
        join_col = 'C.adjudicante' if tipo_entidade == 'adjudicante' else 'C.adjudicatario'
        
        # Obter o nome da entidade selecionada
        entidade_nome_row = db.fetchone("SELECT NOME FROM ENTIDADES WHERE ID_ENTIDADE = ?", [entidade_id])
        entidade_nome = entidade_nome_row['NOME'] if entidade_nome_row else "Desconhecida"

        # Executar a query filtrada
        resultados = db.execute(f'''
            SELECT 
                idcontrato, objectocontrato, precoContratual, dataCelebracaoContrato
            FROM CONTRATOS C
            WHERE {join_col} = ?
            LIMIT 20
        ''', [entidade_id])

    return render_template('resultado_pesquisa_entidade.html', 
                           titulo="Query 2: Pesquisa de Contratos por Entidade",
                           entidades=entidades,
                           selecionado_id=entidade_id,
                           selecionado_nome=entidade_nome,
                           tipo_entidade=tipo_entidade,
                           resultados=resultados,
                           colunas=['ID Contrato', 'Objeto', 'Preço', 'Data Celebração'])

@APP.route('/queries/query_3')
def query_3():
    """Q3: Contratos por Ano (Data da Celebração)"""
    resultados = db.execute('''
        SELECT 
            STRFTIME('%Y', DataCelebracaoContrato) AS Ano,
            COUNT(idcontrato) AS NumContratos
        FROM CONTRATOS
        WHERE DataCelebracaoContrato IS NOT NULL  
        GROUP BY Ano
        ORDER BY Ano DESC
    ''')
    # ...
    return render_template('resultado_tabela.html', 
                            titulo="Query 3: Contratos por Ano de Celebração", 
                            colunas=['Ano', 'NumContratos'], 
                            resultados=resultados)

@APP.route('/queries/query_4')
def query_4():
    """Q4: Contrato com Valor Máximo (Detalhe do Contrato)"""
    resultados = get_dict_result('''
        SELECT 
            idcontrato, objectoContrato, precoContratual
        FROM CONTRATOS
        ORDER BY precoContratual DESC
        LIMIT 1
    ''')
    return render_template('resultado_agregacao.html', 
                            titulo="Query 4: Contrato com o Valor Máximo", 
                            resultado=resultados)

@APP.route('/queries/query_5')
def query_5():
    """Q5: Contagem por Distrito de Execução"""
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
                            titulo="Query 5: Contagem de Contratos por Distrito", 
                            colunas=['DISTRITO', 'NumContratos'], 
                            resultados=resultados)

# --- 2. Queries de Classificação e Agrupamento (Q6 a Q10) ---

@APP.route('/queries/query_6')
def query_6():
    """Q6: Top 5 Tipos de Contrato"""
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
                            titulo="Query 6: Top 5 Tipos de Contrato", 
                            colunas=['Tipo Contrato', 'NumContratos'], 
                            resultados=resultados)

@APP.route('/queries/query_7')
def query_7():
    """Q7: Contagem por Tipo de Procedimento"""
    resultados = db.execute('''
        SELECT 
            TP.TIPO_PROCEDIMENTO, COUNT(C.idcontrato) AS NumContratos
        FROM CONTRATOS C
        JOIN TIPO_PROCEDIMENTO TP ON C.tipoprocedimento = TP.ID_TIPO_PROCEDIMENTO
        GROUP BY TP.TIPO_PROCEDIMENTO
        ORDER BY NumContratos DESC
    ''')
    return render_template('resultado_tabela.html', 
                            titulo="Query 7: Contagem por Tipo de Procedimento", 
                            colunas=['Procedimento', 'NumContratos'], 
                            resultados=resultados)

@APP.route('/queries/query_8')
def query_8():
    """Q8: Top 10 CPV (Código de Classificação)"""
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
                            titulo="Query 8: Top 10 Códigos CPV (Descrição)", 
                            colunas=['Descrição CPV', 'Código CPV', 'NumContratos'], 
                            resultados=resultados)

@APP.route('/queries/query_9')
def query_9():
    """Q9: Contagem por Fundamento Legal (Artigo)"""
    resultados = db.execute('''
        SELECT 
            F.ARTIGO, COUNT(C.idcontrato) AS NumContratos
        FROM CONTRATOS C
        JOIN FUNDAMENTO F ON C.fundamentacao = F.ID_FUNDAMENTO
        WHERE F.ARTIGO IS NOT NULL
        GROUP BY F.ARTIGO
        ORDER BY NumContratos DESC
    ''')
    return render_template('resultado_tabela.html', 
                            titulo="Query 9: Contagem por Artigo de Fundamentação", 
                            colunas=['Artigo', 'NumContratos'], 
                            resultados=resultados)

@APP.route('/queries/query_10')
def query_10():
    """Q10: Duração Média (prazoExecucao) por Tipo de Contrato"""
    resultados = db.execute('''
        SELECT 
            TT.TIPO_CONTRATO, 
            ROUND(AVG(CAST(C.prazoExecucao AS REAL)), 2) AS PrazoMedioDias, -- ❗ Adicionado CAST e precisão 2
            COUNT(C.idcontrato) AS NumContratosValidos                     -- ❗ Adicionado Contagem
        FROM CONTRATOS C
        JOIN TIPO_CONTRATO TT ON C.tipocontrato = TT.ID_TIPO_CONTRATO
        WHERE C.prazoExecucao IS NOT NULL AND C.prazoExecucao > 0
        GROUP BY TT.TIPO_CONTRATO
        ORDER BY PrazoMedioDias DESC
    ''')
    return render_template('resultado_tabela.html', 
                            titulo="Query 10: Prazo Médio de Execução por Tipo de Contrato (Dias)", 
                            colunas=['Tipo Contrato', 'Prazo Médio (dias)'], 
                            resultados=resultados)

# --- 3. Queries de Entidades e Detalhes (Q11 a Q15) ---

@APP.route('/queries/query_11')
def query_11():
    """Q11: Top 10 Adjudicantes por Valor Contratado"""
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
                            titulo="Query 11: Top 10 Adjudicantes por Valor", 
                            colunas=['Nome Adjudicante', 'NIF', 'Valor Contratado (€)'], 
                            resultados=resultados)

@APP.route('/queries/query_12')
def query_12():
    """Q12: Top 10 Adjudicatários por Contagem de Contratos"""
    resultados = db.execute('''
        SELECT 
            E.NOME AS NomeAdjudicatario, 
            E.NIF, 
            COUNT(C.idcontrato) AS NumContratos
        FROM CONTRATOS C
        JOIN ENTIDADES E ON C.Adjudicatarios = E.ID_ENTIDADE
        GROUP BY E.NOME, E.NIF
        ORDER BY NumContratos DESC
        LIMIT 10
    ''')
    return render_template('resultado_tabela.html', 
                            titulo="Query 12: Top 10 Adjudicatários por Número de Contratos", 
                            colunas=['Nome Adjudicatário', 'NIF', 'Contratos Ganhos'], 
                            resultados=resultados)

@APP.route('/queries/query_13')
def query_13():
    """Q13: Pesquisa por Objeto (Input de Pesquisa)"""
    termo = request.args.get('termo', 'Todos') 
    
    resultados = db.execute('''
        SELECT 
            idcontrato, objectocontrato, precoContratual
        FROM CONTRATOS
        WHERE objectocontrato LIKE ?
        LIMIT 20
    ''', [f'%{termo}%'])

    return render_template('resultado_pesquisa.html', 
                            titulo=f"Query 13: Contratos com Objeto Contendo '{termo}'", 
                            colunas=['ID Contrato', 'Objeto', 'Preço'], 
                            resultados=resultados, 
                            termo_pesquisado=termo)


@APP.route('/queries/query_14')
def query_14():
    """Q14: Contratos celebrados em Acordo-Quadro (AQ)"""
    resultados = db.execute('''
        SELECT 
            C.idcontrato, C.objectocontrato, A.DESC_ACORDO_QUADRO
        FROM CONTRATOS C
        JOIN ACORDO A ON C.DescrAcordoQuadro = A.ID_ACORDO  
        LIMIT 20
    ''')
    return render_template('resultado_tabela.html', 
                            titulo="Query 14: Contratos Celebrados em Acordo-Quadro", 
                            colunas=['ID Contrato', 'Objeto', 'Descrição do Acordo-Quadro'], 
                            resultados=resultados)


@APP.route('/queries/query_15')
def query_15():
    """Q15: Entidades Registadas sem NIF (Validação de Dados)"""
    resultados = db.execute('''
        SELECT 
            ID_ENTIDADE, NOME, NIF
        FROM ENTIDADES
        WHERE NIF IS NULL OR NIF = ''
        LIMIT 10
    ''')
    return render_template('resultado_tabela.html', 
                            titulo="Query 15: Entidades Registadas sem NIF", 
                            colunas=['ID Entidade', 'Nome', 'NIF'], 
                            resultados=resultados)