import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo CSV
df = pd.read_csv("csv/VendasGlobais.csv")

# Filtrar registros da categoria "Men´s Footwear" e país "Germany"
filtro = (df["CategoriaNome"] == "Men´s Footwear") & (df["ClientePaís"] == "Germany")
df_filtrado = df[filtro]

# Agrupar por cliente e somar as vendas
clientes_vendas = df_filtrado.groupby("ClienteNome")["Vendas"].sum().sort_values(ascending=False)

# Selecionar os principais clientes
top_clientes = clientes_vendas.head(10)

# Criar gráfico de barras
plt.figure(figsize=(10, 6))
top_clientes.plot(kind='bar', color='teal')
plt.title("Principais Clientes do Segmento 'Men´s Footwear' na Alemanha")
plt.xlabel("Cliente")
plt.ylabel("Vendas Totais ($)")
plt.xticks(rotation=45)
plt.tight_layout()

# Exibir o gráfico
plt.show()