from src.analysis.health_score import health_score

def test_score_range():
    assert 0 <= health_score(25, 60, 100, 1010) <= 100

