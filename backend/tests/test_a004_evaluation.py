def test_a004_output_contract():
    required={"status","competitors","comparison","positioning","gaps","evidence","confidence","assumptions","derived_from"}
    sample={"status":"success","competitors":[],"comparison":[],"positioning":[],"gaps":[],"evidence":[],"confidence":"low","assumptions":[],"derived_from":[]}
    assert required.issubset(sample)
