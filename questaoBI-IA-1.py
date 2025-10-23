import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados diretamente dos arquivos CSV
vendas_df = pd.read_csv("csv/VendasGlobais.csv")
vendedores_df = pd.read_csv("csv/Vendedores.csv")
transportadoras_df = pd.read_csv("csv/Transportadoras.csv")
fornecedores_df = pd.read_csv("csv/Fornecedores.csv")

# Agrupar por nome do cliente e somar as vendas
clientes_vendas = vendas_df.groupby("ClienteNome")["Vendas"].sum().sort_values(ascending=False)

# Selecionar os 10 maiores clientes
top_10_clientes = clientes_vendas.head(10)

# Criar gráfico de barras
plt.figure(figsize=(10, 6))
top_10_clientes.plot(kind='bar', color='skyblue')
plt.title("Top 10 Maiores Clientes em Termos de Vendas ($)")
plt.xlabel("Cliente")
plt.ylabel("Vendas Totais ($)")
plt.xticks(rotation=45)
plt.tight_layout()

# Exibir o gráfico
plt.show()