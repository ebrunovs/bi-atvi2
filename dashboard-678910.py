import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from dash import Dash, html

# Carregar os arquivos CSV
vendas_df = pd.read_csv('csv/VendasGlobais.csv')
vendedores_df = pd.read_csv('csv/Vendedores.csv')
fornecedores_df = pd.read_csv('csv/Fornecedores.csv')

# Mesclar os dados
vendas_df = vendas_df.merge(vendedores_df, on='VendedorID', how='left')
vendas_df = vendas_df.merge(fornecedores_df, on='FornecedorID', how='left')

# Converter coluna de data (formato DD/MM/YYYY no CSV)
vendas_df['Data'] = pd.to_datetime(vendas_df['Data'], format='%d/%m/%Y', errors='coerce')

# Garantir tipos numéricos para agregações
for col in ['Vendas', 'Desconto', 'Margem Bruta', 'Frete']:
    if col in vendas_df.columns:
        vendas_df[col] = pd.to_numeric(vendas_df[col], errors='coerce').fillna(0)

# Função para converter gráfico matplotlib em imagem base64
def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f'data:image/png;base64,{encoded}'

# Helper para plotar Series com fallback quando vazia
def plot_series_safe(s, kind='bar', title='', color=None, horizontal=False, figsize=(10, 6)):
    fig, ax = plt.subplots(figsize=figsize)
    if s is not None and len(s) > 0:
        if horizontal or kind == 'barh':
            s.plot(kind='barh', ax=ax, title=title, color=color)
        elif kind == 'line':
            s.plot(kind='line', ax=ax, title=title, color=color, marker='o')
        else:
            s.plot(kind=kind, ax=ax, title=title, color=color)
    else:
        ax.text(0.5, 0.5, 'Sem dados disponíveis', ha='center', va='center', fontsize=12)
        ax.set_title(title)
        ax.axis('off')
    plt.tight_layout()
    return fig

# 6. Vendedores que mais dão descontos nos EUA
eua_df = vendas_df[vendas_df['ClientePaís'] == 'USA']
desconto_por_vendedor = eua_df.groupby('VendedorNome')['Desconto'].sum().sort_values(ascending=False)
fig6 = plot_series_safe(desconto_por_vendedor, kind='bar', title='Vendedores que mais dão descontos nos EUA', color='skyblue')
img6 = fig_to_base64(fig6)

# 7. Fornecedores com maior margem de lucro no segmento 'Womens wear'
womens_df = vendas_df[vendas_df['CategoriaNome'] == 'Womens wear']
lucro_por_fornecedor = womens_df.groupby('FornecedorNome')['Margem Bruta'].sum().sort_values(ascending=False).head(10)
fig7 = plot_series_safe(lucro_por_fornecedor, kind='barh', title='Fornecedores com maior margem de lucro - Womens wear', color='pink', horizontal=True)
img7 = fig_to_base64(fig7)

# 8. Vendas totais em 2009 e análise entre 2009 e 2012
vendas_df['Ano'] = vendas_df['Data'].dt.year
vendas_ano = vendas_df[vendas_df['Ano'].between(2009, 2012, inclusive='both')]
vendas_por_ano = vendas_ano.groupby('Ano')['Vendas'].sum()
fig8 = plot_series_safe(vendas_por_ano, kind='line', title='Vendas Anuais (2009-2012)', color='green')
img8 = fig_to_base64(fig8)

# 9. Principais clientes do segmento 'Men´s Footwear' em 2012 e cidades envolvidas
mens_2012_df = vendas_df[(vendas_df['CategoriaNome'] == 'Men´s Footwear') & (vendas_df['Ano'] == 2012)]
if not mens_2012_df.empty:
    clientes_mens_2012 = mens_2012_df.groupby(['ClienteNome', 'ClienteCidade'])['Vendas'].sum().sort_values(ascending=False).head(10)
else:
    clientes_mens_2012 = pd.Series(dtype=float)
fig9 = plot_series_safe(clientes_mens_2012, kind='bar', title='Principais Clientes - Men´s Footwear em 2012', color='purple')
img9 = fig_to_base64(fig9)

