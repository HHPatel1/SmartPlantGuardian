import json

def test_json_valid():
    sample = '{"temperature":25,"humidity":60,"voc":100,"pressure":1010}'
    d = json.loads(sample)
    assert "temperature" in d

