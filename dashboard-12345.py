import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from dash import Dash, html

# Carregar os arquivos CSV
vendas_df = pd.read_csv("csv/VendasGlobais.csv")
transportadoras_df = pd.read_csv("csv/Transportadoras.csv")

# Mesclar os dados de vendas com transportadoras
vendas_df = vendas_df.merge(transportadoras_df, on="TransportadoraID", how="left")

# Normalizar nomes de colunas esperadas do CSV
# VendasGlobais.csv tem colunas: ClienteNome, ClientePaís, ClientePaísID, CategoriaNome, Vendas, Frete, ...
# Transportadoras.csv tem colunas: TransportadoraID, TransportadoraNome
# Garantir tipos numéricos para agregações
for col in ["Vendas", "Frete"]:
    if col in vendas_df.columns:
        vendas_df[col] = pd.to_numeric(vendas_df[col], errors="coerce").fillna(0)

# Função para converter gráfico matplotlib em imagem base64
def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return f"data:image/png;base64,{encoded}"

# Helper para plotar Series com fallback quando vazia
def plot_series_safe(s, kind="bar", title="", color=None, horizontal=False):
    fig, ax = plt.subplots()
    if s is not None and len(s) > 0:
        if horizontal or kind == "barh":
            s.plot(kind="barh", ax=ax, title=title, color=color)
        else:
            s.plot(kind="bar", ax=ax, title=title, color=color)
    else:
        ax.text(0.5, 0.5, "Sem dados", ha="center", va="center", fontsize=12)
        ax.set_title(title)
        ax.axis("off")
    return fig

# 1. Top 10 clientes por vendas ($)
top_clientes = vendas_df.groupby("ClienteNome")["Vendas"].sum().nlargest(10)
fig1 = plot_series_safe(top_clientes, kind="bar", title="Top 10 Clientes por Vendas ($)")
img1 = fig_to_base64(fig1)

# 2. Top 3 países por vendas ($)
top_paises = vendas_df.groupby("ClientePaís")["Vendas"].sum().nlargest(3)
fig2 = plot_series_safe(top_paises, kind="bar", title="Top 3 Países por Vendas ($)", color="orange")
img2 = fig_to_base64(fig2)

# 3. Categorias com maior faturamento no Brasil
# No CSV o país está em inglês (Brazil). Categoria é "CategoriaNome" e o valor é "Vendas".
brasil_df = vendas_df[vendas_df["ClientePaís"] == "Brazil"]
categorias_br = brasil_df.groupby("CategoriaNome")["Vendas"].sum().sort_values(ascending=True)
fig3 = plot_series_safe(categorias_br, kind="barh", title="Faturamento por Categoria no Brasil", color="green", horizontal=True)
img3 = fig_to_base64(fig3)

# 4. Despesa com frete por transportadora
frete_por_transportadora = vendas_df.groupby("TransportadoraNome")["Frete"].sum().sort_values(ascending=False)
fig4 = plot_series_safe(frete_por_transportadora, kind="bar", title="Despesa com Frete por Transportadora", color="red")
img4 = fig_to_base64(fig4)

# 5. Principais clientes do segmento “Men´s Footwear” na Germany
# Categoria no CSV: "Men´s Footwear" (com acento) e país: "Germany"
segmento_df = vendas_df[(vendas_df["CategoriaNome"] == "Men´s Footwear") & (vendas_df["ClientePaís"] == "Germany")]
clientes_segmento = segmento_df.groupby("ClienteNome")["Vendas"].sum().nlargest(10)
fig5 = plot_series_safe(clientes_segmento, kind="bar", title="Principais Clientes - Men´s Footwear na Alemanha (Germany)", color="purple")
img5 = fig_to_base64(fig5)

# Criar o app Dash
app = Dash(__name__)

