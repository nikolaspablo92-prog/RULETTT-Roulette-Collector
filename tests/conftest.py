"""
Pytest configuration and fixtures for RULETTT tests
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


@pytest.fixture
def sample_roulette_data():
    """Sample roulette spin data for testing"""
    return [
        {"number": 17, "color": "black", "time": "2025-01-15T10:00:00"},
        {"number": 0, "color": "green", "time": "2025-01-15T10:01:00"},
        {"number": 32, "color": "red", "time": "2025-01-15T10:02:00"},
    ]


@pytest.fixture
def test_db_path(tmp_path):
    """Temporary database path for testing"""
    return tmp_path / "test_roulette.db"
