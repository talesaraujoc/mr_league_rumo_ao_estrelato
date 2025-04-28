from dash import html, dcc, register_page, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from src.data_loader import carregar_dados_google_sheets

# Registrar esta página
register_page(__name__, path="/round_summary", name="Resumo da Rodada")

# Lista de critérios disponíveis
criterios_disponiveis = ['GOL', 'ASS', 'FALTA', 'GC', 'AMA', 'AZUL', 'VER', 'PP', 'GS', 'DD', 'DP']

# Layout
layout = dbc.Container([
    # PRIMEIRA ROW: Filtros + Gráfico V/E/D
    dbc.Row([
        # Coluna de filtros
        dbc.Col([
            html.Div([
                html.Label("Competição:", className="fw-bold", style={"color": "#38003D"}),
                dcc.RadioItems(
                    id='competicao-round',
                    options=[
                        {"label": "LIGA", "value": "LIGA"},
                        {"label": "COPA", "value": "COPA"}
                    ],
                    value="LIGA",
                    inline=False,
                    style={"marginBottom": "20px"}
                ),
                html.Label("Rodada:", className="fw-bold", style={"color": "#38003D"}),
                dcc.Dropdown(
                    id='dropdown-rodada-round',
                    options=[],
                    value=None,
                    placeholder="Selecione a rodada",
                    clearable=False,
                    style={"marginBottom": "20px"}
                ),
                html.Label("Critério:", className="fw-bold", style={"color": "#38003D"}),
                dcc.Dropdown(
                    id='dropdown-criterio-round',
                    options=[{"label": criterio, "value": criterio} for criterio in criterios_disponiveis],
                    value="GOL",
                    clearable=False
                )
            ], style={"padding": "10px", "backgroundColor": "#F8F9FA", "borderRadius": "10px"})
        ], md=3),

        # Coluna do gráfico V/E/D
        dbc.Col([
            dcc.Graph(id='grafico-ved-round')
        ], md=9)
    ], className="my-4"),

    # SEGUNDA ROW: Gráfico de Scout
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='grafico-criterio-round')
        ], md=12)
    ])
], fluid=True)

# Callback para preencher rodadas disponíveis
@callback(
    Output('dropdown-rodada-round', 'options'),
    Output('dropdown-rodada-round', 'value'),
    Input('competicao-round', 'value')
)
def atualizar_rodadas(competicao):
    df_full = carregar_dados_google_sheets()
    df = df_full[df_full['COMPETIÇÃO'] == competicao]
    rodadas = sorted(df['RODADA'].unique())
    options = [{"label": str(rodada), "value": rodada} for rodada in rodadas]
    value = rodadas[0] if rodadas else None
    return options, value

# Callback para atualizar os gráficos
@callback(
    Output('grafico-ved-round', 'figure'),
    Output('grafico-criterio-round', 'figure'),
    Input('competicao-round', 'value'),
    Input('dropdown-rodada-round', 'value'),
    Input('dropdown-criterio-round', 'value')
)
def atualizar_graficos_round(competicao, rodada, criterio):
    if rodada is None:
        return {}, {}

    df_full = carregar_dados_google_sheets()
    df = df_full[(df_full['COMPETIÇÃO'] == competicao) & (df_full['RODADA'] == str(rodada))]

    # Gráfico V/E/D por Time
    ved_data = df.groupby(['TIME', 'PARTIDA'])[['V', 'E', 'D']].max().reset_index()
    ved_data = ved_data.groupby('TIME')[['V', 'E', 'D']].sum().reset_index()
    ved_data = ved_data.melt(id_vars='TIME', value_vars=['V', 'E', 'D'], var_name='Resultado', value_name='Quantidade')

    fig_ved = px.bar(
        ved_data, x='TIME', y='Quantidade', color='Resultado',
        color_discrete_map={
            "V": "#5D9231",     # Verde suave (Vitória)
            "E": "#BDA65E",     # Dourado opaco (Empate)
            "D": "#FF5C5C"      # Vermelho suave (Derrota)
        },
        barmode='group',
        title=f"Resultados da Rodada {rodada} - {competicao}",
        template='plotly_white',
        text_auto=True
    )

    fig_ved.update_traces(
        marker_line_width=1,
        marker_line_color="white",
        selector=dict(type='bar')
    )

    fig_ved.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='#38003D',
        title_x=0.5,
        xaxis_title=None,
        yaxis_title=None,
        bargap=0.25,
        bargroupgap=0.1
    )

    # Gráfico Critério selecionado
    criterio_data = df.groupby('PLAYER')[criterio].sum().reset_index()
    criterio_data = criterio_data[criterio_data[criterio] > 0]

    fig_criterio = px.bar(
        criterio_data, x=criterio, y='PLAYER',
        orientation='h',
        title=f"{criterio} - Rodada {rodada} ({competicao})",
        template='plotly_white',
        color_discrete_sequence=["#38003D"],
        text_auto=True
    )
    fig_criterio.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='#38003D',
        title_x=0.5,
        yaxis_title=None
    )

    return fig_ved, fig_criterio
