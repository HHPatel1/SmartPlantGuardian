
import plotly.express as px

def line(df, y, title):
    return px.line(df, x="timestamp", y=y, title=title)

