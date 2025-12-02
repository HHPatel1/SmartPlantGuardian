
from dash import html, dcc

def render():
    return html.Div([
        html.Label("Email address for alerts:"),
        dcc.Input(id="email_input", type="email"),
        html.Button("Register", id="email_button")
    ])

