import pandas as pd
from pathlib import Path
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import sqlite3
from utils.compute_health_score import compute_health_score

ROOT = Path(__file__).resolve().parents[3]
DB_PATH = ROOT / "data" / "database" / "plant_data.sqlite"

app = Dash(__name__)
server = app.server

def load_data(limit=300):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(
        f"SELECT * FROM readings ORDER BY timestamp DESC LIMIT {limit}",
        conn
    )
    conn.close()
    return df.sort_values("timestamp")

app.layout = html.Div([
    html.H1("Smart Plant Guardian Dashboard", style={"textAlign": "center"}),

    html.Div(id="health-box", style={"textAlign": "center"}),

    dcc.Interval(id="timer", interval=5000),

    dcc.Tabs([
        dcc.Tab(label="Live Data", children=[
            dcc.Graph(id="temp"),
            dcc.Graph(id="hum"),
            dcc.Graph(id="voc"),
            dcc.Graph(id="pressure")
        ]),

        dcc.Tab(label="Email Alerts", children=[
            html.Div([
                html.Label("Enter email to receive alerts"),
                dcc.Input(type="email", id="email"),
                html.Button("Save", id="save"),
                html.Div(id="saved")
            ])
        ])

    ])
])

@app.callback(
    [
        Output("temp", "figure"),
        Output("hum", "figure"),
        Output("voc", "figure"),
        Output("pressure", "figure"),
        Output("health-box", "children")
    ],
    [Input("timer", "n_intervals")]
)
def update(n):
    df = load_data()

    fig1 = px.line(df, x="timestamp", y="temperature", title="Temperature (°C)")
    fig2 = px.line(df, x="timestamp", y="humidity", title="Humidity (%)")
    fig3 = px.line(df, x="timestamp", y="voc", title="VOC Index")
    fig4 = px.line(df, x="timestamp", y="pressure", title="Pressure (hPa)")

    last = df.iloc[-1]
    score = compute_health_score(
        last.temperature,
        last.humidity,
        last.voc,
        last.pressure
    )

    return fig1, fig2, fig3, fig4, html.H3(f"Health Score: {score}/100")

@app.callback(
    Output("saved", "children"),
    [Input("save", "n_clicks")],
    [Input("email", "value")]
)
def save_email(n, email):
    if n and email:
        path = ROOT / "metadata" / "emails.txt"
        with open(path, "a") as f:
            f.write(email + "\n")
        return "Email saved!"
    return ""

if __name__ == "__main__":

    app.run(debug=True)

