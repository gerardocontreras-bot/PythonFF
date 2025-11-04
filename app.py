# Dashboard Financiero - versión GitHub

#incluir paquetes a usar (no instalacion)
import plotly as pl
import plotly.express as px
import numpy as np
import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

# Paso 1: iniciar Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.title = "Dashboard Financiero"

# Leer el archivo
df = pd.read_csv("empresas.csv")

sales_list = [
    "Total Revenues", "Cost of Revenues", "Gross Profit", "Total Operating Expenses",
    "Operating Imcome", "Net Income", "Shares Outstanding", "Close Stock Price",
    "Market Cap", "Multiple of Revenue"
]

# Paso 2: Layout del app
app.layout = html.Div([
    # Línea de filtros y dropdowns
    html.Div([
        # Primer dropdown: empresas
        html.Div(
            dcc.Dropdown(
                id="stockdropdown",
                value=["Amazon", "Tesla", "Microsoft", "Apple", "Google"],
                options=[{"label": x, "value": x} for x in sorted(df["Company"].unique())],
                multi=True,
                className="six columns"
            ),
            style={"width": "50%"}
        ),

        # Segundo dropdown: variable numérica
        html.Div(
            dcc.Dropdown(
                id="numericdropdown",
                value="Total Revenues",
                clearable=False,
                options=[{"label": x, "value": x} for x in sales_list],
                className="six columns"
            ),
            style={"width": "50%"}
        )
    ], className="row custom-dropdown"),

    # Gráficas
    html.Div([dcc.Graph(id="bar", figure={})]),
    html.Div([dcc.Graph(id="boxplot", figure={})]),

    # Tabla
    html.Div([
        html.Div(id="table-container_1", style={"marginBottom": "15px", "marginTop": "0px"})
    ])
])

# Paso 3: Callback
@app.callback(
    [Output("bar", "figure"),
     Output("boxplot", "figure"),
     Output("table-container_1", "children")],
    [Input("stockdropdown", "value"),
     Input("numericdropdown", "value")]
)

# Paso 4: Función de actualización
def display_value(selected_stock, selected_numeric):
    if len(selected_stock) == 0:
        dfv_fltrd = df[df["Company"].isin(["Amazon", "Tesla", "Microsoft", "Apple", "Google"])]
    else:
        dfv_fltrd = df[df["Company"].isin(selected_stock)]

    # Gráfica de líneas
    fig = px.line(
        dfv_fltrd, color="Company", x="Quarter", markers=True, y=selected_numeric,
        width=1000, height=500
    )
    fig.update_layout(
        title=f"{selected_numeric} de {', '.join(selected_stock)}",
        xaxis_title="Quarter"
    )
    fig.update_traces(line=dict(width=2))

    # Boxplot
    fig2 = px.box(
        dfv_fltrd, x="Company", color="Company", y=selected_numeric,
        width=1000, height=500
    )
    fig2.update_layout(title=f"{selected_numeric} de {', '.join(selected_stock)}")

    # Tabla
    df_reshape = dfv_fltrd.pivot(index="Company", columns="Quarter", values=selected_numeric)
    df_reshape2 = df_reshape.reset_index()

    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_reshape2.columns],
        data=df_reshape2.to_dict("records"),
        export_format="csv",
        fill_width=True,
        style_cell={"font-size": "12px"},
        style_table={"backgroundColor": "blue", "color": "white"},
    )

    return fig, fig2, table


# Correr la app
if __name__ == "__main__":
    app.run(port=10000, debug=False, host = "0.0.0.0")
