"""
RULETTT - European Roulette Data Collection and Analysis System

Main modules:
- utils: Roulette utilities (RouletteUtils)
- data_collector: Data collection and storage (DataCollector)
- game_analyzer: Strategy analysis (GameAnalyzer, GameStrategy, PredefinedStrategies)
- ai_assistant: AI-powered analysis (AIAssistant)
- user_strategies: Custom user strategies
- bot_simulator: Bot simulation (BotSimulator)
- auth_manager: Authentication management (AuthManager)
- paddypower_auto_collector: Auto-collection from PaddyPower (PaddyPowerCollector, AntiDetectBrowser)

Version: 2.0.0
License: MIT
Author: RULETTT Team
"""

__version__ = "2.0.0"
__author__ = "RULETTT Team"
__license__ = "MIT"

# Import core classes
try:
    from .utils import RouletteUtils
except ImportError:
    RouletteUtils = None

try:
    from .data_collector import DataCollector
except ImportError:
    DataCollector = None

try:
    from .game_analyzer import GameAnalyzer, GameStrategy, PredefinedStrategies
except ImportError:
    GameAnalyzer = None
    GameStrategy = None
    PredefinedStrategies = None

try:
    from .ai_assistant import AIAssistant
except ImportError:
    AIAssistant = None

try:
    from .bot_simulator import BotSimulator
except ImportError:
    BotSimulator = None

try:
    from .auth_manager import AuthManager
except ImportError:
    AuthManager = None

try:
    from .paddypower_auto_collector import PaddyPowerCollector, AntiDetectBrowser
except ImportError:
    PaddyPowerCollector = None
    AntiDetectBrowser = None

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "RouletteUtils",
    "DataCollector",
    "GameAnalyzer",
    "GameStrategy",
    "PredefinedStrategies",
    "AIAssistant",
    "BotSimulator",
    "AuthManager",
    "PaddyPowerCollector",
    "AntiDetectBrowser",
]
