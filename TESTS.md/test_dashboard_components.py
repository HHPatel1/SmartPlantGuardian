
from src.dashboard.components.health_card import render

def test_health_card():
    card = render(80)
    assert "Health Score" in card.children

