---

## III. Usage and Deliverables

### Deliverables

1.  *ETL Script (DataBase_Modeling.ipynb):* O script principal (Notebook Jupyter) contendo toda a lógica de transformação, validação e geração de IDs, culminando na criação da base de dados final.
2.  *Cleaned Dimensional Files (.csv):* Tabelas de pesquisa padronizadas, desduplicadas e indexadas por ID (e.g., `entities.csv`, `cpv_codes.csv`, `local_execution.csv`).
3.  *Final Database (.db):* O ficheiro da base de dados relacional (`ContratosPublicos2024.db` ou similar) pronto para ser consumido pela aplicação.

---

### Execution and Usage

Para executar o projeto e visualizar a aplicação, siga os seguintes passos:

#### 1. Configuração do Ambiente (Conda)

Crie um ambiente Python dedicado e instale as dependências:

```bash
# 1. Criar o ambiente Conda com Python 3.12
conda create --name sql python=3.12

# 2. Ativar o ambiente
conda activate sql

# 3. Instalar as dependências (incluindo pandas, sqlite3, e frameworks da app)
conda install -r requirements.txt

# Rodar o ficheiro Jupyter Notebook
# Este passo executa a limpeza, modelação e criação da DB.
jupyter notebook DataBase_Modeling.ipynb
# OU (Se usar a CLI do ipynb)
# python -m ipykernel run DataBase_Modeling.ipynb

# Rodar a aplicação (assumindo que 'server.py' contém a lógica do Flask/Streamlit/Django)
python server.py

