import logging
import sqlite3
import re
import os
from contextlib import closing # Usado para garantir que a conexão fecha

# --- CONFIGURAÇÃO ---
# O DB_FILE deve ser acessível a partir da localização do seu server.py
# Se estiver na mesma pasta, use apenas o nome:
DB_FILE = 'CONTRATOS.db'

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
# --- FIM CONFIGURAÇÃO ---


# Função para criar uma nova conexão
# Vamos abrir e fechar a conexão em CADA query para evitar problemas de thread,
# o que é aceitável para aplicações SQLite pequenas.
def get_db_connection():
    """
    Cria e retorna uma nova conexão SQLite com row_factory ativada.
    """
    if not os.path.exists(DB_FILE):
        logging.warning(f"Ficheiro de Base de Dados '{DB_FILE}' não encontrado. Será criado automaticamente.")
        
    try:
        conn = sqlite3.connect(DB_FILE)
        # Permite aceder às colunas pelo nome (ex: resultado['NOME'])
        conn.row_factory = sqlite3.Row 
        return conn
    except sqlite3.Error as e:
        logging.error(f"Erro ao conectar à base de dados: {e}")
        raise # Levanta o erro para a aplicação Flask lidar com ele


# Função adaptada para executar comandos SQL (SELECT que retornam múltiplos resultados)
def execute(sql, args=None):
    """
    Executa uma query SQL (preferencialmente SELECT) e retorna todos os resultados.
    """
    sql_limpo = re.sub(r'\s+', ' ', sql).strip()
    logging.info(f'SQL (All): {sql_limpo} Args: {args}')
    
    # Usa 'closing' para garantir que a conexão é fechada, mesmo em caso de erro
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        try:
            if args:
                cursor.execute(sql, args)
            else:
                cursor.execute(sql)
            
            # Se for um SELECT, retorna todos os dados
            if sql_limpo.upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                # Para comandos de escrita (INSERT, UPDATE, DELETE)
                conn.commit()
                return None
        except sqlite3.Error as e:
            logging.error(f"Erro na execução SQL: {e}")
            raise # Re-lança o erro para ser tratado na rota Flask

# Função auxiliar para SELECTs que retornam apenas um resultado (Q1, Q4, etc.)
def fetchone(sql, args=None):
    """
    Executa uma query SQL e retorna apenas o primeiro resultado.
    """
    sql_limpo = re.sub(r'\s+', ' ', sql).strip()
    logging.info(f'SQL (One): {sql_limpo} Args: {args}')

    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        try:
            if args:
                cursor.execute(sql, args)
            else:
                cursor.execute(sql)
                
            if sql_limpo.upper().startswith("SELECT"):
                return cursor.fetchone()
            else:
                conn.commit()
                return None
        except sqlite3.Error as e:
            logging.error(f"Erro na execução SQL (fetchone): {e}")
            raise

# Não é necessário usar a função 'connect' ou 'close' diretamente nas rotas,
# pois a gestão da conexão é feita dentro de cada chamada 'execute'/'fetchone'.

# ** Nota: A função 'execute' anterior foi renomeada para 'execute_write' se 
# precisasse de INSERTs/UPDATEs, mas a nova função 'execute' já trata isso. **
