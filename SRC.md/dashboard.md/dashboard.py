
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3
from pathlib import Path
import plotly.express as px
from src.analysis.health_score import health_score
from src.dashboard.components.plant_image import render as plant_img
from src.dashboard.components.email_tab import render as email_tab

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "data" / "database" / "plant_data.sqlite"

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def read_db():
    conn = sqlite3.connect(DB)
    df = pd.read_sql("SELECT * FROM readings ORDER BY timestamp DESC LIMIT 500", conn)
    conn.close()
    return df

app.layout = dbc.Container([
    html.H1("🌱 Smart Plant Guardian Dashboard", className="text-center"),
    dcc.Tabs(id="tabs", value="live", children=[
        dcc.Tab(label="📈 Live Data", value="live"),
        dcc.Tab(label="📥 Email Alerts", value="email"),
        dcc.Tab(label="🌿 Plant Profile", value="plant"),
    ]),
    html.Div(id="tab_content"),
    dcc.Interval(id="update_interval", interval=5000, n_intervals=0)
], fluid=True)


@app.callback(
    Output("tab_content", "children"),
    Input("tabs", "value"),
    Input("update_interval", "n_intervals")
)
def render_tab(tab, n):
    df = read_db()

    if tab == "live":
        if df.empty:
            return html.H3("Waiting for live sensor data...")

        fig_temp = px.line(df, x="timestamp", y="temperature", title="Temperature (°C)")
        fig_hum = px.line(df, x="timestamp", y="humidity", title="Humidity (%)")
        fig_voc = px.line(df, x="timestamp", y="voc", title="VOC Index")
        fig_pres = px.line(df, x="timestamp", y="pressure", title="Pressure (hPa)")

        latest = df.iloc[-1]
        score = health_score(
            latest.temperature,
            latest.humidity,
            latest.voc,
            latest.pressure
        )

        return dbc.Row([
            dbc.Col([
                html.H3(f"💡 Health Score: {score}/100"),
                plant_img()
            ], width=3),
            dbc.Col([dcc.Graph(figure=fig_temp)], width=9),
            dbc.Col([dcc.Graph(figure=fig_hum)], width=12),
            dbc.Col([dcc.Graph(figure=fig_voc)], width=12),
            dbc.Col([dcc.Graph(figure=fig_pres)], width=12)
        ])

    elif tab == "email":
        return email_tab()

    elif tab == "plant":
        return html.Div([
            html.H3("Peace Lily Profile"),
            html.P("Optimal Conditions:"),
            html.Ul([
                html.Li("Temperature: 20–27°C"),
                html.Li("Humidity: 50–70%"),
                html.Li("VOC < 200"),
                html.Li("Pressure: 995–1030 hPa")
            ])
        ])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
