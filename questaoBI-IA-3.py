import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo CSV
vendas_df = pd.read_csv("csv/VendasGlobais.csv")

# Filtrar apenas os registros do Brasil
vendas_brasil = vendas_df[vendas_df["ClientePaísID"].astype(str).str.upper() == "BRA"]

# Agrupar por categoria e somar as vendas
faturamento_por_categoria = vendas_brasil.groupby("CategoriaNome")["Vendas"].sum().sort_values(ascending=False)

# Criar gráfico de barras
plt.figure(figsize=(10, 6))
faturamento_por_categoria.plot(kind='bar', color='green')
plt.title("Categorias de Produtos com Maior Faturamento no Brasil")
plt.xlabel("Categoria")
plt.ylabel("Faturamento Total (Vendas $)")
plt.xticks(rotation=45)
plt.tight_layout()

# Exibir o gráfico
plt.show()