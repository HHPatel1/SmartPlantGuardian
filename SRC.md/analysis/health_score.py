def health_score(t, h, voc, p):
    score = 100
    if t < 20 or t > 27: score -= 10
    if h < 50 or h > 70: score -= 10
    if voc > 200: score -= (voc - 200) / 5
    if p < 995 or p > 1030: score -= 5
    return max(0, int(score))

