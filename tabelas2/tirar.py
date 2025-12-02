import pandas as pd
c = pd.read_csv('contratos.csv')
print(c.head())
c.drop('Unnamed: 0',axis=1,inplace=True)
print(c.head())
c.to_csv('contratos.csv')