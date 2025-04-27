from dash import dash, html, dcc, Output, Input, State, dash_table, callback, register_page
import dash_bootstrap_components as dbc

import pandas as pd
import plotly as plt
from datetime import date
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash_ag_grid as dag

from src.globals import *


# Dash
register_page(__name__, name="test", path='/model_page')



# DataFrame =================



########## Pré-layout ================



# Layout    =================
#app.layout = html.Div([
layout = html.Div([], className="main-container")


# Callbacks =================
#@callback(
#    Output('dcc-two_suboptions_dcc-one', 'options'),
#    Input('dcc-one_tipo_feature', 'value')
#)