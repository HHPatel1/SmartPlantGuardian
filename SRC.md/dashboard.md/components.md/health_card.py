
from dash import html

def render(score):
    color = "green" if score > 80 else "orange" if score > 50 else "red"
    return html.Div(
        f"Health Score: {score}",
        style={
            "background": color,
            "padding": "12px",
            "border-radius": "8px",
            "color": "white",
            "fontSize": "24px",
            "textAlign": "center"
        }
    )

