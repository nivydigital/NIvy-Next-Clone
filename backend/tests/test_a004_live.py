import os
import pytest

@pytest.mark.skipif(os.getenv("AIOS_LIVE_TESTS") != "1", reason="Live agent tests deferred")
def test_a004_live():
    pytest.fail("Deferred: run centralized live-agent batch with AIOS_LIVE_TESTS=1")
