---

## III. Usage and Deliverables

### Deliverables

1.  *ETL Script (DataBase_Modeling.ipynb):* O script principal (Notebook Jupyter) contendo toda a lógica de transformação, validação e geração de IDs, culminando na criação da base de dados final.
2.  *Cleaned Dimensional Files (.csv):* Tabelas de pesquisa padronizadas, desduplicadas e indexadas por ID (e.g., `entidades.csv`, `cpv.csv`, `localExecucao.csv`).
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
pip install -r requirements.txt
```
#### 2. Rodar o ficheiro Jupyter Notebook **DATABASE_MODELING**
 Este passo executa a limpeza, modelação e criação da DB.
#### 3. Ligar o server.py
```bash
# Rodar a aplicação (assumindo que 'server.py' contém a lógica do Flask/Streamlit/Django)
python server.py
---
```

---

## Equipa / Créditos

Este projeto foi desenvolvido por:

| Membro | Curso e Número Mecanográfico | Perfil do LinkedIn |
| :--- | :--- | :--- |
| **Afonso Marcos** | Bioinformática FCUP / 202404088 | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/afonsomarcos20/) |
| **Pedro Afonso** | Bioinformática FCUP / 202404125 | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pedro-afonso-282a43294/) |
| **Artur Anselmo** | Bioinformática FCUP / 202403965 | (Link indisponível) |
| **Marcos Torres** | Bioinformática FCUP / 202409299 | (Link indisponível) |

---*Marcos Torres** | Bioinformática FCUP / 202409299 | (Link indisponível) |

---
---
