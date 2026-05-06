import pytest
import inspect
import asyncio
from app.collectors.base import BaseCollector
from app.collectors.collector_104 import Collector104
from app.collectors.collector_1111 import Collector1111
from app.config import config

def test_collectors_have_search_real():
    """Verify that collectors have the async search_real method."""
    collectors = [Collector104(), Collector1111()]
    
    for collector in collectors:
        assert hasattr(collector, "search_real"), f"{collector.__class__.__name__} missing search_real"
        assert inspect.iscoroutinefunction(collector.search_real), f"{collector.__class__.__name__}.search_real must be async"

def test_base_collector_search_real_default():
    """BaseCollector.search_real should return an empty list by default.
    Using asyncio.run to test without requiring pytest-asyncio plugin.
    """
    class DummyCollector(BaseCollector):
        def search(self, k, l): return []
        def get_jd(self, u): return ""
        
    collector = DummyCollector()
    res = asyncio.run(collector.search_real(["test"], ["test"]))
    assert res == []

def test_default_config_flags():
    """Verify default feature flags are safe."""
    assert config.USE_REAL_COLLECTORS is False
    assert config.MAX_JOBS_PER_SOURCE == 3
    assert config.PLAYWRIGHT_HEADLESS is True

def test_mock_mode_logic_separation():
    """
    Ensures that mock mode (by default) doesn't use real collectors.
    This is a structural check of config defaults.
    """
    assert not config.USE_REAL_COLLECTORS
