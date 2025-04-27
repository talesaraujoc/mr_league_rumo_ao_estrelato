from dash import html, dcc, register_page, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from src.data_loader import carregar_dados_google_sheets
import pandas as pd

# Registrar a página
register_page(__name__, path="/player_profile", name="Analítico por Jogador")

# Carrega os dados
df_full = carregar_dados_google_sheets()

# Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            #html.H2("Analítico por Jogador", className="text-center my-4", style={"color": "#38003D"}),
            dcc.Dropdown(
                id='dropdown-jogador',
                options=[{"label": jogador, "value": jogador} for jogador in sorted(df_full['PLAYER'].unique())],
                placeholder="Selecione um jogador",
                style={"marginBottom": "20px"}
            )
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='grafico-pontos-rodada')
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.Div(id='cartoes-estatisticas', className="d-flex flex-wrap justify-content-center gap-3")
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H4("Médias da Competição", className="text-center my-4", style={"color": "#38003D"}),
            html.Div(id='cartoes-medias', className="d-flex flex-wrap justify-content-center gap-3")
        ], width=12)
    ])
], fluid=True)

# Callback principal
@callback(
    Output('grafico-pontos-rodada', 'figure'),
    Output('cartoes-estatisticas', 'children'),
    Output('cartoes-medias', 'children'),
    Input('dropdown-jogador', 'value')
)
def atualizar_perfil(jogador):
    if jogador is None:
        return {}, [], []

    df_jogador = df_full[df_full['PLAYER'] == jogador]

    # 🎯 Agrupamento de pontos por rodada
    df_agrupado = df_jogador.groupby('RODADA')['PTS'].sum().reset_index()

    # Gráfico de Pontos por Rodada (agregado)
    fig = px.line(
        df_agrupado,
        x='RODADA',
        y='PTS',
        title=f"Pontos por Rodada - {jogador}",
        markers=True,
        template='plotly_white'
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='#38003D',
        title_x=0.5
    )

    # Estatísticas agregadas do jogador
    stats = df_jogador.agg({
        'GOL': 'sum',
        'ASS': 'sum',
        'V': 'sum',
        'E': 'sum',
        'D': 'sum',
        'STG': 'sum',
        'GS': 'sum',
        'DD': 'sum',
        'DP': 'sum'
    }).to_dict()

    # Detecta se é Goleiro (GK)
    posicao = df_jogador['POSIÇÃO'].iloc[0]
    cartoes = []

    # Cartões das estatísticas principais
    cartoes.extend([
        criar_cartao('Gols', stats['GOL']),
        criar_cartao('Assistências', stats['ASS']),
        criar_cartao('Vitórias', stats['V']),
        criar_cartao('Empates', stats['E']),
        criar_cartao('Derrotas', stats['D']),
        criar_cartao('Sem sofrer gols (STG)', stats['STG']),
    ])

    if posicao == 'GK':
        cartoes.extend([
            criar_cartao('Gols Sofridos (GS)', stats['GS']),
            criar_cartao('Defesas Difíceis (DD)', stats['DD']),
            criar_cartao('Pênaltis Defendidos (DP)', stats['DP']),
        ])

    # Médias da competição
    medias = df_full.groupby('PLAYER').agg({
        'GOL': 'sum',
        'ASS': 'sum',
        'V': 'sum',
        'E': 'sum',
        'D': 'sum',
        'STG': 'sum'
    }).mean().round(2).to_dict()

    cartoes_medias = [
        criar_cartao(f"Média de Gols", medias['GOL']),
        criar_cartao(f"Média de Assistências", medias['ASS']),
        criar_cartao(f"Média de Vitórias", medias['V']),
        criar_cartao(f"Média de Empates", medias['E']),
        criar_cartao(f"Média de Derrotas", medias['D']),
        criar_cartao(f"Média de STG", medias['STG']),
    ]

    return fig, cartoes, cartoes_medias

# Função para criar cartões de estatísticas
def criar_cartao(titulo, valor):
    return dbc.Card([
        dbc.CardBody([
            html.H6(titulo, className="card-title text-center", style={"color": "#38003D"}),
            html.H3(int(valor) if pd.notnull(valor) else 0, className="card-text text-center", style={"color": "#38003D"})
        ])
    ], style={"width": "180px", "backgroundColor": "#F8F9FA", "border": "1px solid #E6E6E6", "borderRadius": "10px"})
