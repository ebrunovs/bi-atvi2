import pandas as pd
import matplotlib.pyplot as plt

# Carregar os arquivos CSV
vendas_df = pd.read_csv("csv/VendasGlobais.csv")
fornecedores_df = pd.read_csv("csv/Fornecedores.csv")

# Filtrar apenas registros da categoria "Womens wear"
womens_wear_df = vendas_df[vendas_df["CategoriaNome"] == "Womens wear"]

# Agrupar por FornecedorID e somar a Margem Bruta
margem_por_fornecedor = womens_wear_df.groupby("FornecedorID")["Margem Bruta"].sum().reset_index()

# Mesclar com os nomes dos fornecedores
margem_por_fornecedor = margem_por_fornecedor.merge(fornecedores_df, on="FornecedorID")

# Ordenar por margem de lucro decrescente
margem_por_fornecedor = margem_por_fornecedor.sort_values(by="Margem Bruta", ascending=False)

# Criar gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(margem_por_fornecedor["FornecedorNome"], margem_por_fornecedor["Margem Bruta"], color='mediumseagreen')
plt.title("Fornecedores com Maior Margem de Lucro no Segmento 'Womens wear'")
plt.xlabel("Fornecedor")
plt.ylabel("Margem de Lucro Total ($)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Exibir o gráfico
plt.show()