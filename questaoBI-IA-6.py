import pandas as pd
import matplotlib.pyplot as plt

# Carregar os arquivos CSV
vendas_df = pd.read_csv("csv/VendasGlobais.csv")
vendedores_df = pd.read_csv("csv/Vendedores.csv")

# Filtrar apenas os registros dos Estados Unidos
vendas_eua = vendas_df[vendas_df["ClientePaís"] == "USA"]

# Agrupar por VendedorID e somar os descontos
descontos_por_vendedor = vendas_eua.groupby("VendedorID")["Desconto"].sum().reset_index()

# Mesclar com os nomes dos vendedores
descontos_por_vendedor = descontos_por_vendedor.merge(vendedores_df, on="VendedorID")

# Ordenar por valor de desconto
descontos_por_vendedor = descontos_por_vendedor.sort_values(by="Desconto", ascending=False)

# Criar gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(descontos_por_vendedor["VendedorNome"], descontos_por_vendedor["Desconto"], color='salmon')
plt.title("Vendedores que Mais Concedem Descontos nos Estados Unidos")
plt.xlabel("Vendedor")
plt.ylabel("Total de Descontos ($)")
plt.xticks(rotation=45)
plt.tight_layout()

# Exibir o gráfico
plt.show()