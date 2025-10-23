import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo de vendas
vendas_df = pd.read_csv("csv/VendasGlobais.csv")

# Agrupar por país e somar as vendas
vendas_por_pais = vendas_df.groupby("ClientePaís")["Vendas"].sum().sort_values(ascending=False)

# Selecionar os três maiores países
top_3_paises = vendas_por_pais.head(3)

# Criar gráfico de barras
plt.figure(figsize=(8, 5))
top_3_paises.plot(kind='bar', color='orange')
plt.title("Top 3 Países em Termos de Vendas ($)")
plt.xlabel("País")
plt.ylabel("Vendas Totais ($)")
plt.xticks(rotation=0)
plt.tight_layout()

# Exibir o gráfico
plt.show()