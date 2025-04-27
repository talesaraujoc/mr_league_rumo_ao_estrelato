from dash import dash, html, dcc, page_container
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY, "https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"], use_pages=True, pages_folder="pages")


server = app.server


# Configuração da NavBar
navbar = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.NavbarBrand("X", className="ms-3"),
                width="auto"
            ),
            dbc.Col(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("HOME", href="/")),
                    dbc.NavItem(dbc.NavLink("Resumo da Rodada", href="/round_summary")),
                    dbc.NavItem(dbc.NavLink("Ranking de Jogadores", href="/player_ranking")),
                    dbc.NavItem(dbc.NavLink("Analítico por Jogador", href="/player_profile")),
                    #
                ], className="ms-auto", navbar=True),
                width="auto"
            )
        ], align="center", className="g-0 w-100 justify-content-between")
    ]),
    color="#38003D",
    dark=True,
    className="py-2"
)

# Layout principal
app.layout = html.Div([
    dbc.Row([
        # Navbar à esquerda
        dbc.Col(
            navbar,
            xs=10, sm=10, md=10, lg=10, xl=10,  # ocupa 10/12 em todas telas
            style={"paddingLeft": "20px"}
        ),

        # Logomarca à direita
        dbc.Col(
            html.Div(
                html.Img(src='assets/logo.png', style={"height": "50px", "width": "auto"}),
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "flex-end",
                    "paddingRight": "20px",
                    "width": "100%"
                }
            ),
            xs=2, sm=2, md=2, lg=2, xl=2,  # ocupa 2/12 em todas telas
        )
    ], 
    style={"backgroundColor": "#FFFFFF", "height": "80px", "alignItems": "center"},
    className="g-0 flex-nowrap"  # importante: impede quebra para baixo
    ),

    page_container
], style={"overflowX": "hidden"})  # opcional: impede scroll lateral




if __name__ == '__main__':
    app.run(debug=False)
