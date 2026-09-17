import pytest
from backend.app.runtime.a003 import A003BuyerPersonaError

def test_a003_requires_icp():
    assert "icp_definition" in str(A003BuyerPersonaError("A003 requires icp_definition as an object"))

def test_a003_provenance_rule():
    assert "provenance" in str(A003BuyerPersonaError("A003 supplied market evidence contains missing provenance"))
