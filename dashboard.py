import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Carregar os dados
ocorrencias = pd.read_csv('ocorrencia_clean.csv', sep=';')
recomendacoes = pd.read_csv('recomendacao_clean.csv', sep=';')
fatores = pd.read_csv('fator_contribuinte_clean.csv', sep=';')

# Conversão de colunas numéricas (latitude e longitude)
ocorrencias['ocorrencia_latitude'] = pd.to_numeric(ocorrencias['ocorrencia_latitude'], errors='coerce')
ocorrencias['ocorrencia_longitude'] = pd.to_numeric(ocorrencias['ocorrencia_longitude'], errors='coerce')

# Aplicativo Dash
app = dash.Dash(__name__)

# Layout do app
app.layout = html.Div([
    html.H1("Dashboards de Segurança Aeronáutica"),
    
    # Dropdown para selecionar dashboard
    dcc.Dropdown(
        id='dashboard-selector',
        options=[
            {'label': 'Ocorrências Aeronáuticas', 'value': 'ocorrencias'},
            {'label': 'Recomendações de Segurança', 'value': 'recomendacoes'},
            {'label': 'Fatores Contribuintes', 'value': 'fatores'},
        ],
        value='ocorrencias',
        style={'width': '50%'}
    ),
    html.Div(id='dashboard-content')
])

# Callback para atualizar o dashboard
@app.callback(
    Output('dashboard-content', 'children'),
    [Input('dashboard-selector', 'value')]
)
def update_dashboard(dashboard):
    if dashboard == 'ocorrencias':
        # Mapa de ocorrências
        fig_map = px.scatter_mapbox(
            ocorrencias,
            lat='ocorrencia_latitude',
            lon='ocorrencia_longitude',
            color='ocorrencia_classificacao',
            hover_name='ocorrencia_cidade',
            title="Mapa de Ocorrências",
            mapbox_style="open-street-map",
            zoom=3
        )
        
        # Gráfico de barras por estado
        uf_counts = ocorrencias['ocorrencia_uf'].value_counts().reset_index()
        uf_counts.columns = ['Estado', 'Quantidade']
        
        fig_barras = px.bar(
            uf_counts,
            x='Estado',
            y='Quantidade',
            title='Ocorrências por Estado',
            labels={'Estado': 'Estado', 'Quantidade': 'Quantidade'}
        )
        
        return html.Div([
            dcc.Graph(figure=fig_map),
            dcc.Graph(figure=fig_barras)
        ])
    
    elif dashboard == 'recomendacoes':
        # Gráfico de status de recomendações
        fig_status = px.pie(
            recomendacoes,
            names='recomendacao_status',
            title='Status das Recomendações'
        )
        
        # Gráfico de barras de destinatários
        dest_counts = recomendacoes['recomendacao_destinatario_sigla'].value_counts().reset_index()
        dest_counts.columns = ['Destinatário', 'Quantidade']
        
        fig_dest = px.bar(
            dest_counts,
            x='Destinatário',
            y='Quantidade',
            title='Recomendações por Destinatário',
            labels={'Destinatário': 'Destinatário', 'Quantidade': 'Quantidade'}
        )
        
        return html.Div([
            dcc.Graph(figure=fig_status),
            dcc.Graph(figure=fig_dest)
        ])
    
    elif dashboard == 'fatores':
        # Gráfico de barras de fatores mais frequentes
        fator_counts = fatores['fator_nome'].value_counts().reset_index()
        fator_counts.columns = ['Fator', 'Quantidade']
        
        fig_fatores = px.bar(
            fator_counts,
            x='Fator',
            y='Quantidade',
            title='Fatores Contribuintes Mais Frequentes',
            labels={'Fator': 'Fator', 'Quantidade': 'Quantidade'}
        )
        
        # Gráfico de pizza de áreas afetadas
        fig_areas = px.pie(
            fatores,
            names='fator_area',
            title='Distribuição por Área Afetada'
        )
        
        return html.Div([
            dcc.Graph(figure=fig_fatores),
            dcc.Graph(figure=fig_areas)
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
