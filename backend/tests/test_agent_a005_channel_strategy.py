import pytest
from backend.app.runtime.a005 import A005ChannelStrategyError

def test_a005_requires_market_research():
    assert "market_research" in str(A005ChannelStrategyError("A005 requires market_research as an object"))

def test_a005_requires_icp():
    assert "icp_definition" in str(A005ChannelStrategyError("A005 requires icp_definition as an object"))
