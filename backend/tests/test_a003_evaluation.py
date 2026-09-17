def test_a003_evaluation_contract():
    required = {"status", "personas", "evidence", "assumptions", "confidence", "derived_from"}
    sample = {"status":"success","personas":[],"evidence":[],"assumptions":[],"confidence":"low","derived_from":[]}
    assert required.issubset(sample)
    assert sample["confidence"] in {"high","medium","low"}
