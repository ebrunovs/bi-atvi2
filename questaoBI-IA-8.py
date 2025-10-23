import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo CSV
df = pd.read_csv("csv/VendasGlobais.csv")

# Converter a coluna 'Data' para datetime
df["Data"] = pd.to_datetime(df["Data"], errors="coerce", dayfirst=True)

# Remover linhas com datas inválidas
df = df.dropna(subset=["Data"])

# Extrair o ano da data
df["Ano"] = df["Data"].dt.year

# Filtrar vendas entre 2009 e 2012
df_periodo = df[df["Ano"].between(2009, 2012)]

# Agrupar por ano e somar as vendas
vendas_anuais = df_periodo.groupby("Ano")["Vendas"].sum().sort_index()

# Total vendido em 2009
vendas_2009 = vendas_anuais.loc[2009]
print(f"Total vendido em 2009: ${vendas_2009:,.2f}")

# Exibir vendas anuais
print("\nVendas anuais entre 2009 e 2012:")
print(vendas_anuais)

# Análise de tendência
if vendas_anuais.is_monotonic_increasing:
    tendencia = "crescendo"
elif vendas_anuais.is_monotonic_decreasing:
    tendencia = "decaindo"
else:
    tendencia = "estável ou variável"

print(f"\nConclusão: O faturamento está {tendencia} entre 2009 e 2012.")

# Gerar gráfico de linha
plt.figure(figsize=(8, 5))
plt.plot(vendas_anuais.index, vendas_anuais.values, marker='o', linestyle='-', color='blue')
plt.title("Vendas Anuais (2009–2012)")
plt.xlabel("Ano")
plt.ylabel("Vendas Totais ($)")
plt.grid(True)
plt.tight_layout()
plt.show()