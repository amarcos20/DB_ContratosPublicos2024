#! /usr/bin/python3
import logging
from app import APP
# O 'db' é importado, mas NÃO precisa de ser conectado manualmente
# A conexão é gerida por chamada dentro das rotas.

if __name__ == '__main__':
  # Configuração de logging
  logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
  
  # REMOVER: db.connect() - A função não é usada na nova estrutura de db.py
  # A gestão da conexão é automática.
  
  # Inicia o servidor Flask
  APP.run(host='0.0.0.0', port=9999)

