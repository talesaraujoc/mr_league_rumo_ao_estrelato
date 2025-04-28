from dash import html, dcc, register_page, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from src.data_loader import carregar_dados_google_sheets

# Registrar esta página
register_page(__name__, path="/")

# Layout da página
layout = dbc.Container([
    # Cards de informações
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H6("Total de Partidas", className="card-title text-white mb-2", style={"fontSize": "16px"}),
                    html.H3(id='total-partidas', className="card-text text-white", style={"fontSize": "26px"})
                ])
            ], style={"backgroundColor": "#38003D", "border": "none", "borderRadius": "10px", "padding": "10px"}),
            xs=12, sm=6, md=3, className="mb-3"
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H6("1° Colocado Geral", className="card-title text-dark mb-2", style={"fontSize": "16px"}),
                    html.H5(id='primeiro-colocado', className="card-text text-dark", style={"fontSize": "20px"})
                ])
            ], style={"backgroundColor": "#BDE79A", "border": "none", "borderRadius": "10px", "padding": "10px"}),
            xs=12, sm=6, md=3, className="mb-3"
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H6("Total de Gols", className="card-title text-white mb-2", style={"fontSize": "16px"}),
                    html.H3(id='total-gols', className="card-text text-white", style={"fontSize": "26px"})
                ])
            ], style={"backgroundColor": "#5D9231", "border": "none", "borderRadius": "10px", "padding": "10px"}),
            xs=12, sm=6, md=3, className="mb-3"
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H6("Quantidade de Rodadas", className="card-title text-white mb-2", style={"fontSize": "16px"}),
                    html.H3(id='quantidade-rodadas', className="card-text text-white", style={"fontSize": "26px"})
                ])
            ], style={"backgroundColor": "#751F7D", "border": "none", "borderRadius": "10px", "padding": "10px"}),
            xs=12, sm=6, md=3, className="mb-3"
        ),
    ], className="my-4"),

    # Dropdowns de filtros
    dbc.Row([
        dbc.Col([
            html.Label("Filtrar por Competição:", className="mb-2 fw-bold", style={"color": "#38003D"}),
            dcc.Dropdown(
                id='dropdown-competicao',
                options=[
                    {"label": "Todas", "value": "Todas"},
                    {"label": "LIGA", "value": "LIGA"},
                    {"label": "COPA", "value": "COPA"}
                ],
                value="Todas",
                clearable=False,
                style={"width": "80%"}
            )
        ], md=6),

        dbc.Col([
            html.Label("Escolher Métrica:", className="mb-2 fw-bold", style={"color": "#38003D"}),
            dcc.Dropdown(
                id='dropdown-metrica',
                options=[
                    {"label": "Gols", "value": "GOL"},
                    {"label": "Assistências", "value": "ASS"}
                ],
                value="GOL",
                clearable=False,
                style={"width": "80%"}
            )
        ], md=6)
    ]),

    # Gráficos
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='grafico-top5-pts'),
            md=6
        ),
        dbc.Col(
            dcc.Graph(id='grafico-top5-metrica'),
            md=6
        ),
    ])
], fluid=True)

# Callback para atualizar todos os dados
@callback(
    Output('grafico-top5-pts', 'figure'),
    Output('grafico-top5-metrica', 'figure'),
    Output('total-partidas', 'children'),
    Output('primeiro-colocado', 'children'),
    Output('total-gols', 'children'),
    Output('quantidade-rodadas', 'children'),
    Input('dropdown-competicao', 'value'),
    Input('dropdown-metrica', 'value')
)
def atualizar_graficos(competicao, metrica):

    df_full = carregar_dados_google_sheets()

    if competicao == "Todas":
        df = df_full.copy()
    else:
        df = df_full[df_full['COMPETIÇÃO'] == competicao]

    # Estatísticas
    total_partidas = df['PARTIDA'].nunique()
    total_gols = df['GOL'].sum()
    quantidade_rodadas = df['RODADA'].nunique()

    # Top 1 jogador
    if df.empty:
        top1 = "Sem dados"
    else:
        top1 = df.groupby('PLAYER')['PTS'].sum().sort_values(ascending=False).index[0]

    # Gráfico Top 5 Pontos
    top5_pts = df.groupby('PLAYER')['PTS'].sum().sort_values(ascending=False).head(5).reset_index()
    fig_top5_pts = px.bar(
        top5_pts, x='PTS', y='PLAYER',
        orientation='h',
        title=f"Top 5 Jogadores - Pontos ({competicao})",
        labels={'PTS': 'Pontos', 'PLAYER': 'Jogador'},
        template='plotly_white',
        color_discrete_sequence=["#38003D"],
        text_auto=True
    )
    fig_top5_pts.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='#38003D',
        title_font_size=20,
        title_x=0.5,
        xaxis_title=None,
        yaxis_title=None,
        xaxis=dict(title="Pontos", title_font_size=14)
    )

    # Gráfico Top 5 Métrica (GOL ou ASS)
    top5_metrica = df.groupby('PLAYER')[metrica].sum().sort_values(ascending=False).head(5).reset_index()
    fig_top5_metrica = px.bar(
        top5_metrica, x=metrica, y='PLAYER',
        orientation='h',
        title=f"Top 5 Jogadores - {'Gols' if metrica == 'GOL' else 'Assistências'} ({competicao})",
        labels={metrica: 'Quantidade', 'PLAYER': 'Jogador'},
        template='plotly_white',
        color_discrete_sequence=["#5D9231"],
        text_auto=True
    )
    fig_top5_metrica.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='#38003D',
        title_font_size=20,
        title_x=0.5,
        xaxis_title=None,
        yaxis_title=None,
        xaxis=dict(title="Quantidade", title_font_size=14)
    )

    return fig_top5_pts, fig_top5_metrica, total_partidas, top1, total_gols, quantidade_rodadas