# 10. Vendas por país na Europa
europa_paises = ['France', 'Germany', 'Italy', 'Spain', 'Portugal', 'Netherlands', 'Belgium', 'Sweden', 'Norway', 'Denmark', 'Finland', 'Austria', 'Switzerland', 'Ireland', 'UK', 'United Kingdom']
europa_df = vendas_df[vendas_df['ClientePaís'].isin(europa_paises)]
vendas_por_pais = europa_df.groupby('ClientePaís')['Vendas'].sum().sort_values(ascending=False)
fig10 = plot_series_safe(vendas_por_pais, kind='bar', title='Vendas por País na Europa', color='orange')
img10 = fig_to_base64(fig10)

# Criar o app Dash
app = Dash(__name__)

# Estilos CSS modernos
app.layout = html.Div(
    style={
        'fontFamily': 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
        'background': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'minHeight': '100vh',
        'padding': '20px',
        'margin': '0'
    },
    children=[
        html.Div([
            html.H1(
                ' Dashboard de Vendas - Análise Avançada',
                style={
                    'textAlign': 'center',
                    'color': 'white',
                    'marginBottom': '40px',
                    'fontSize': '48px',
                    'fontWeight': 'bold',
                    'textShadow': '2px 2px 4px rgba(0,0,0,0.3)'
                }
            )
        ]),
        html.Div(
            style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(500px, 1fr))',
                'gap': '30px',
                'marginBottom': '30px'
            },
            children=[
                html.Div([
                    html.H2(' Vendedores que mais dão descontos nos EUA', style={'color': '#2c3e50', 'fontSize': '22px', 'marginBottom': '15px', 'textAlign': 'center'}),
                    html.Img(src=img6, style={'width': '100%', 'borderRadius': '8px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'})
                ], style={'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '15px', 'boxShadow': '0 8px 16px rgba(0,0,0,0.2)'}),
                html.Div([
                    html.H2(' Fornecedores - Maior Margem (Womens wear)', style={'color': '#2c3e50', 'fontSize': '22px', 'marginBottom': '15px', 'textAlign': 'center'}),
                    html.Img(src=img7, style={'width': '100%', 'borderRadius': '8px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'})
                ], style={'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '15px', 'boxShadow': '0 8px 16px rgba(0,0,0,0.2)'})
            ]
        ),
        html.Div(
            style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(500px, 1fr))',
                'gap': '30px',
                'marginBottom': '30px'
            },
            children=[
                html.Div([
                    html.H2(' Evolução de Vendas Anuais (2009-2012)', style={'color': '#2c3e50', 'fontSize': '22px', 'marginBottom': '15px', 'textAlign': 'center'}),
                    html.Img(src=img8, style={'width': '100%', 'borderRadius': '8px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'})
                ], style={'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '15px', 'boxShadow': '0 8px 16px rgba(0,0,0,0.2)'}),
                html.Div([
                    html.H2(' Top Clientes - Men´s Footwear 2012', style={'color': '#2c3e50', 'fontSize': '22px', 'marginBottom': '15px', 'textAlign': 'center'}),
                    html.Img(src=img9, style={'width': '100%', 'borderRadius': '8px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'})
                ], style={'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '15px', 'boxShadow': '0 8px 16px rgba(0,0,0,0.2)'})
            ]
        ),
        html.Div(
            style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '40px'},
            children=[
                html.Div([
                    html.H2(' Vendas por País na Europa', style={'color': '#2c3e50', 'fontSize': '22px', 'marginBottom': '15px', 'textAlign': 'center'}),
                    html.Img(src=img10, style={'width': '100%', 'borderRadius': '8px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'})
                ], style={'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '15px', 'boxShadow': '0 8px 16px rgba(0,0,0,0.2)', 'maxWidth': '1100px', 'width': '100%'})
            ]
        ),
        html.Div([
            html.P(' 2025 Dashboard de Vendas - Business Intelligence | Análise Avançada', style={'textAlign': 'center', 'color': 'white', 'fontSize': '14px', 'marginTop': '20px', 'opacity': '0.8'})
        ])
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
