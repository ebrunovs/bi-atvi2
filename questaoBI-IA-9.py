import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo CSV
df = pd.read_csv("csv/VendasGlobais.csv")

# Converter a coluna de data para datetime
df["Data"] = pd.to_datetime(df["Data"], errors="coerce", dayfirst=True)

# Extrair o ano
df["Ano"] = df["Data"].dt.year

# Filtrar registros da categoria "Men´s Footwear" no ano de 2012
filtro = (df["CategoriaNome"] == "Men´s Footwear") & (df["Ano"] == 2012)
df_filtrado = df[filtro]

# Agrupar por cliente e somar as vendas
clientes_vendas = df_filtrado.groupby("ClienteNome")["Vendas"].sum().sort_values(ascending=False)

# Agrupar por cidade e somar as vendas
cidades_vendas = df_filtrado.groupby("ClienteCidade")["Vendas"].sum().sort_values(ascending=False)

# Gráfico de barras - principais clientes
plt.figure(figsize=(10, 6))
clientes_vendas.plot(kind='bar', color='royalblue')
plt.title("Principais Clientes - Men´s Footwear em 2012")
plt.xlabel("Cliente")
plt.ylabel("Vendas ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gráfico de barras - cidades com vendas
plt.figure(figsize=(10, 6))
cidades_vendas.plot(kind='bar', color='darkorange')
plt.title("Cidades com Vendas - Men´s Footwear em 2012")
plt.xlabel("Cidade")
plt.ylabel("Vendas ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()