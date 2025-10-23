import pandas as pd
import matplotlib.pyplot as plt

# Carregar os arquivos CSV
vendas_df = pd.read_csv("csv/VendasGlobais.csv")
transportadoras_df = pd.read_csv("csv/Transportadoras.csv")

# Agrupar os dados de vendas por TransportadoraID e somar os valores de frete
frete_por_transportadora = vendas_df.groupby("TransportadoraID")["Frete"].sum().reset_index()

# Mesclar com os nomes das transportadoras
frete_por_transportadora = frete_por_transportadora.merge(transportadoras_df, on="TransportadoraID")

# Ordenar por despesa de frete
frete_por_transportadora = frete_por_transportadora.sort_values(by="Frete", ascending=False)

# Criar gráfico de barras
plt.figure(figsize=(8, 5))
plt.bar(frete_por_transportadora["TransportadoraNome"], frete_por_transportadora["Frete"], color='steelblue')
plt.title("Despesa com Frete por Transportadora")
plt.xlabel("Transportadora")
plt.ylabel("Despesa Total com Frete ($)")
plt.xticks(rotation=45)
plt.tight_layout()

# Exibir o gráfico
plt.show()