# Estilos CSS modernos
app.layout = html.Div(
    style={
        "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "minHeight": "100vh",
        "padding": "20px",
        "margin": "0"
    },
    children=[
        # Cabeçalho
        html.Div([
            html.H1(
                "📊 Dashboard de Vendas",
                style={
                    "textAlign": "center",
                    "color": "white",
                    "marginBottom": "40px",
                    "fontSize": "48px",
                    "fontWeight": "bold",
                    "textShadow": "2px 2px 4px rgba(0,0,0,0.3)"
                }
            )
        ]),
        
        # Grid de gráficos - Primeira linha (2 gráficos)
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(500px, 1fr))",
                "gap": "30px",
                "marginBottom": "30px"
            },
            children=[
                # Card 1
                html.Div([
                    html.H2(
                        "🏆 Top 10 Clientes por Vendas",
                        style={
                            "color": "#2c3e50",
                            "fontSize": "22px",
                            "marginBottom": "15px",
                            "textAlign": "center"
                        }
                    ),
                    html.Img(
                        src=img1,
                        style={"width": "100%", "borderRadius": "8px", "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"}
                    )
                ], style={
                    "backgroundColor": "white",
                    "padding": "25px",
                    "borderRadius": "15px",
                    "boxShadow": "0 8px 16px rgba(0,0,0,0.2)",
                    "transition": "transform 0.3s ease"
                }),
                
                # Card 2
                html.Div([
                    html.H2(
                        "🌍 Top 3 Países por Vendas",
                        style={
                            "color": "#2c3e50",
                            "fontSize": "22px",
                            "marginBottom": "15px",
                            "textAlign": "center"
                        }
                    ),
                    html.Img(
                        src=img2,
                        style={"width": "100%", "borderRadius": "8px", "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"}
                    )
                ], style={
                    "backgroundColor": "white",
                    "padding": "25px",
                    "borderRadius": "15px",
                    "boxShadow": "0 8px 16px rgba(0,0,0,0.2)"
                })
            ]
        ),
        
        # Segunda linha (2 gráficos)
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(500px, 1fr))",
                "gap": "30px",
                "marginBottom": "30px"
            },
            children=[
                # Card 3
                html.Div([
                    html.H2(
                        "🇧🇷 Faturamento por Categoria no Brasil",
                        style={
                            "color": "#2c3e50",
                            "fontSize": "22px",
                            "marginBottom": "15px",
                            "textAlign": "center"
                        }
                    ),
                    html.Img(
                        src=img3,
                        style={"width": "100%", "borderRadius": "8px", "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"}
                    )
                ], style={
                    "backgroundColor": "white",
                    "padding": "25px",
                    "borderRadius": "15px",
                    "boxShadow": "0 8px 16px rgba(0,0,0,0.2)"
                }),
                
                # Card 4
                html.Div([
                    html.H2(
                        "🚚 Despesa com Frete por Transportadora",
                        style={
                            "color": "#2c3e50",
                            "fontSize": "22px",
                            "marginBottom": "15px",
                            "textAlign": "center"
                        }
                    ),
                    html.Img(
                        src=img4,
                        style={"width": "100%", "borderRadius": "8px", "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"}
                    )
                ], style={
                    "backgroundColor": "white",
                    "padding": "25px",
                    "borderRadius": "15px",
                    "boxShadow": "0 8px 16px rgba(0,0,0,0.2)"
                })
            ]
        ),
        
        # Terceira linha (1 gráfico centralizado)
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "center",
                "marginBottom": "40px"
            },
            children=[
                # Card 5
                html.Div([
                    html.H2(
                        "👞 Principais Clientes - Calçados Masculinos na Alemanha",
                        style={
                            "color": "#2c3e50",
                            "fontSize": "22px",
                            "marginBottom": "15px",
                            "textAlign": "center"
                        }
                    ),
                    html.Img(
                        src=img5,
                        style={"width": "100%", "borderRadius": "8px", "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"}
                    )
                ], style={
                    "backgroundColor": "white",
                    "padding": "25px",
                    "borderRadius": "15px",
                    "boxShadow": "0 8px 16px rgba(0,0,0,0.2)",
                    "maxWidth": "1100px",
                    "width": "100%"
                })
            ]
        ),
        
        # Rodapé
        html.Div([
            html.P(
                "© 2025 Dashboard de Vendas - Business Intelligence",
                style={
                    "textAlign": "center",
                    "color": "white",
                    "fontSize": "14px",
                    "marginTop": "20px",
                    "opacity": "0.8"
                }
            )
        ])
    ]
)

# Executar o servidor
if __name__ == "__main__":
    app.run(debug=True)