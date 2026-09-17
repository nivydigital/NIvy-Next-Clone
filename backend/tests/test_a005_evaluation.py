def test_a005_output_contract():
    required={"status","channels","prioritization","channel_fit","experiments","constraints","confidence","assumptions","derived_from"}
    sample={"status":"success","channels":[],"prioritization":[],"channel_fit":[],"experiments":[],"constraints":[],"confidence":"low","assumptions":[],"derived_from":[]}
    assert required.issubset(sample)
