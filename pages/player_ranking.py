from dash import html, dcc, register_page, Output, Input, callback
import dash_bootstrap_components as dbc
from dash import dash_table
from src.data_loader import carregar_dados_google_sheets
import pandas as pd

# Registrar esta página
register_page(__name__, path="/player_ranking", name="Ranking de Jogadores")

# Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H5("Ranking Geral", className="text-center my-4", style={"color": "#38003D"}),
            dash_table.DataTable(
                id='tabela-ranking',
                columns=[
                    {"name": "Posição", "id": "Posição"},
                    {"name": "Jogador", "id": "PLAYER"},
                    # {"name": "Função", "id": "POSIÇÃO"},  # se quiser adicionar
                    {"name": "Partidas", "id": "PARTIDAS"},
                    {"name": "V", "id": "V"},
                    {"name": "E", "id": "E"},
                    {"name": "D", "id": "D"},
                    {"name": "STG", "id": "STG"},
                    {"name": "Gols", "id": "GOL"},
                    {"name": "Assistências", "id": "ASS"},
                    {"name": "Pontos", "id": "PTS"}
                ],
                style_cell={
                    'textAlign': 'center',
                    'padding': '8px',
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '15px'
                },
                style_header={
                    'backgroundColor': '#38003D',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'fontSize': '16px',
                    'textAlign': 'center'
                },
                style_data={
                    'backgroundColor': 'white',
                    'color': '#38003D'
                },
                style_table={
                    'overflowX': 'auto',
                    'border': '1px solid #E6E6E6'
                },
                page_size=25,
                sort_action="native",
                sort_mode="multi",
                style_data_conditional=[
                    {
                        'if': {'filter_query': '{Posição} = 1'},
                        'backgroundColor': '#FFD700',  # Ouro para o 1º lugar
                        'color': 'black',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {'filter_query': '{Posição} = 2'},
                        'backgroundColor': '#C0C0C0',  # Prata para o 2º
                        'color': 'black',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {'filter_query': '{Posição} = 3'},
                        'backgroundColor': '#CD7F32',  # Bronze para o 3º
                        'color': 'black',
                        'fontWeight': 'bold'
                    }
                ]
            )
        ])
    ])
], fluid=True)

# Callback para carregar a tabela
@callback(
    Output('tabela-ranking', 'data'),
    Input('tabela-ranking', 'id')  # Dummy Input só para ativar o callback no carregamento
)
def carregar_tabela(_):
    df_full = carregar_dados_google_sheets()

    # Número de partidas jogadas (considera 1 linha = 1 jogo por jogador)
    partidas_jogadas = df_full.groupby('PLAYER').size().reset_index(name='PARTIDAS')

    # Agrupar somas de estatísticas por jogador
    df_ranking = df_full.groupby(['PLAYER', 'POSIÇÃO']).agg({
        'V': 'sum',
        'E': 'sum',
        'D': 'sum',
        'STG': 'sum',
        'GOL': 'sum',
        'ASS': 'sum',
        'PTS': 'sum'
    }).reset_index()

    # Merge para incluir a quantidade de partidas
    df_ranking = df_ranking.merge(partidas_jogadas, on='PLAYER', how='left')

    # Ordenar pela pontuação de forma decrescente
    df_ranking = df_ranking.sort_values(by='PTS', ascending=False).reset_index(drop=True)

    # Criar uma coluna de posição no ranking
    df_ranking.insert(0, 'Posição', df_ranking.index + 1)

    return df_ranking.to_dict('records')
