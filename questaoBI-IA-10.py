import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo CSV
df = pd.read_csv("csv/VendasGlobais.csv")

# Lista de países europeus presentes no arquivo
paises_europeus = [
    "Germany", "France", "UK", "Ireland", "Denmark", "Sweden", "Austria",
    "Spain", "Portugal", "Belgium", "Switzerland", "Italy", "Finland",
    "Poland", "Norway"
]

# Filtrar apenas os registros de países europeus
df_europa = df[df["ClientePaís"].isin(paises_europeus)]

# Agrupar por país e somar as vendas
vendas_por_pais = df_europa.groupby("ClientePaís")["Vendas"].sum().sort_values(ascending=False)

# Exibir os valores
print("Total de vendas por país europeu:")
print(vendas_por_pais)

# Criar gráfico de barras
plt.figure(figsize=(10, 6))
vendas_por_pais.plot(kind='bar', color='cornflowerblue')
plt.title("Vendas Totais por País na Europa")
plt.xlabel("País")
plt.ylabel("Vendas ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()