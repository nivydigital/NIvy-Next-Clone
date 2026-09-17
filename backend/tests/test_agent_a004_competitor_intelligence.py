import pytest
from backend.app.runtime.a004 import A004CompetitorError

def test_a004_requires_evidence():
    assert "evidence" in str(A004CompetitorError("A004 requires market research evidence"))

def test_a004_requires_provenance():
    assert "provenance" in str(A004CompetitorError("A004 evidence items missing provenance"))
