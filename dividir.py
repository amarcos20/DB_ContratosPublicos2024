import pandas as pd
import os

# --- Definição do novo diretório ---
diretorio_destino = 'tabelas_3' 
# Cria o diretório 'tabelas_3' se ele não existir
os.makedirs(diretorio_destino, exist_ok=True) 

df = pd.read_excel('ContratosPublicos2024.xlsx')
df.head()

coluna_chave = 'idcontrato' 
dataframes_por_coluna = {}

# Itera sobre todas as colunas do DataFrame
for nome_coluna in df.columns:
    # Cria uma lista de colunas para selecionar, incluindo sempre a chave
    colunas_para_selecionar = [coluna_chave, nome_coluna]
    
    # Remove duplicatas da lista no caso de nome_coluna ser 'idcontrato'
    colunas_para_selecionar = list(set(colunas_para_selecionar)) 
    
    # Cria o novo DataFrame com 'idcontrato' e a coluna atual
    novo_df = df[colunas_para_selecionar].copy()
    
    # Prepara o nome do arquivo e o caminho completo no novo diretório
    nome_arquivo_limpo = nome_coluna.replace(' ', '_').replace('/', '_')
    caminho_completo = os.path.join(diretorio_destino, f'{nome_arquivo_limpo}.csv')
    
    # Salva o DataFrame no novo diretório
    novo_df.to_csv(caminho_completo, index=False)

print(f"✅ DataFrames salvos no novo diretório: '{diretorio_destino}'.")
print("Cada arquivo CSV contém a coluna 'idcontrato' e uma das outras colunas.")