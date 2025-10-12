# GitHub Copilot Instructions

## Project Overview

This is a **RULETTT** system - a comprehensive cloud-enabled roulette data collection and analysis platform with real-time collaboration features. The project consists of JavaScript browser collectors, Python analyzers, REST API server, web dashboard, and cloud data synchronization.

## API & Web Services

### Flask API Server (`api_server.py`)

- **Endpoints**: REST API with `/api/` prefix for health, spins, statistics, strategies, sessions
- **CORS Enabled**: Supports cross-origin requests from webapp
- **Real-time Features**: Chat system, activity feed, team sessions
- **Database Integration**: SQLite with automatic table creation
- **Export Capabilities**: JSON export with pagination and filtering

### Web Dashboard (`webapp/`)

- **Multi-device Support**: Responsive HTML5 interfaces (dashboard.html, mobile.html)
- **Real-time Updates**: WebSocket integration for live data streams
- **Advanced Analytics**: Dedicated analytics page with visualization
- **Team Communication**: Built-in chat and collaboration tools

### Cloud Data Manager (`cloud_data_manager.py`)

- **Multi-platform Sync**: Firebase Realtime Database, GitHub Gist backup
- **Async Operations**: aiohttp-based async data syncing
- **Export Formats**: JSON, CSV, Excel with pandas integration
- **Team Activity Logging**: Real-time activity broadcasting

## Key Development Patterns

### Russian Language Interface

- All user-facing text in Russian (Cyrillic + emoji)
- Console logs: `print("✅ Готово!")` style with status emojis
- Error messages: `"❌ Ошибка: ..."` format
- CLI menus use numbered options with emoji prefixes

### Roulette Domain Constants

- **Red numbers**: `{1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}` (defined in `RouletteUtils.RED_NUMBERS`)
- **Black numbers**: `{2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}` (in `RouletteUtils.BLACK_NUMBERS`)
- **Green**: Only 0 (European roulette - no 00)
- **Number validation**: `0 <= n <= 36`

### Graceful Dependency Management

```python
# Pattern used throughout codebase
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️ numpy не установлен, используем базовые функции")

# Use fallback logic
if NUMPY_AVAILABLE:
    result = np.mean(values)
else:
    result = sum(values) / len(values)
```

### Database Schema Pattern

- **SQLite**: Primary storage in `data/` directory
- **Schema**: Consistent table structure across all database files
- **Session tracking**: All tables include `session_id` for team collaboration
- **Auto-creation**: Tables created automatically if missing

## Critical Workflows

### Testing Workflow

```bash
# ALWAYS run before making changes
python test_system.py  # Smoke tests: imports, basic functions, strategies
```

### Local Development Setup

```bash
# Setup (first time)
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Running services (use VS Code tasks)
# Task: "🚀 Запустить API сервер" - starts Flask API on port 5000
# Task: "🌐 Запустить веб-сервер" - starts static server on port 8080
# Task: "🎲 Запустить все сервисы RULETTT" - starts both services
```

## Architecture & Components

### Core Components

- **JavaScript Browser Collector** (`auto_collector_console_code.js`) - Browser console script for real-time roulette data collection
- **Python Analyzer Suite** (`src/`) - Data analysis, AI-powered pattern recognition, and strategy backtesting
  - `utils.py` - Roulette utilities (color mapping, number validation, dozen calculations)
  - `data_collector.py` - SQLite-based data persistence and statistics
  - `game_analyzer.py` - Strategy backtesting engine with predefined strategies
  - `ai_assistant.py` - AI pattern analysis and strategy recommendations
  - `main.py` / `main_single_table.py` - Interactive CLI menu system
  - `live_data_collector.py` - Real-time data acquisition from multiple sources
  - `user_strategies.py` - Custom user-defined betting strategies
- **Web Interface** (`webapp/`) - HTML5 dashboard, mobile interface, and analytics
- **API Server** (`api_server.py`) - Flask REST API with CORS support for team collaboration
- **Cloud Integration** (`cloud_data_manager.py`) - Firebase, GitHub Gist, and multi-platform sync
- **Data Storage** - Multi-tier: localStorage → SQLite → Cloud (Firebase/Gist backup)

## API & Web Services

### Flask API Server (`api_server.py`)

- **Endpoints**: REST API with `/api/` prefix for health, spins, statistics, strategies, sessions
- **CORS Enabled**: Supports cross-origin requests from webapp
- **Real-time Features**: Chat system, activity feed, team sessions
- **Database Integration**: SQLite with automatic table creation
- **Export Capabilities**: JSON export with pagination and filtering

### Web Dashboard (`webapp/`)

- **Multi-device Support**: Responsive HTML5 interfaces (dashboard.html, mobile.html)
- **Real-time Updates**: WebSocket integration for live data streams
- **Advanced Analytics**: Dedicated analytics page with visualization
- **Team Communication**: Built-in chat and collaboration tools

### Cloud Data Manager (`cloud_data_manager.py`)

- **Multi-platform Sync**: Firebase Realtime Database, GitHub Gist backup
- **Async Operations**: aiohttp-based async data syncing
- **Export Formats**: JSON, CSV, Excel with pandas integration
- **Team Activity Logging**: Real-time activity broadcasting

### Data Flow Architecture

1. **Collection**: JavaScript runs in browser console, DOM scraping every 30 seconds
2. **Storage**: Data saved to browser localStorage AND exported as JSON
3. **Transfer**: User copies JSON from browser console to `roulette_console_data.json`
4. **Analysis**: `console_to_analysis.py` imports JSON → SQLite → Python analysis
5. **API Integration**: Flask server exposes data via REST endpoints
6. **Web Interface**: Real-time dashboard consumes API data
7. **Cloud Sync**: Async synchronization to Firebase and GitHub Gist

## Key Files & Patterns

### JavaScript Collector (`auto_collector_console_code.js`)

- **Entry Point**: Copy entire file contents to browser console (F12)
- **DOM Scraping**: Uses selector `.game-area__history-line--Lkj9A` to find roulette history
- **Duplicate Prevention**: Tracks timestamps to avoid re-adding same spin within 10 seconds
- **Global Functions**: `stopRouletteCollector()`, `exportRouletteData()`, `showRouletteStats()`, `saveRouletteStats()`, `clearRouletteData()`
- **Auto-Persistence**: localStorage key `rouletteData` survives page refreshes
- **Collection Rate**: 30-second intervals, max 100 results stored

### Python Analyzer Structure (`src/`)

- **`utils.py`**: Stateless utility class with roulette constants (RED_NUMBERS, BLACK_NUMBERS sets)
- **`data_collector.py`**: SQLite wrapper with session tracking, test data generation (500 spins default)
- **`game_analyzer.py`**: Strategy pattern implementation - base `GameStrategy` class + `PredefinedStrategies` factory
- **`ai_assistant.py`**: Optional numpy dependency (graceful degradation if missing), pattern analysis without ML libraries
- **`main.py`**: CLI menu system with numbered options, Russian language prompts

### Project Structure Convention

```
RULETTT/
├── auto_collector_console_code.js         # Browser console collector (paste & run)
├── console_to_analysis.py                 # Bridge: JSON → SQLite converter
├── roulette_console_data.json            # Data transfer file (browser → Python)
├── src/                                   # Python analyzer suite
│   ├── main.py                           # Entry point: py src/main.py
│   ├── utils.py                          # Roulette constants & helpers
│   ├── data_collector.py                 # SQLite persistence layer
│   ├── game_analyzer.py                  # Strategy backtesting engine
│   └── ai_assistant.py                   # Pattern analysis & recommendations
├── data/                                  # SQLite databases (*.db files)
├── docs/explanation.md                    # Plain-language code explanations
├── verified_apis.md                       # Casino API endpoints documentation
└── test_system.py                         # Smoke tests for all modules
```

## Development Workflows

### Starting Data Collection (Browser → localStorage)

1. Open target casino website in browser (Opera recommended in docs)
2. Open browser console (F12 or Ctrl+Shift+I)
3. Copy/paste entire `auto_collector_console_code.js`
4. Collector auto-starts, updates every 30 seconds
5. Monitor: `showRouletteStats()` in console

### Exporting Data for Analysis (Browser → Python)

```javascript
exportRouletteData(); // In browser console - copies JSON to clipboard
```

```bash
# Paste clipboard into roulette_console_data.json
py console_to_analysis.py  # Converts JSON → SQLite
py src/main.py             # Interactive analysis menu
```

### Python Analysis Workflow

```bash
# Setup (first time)
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Testing (always run before coding)
py test_system.py      # Smoke tests: imports, basic functions, strategies

# Running services
py src/main.py         # Interactive CLI menu
py api_server.py       # Flask REST API server (port 5000)
py cloud_data_manager.py  # Cloud sync demonstration
# Menu options:
# 1. Data Management → Generate test data (500 spins/7 days default)
# 2. Strategy Analysis → Test predefined strategies (Martingale, etc.)
# 3. AI Assistant → Pattern analysis and recommendations
```

### Adding Custom Strategies

Extend `game_analyzer.py`:

```python
class MyStrategy(GameStrategy):
    def make_bet(self, spin_number, history):
        # Custom logic here
        return {"type": "color", "numbers": ["red"], "amount": 10}
```

### Testing & Validation

- **No formal test framework** - uses smoke test script `test_system.py`
- Tests imports, utils (color/dozen calculations), data collector, basic strategies
- Database: `data/test_simple.db` for testing, `data/final_single_table.db` for production
- Manual testing via interactive CLI menus

## Project-Specific Conventions

### Russian Language Interface

- All user-facing text in Russian (Cyrillic + emoji)
- Console logs: `print("✅ Готово!")` style with status emojis
- Error messages: `"❌ Ошибка: ..."` format
- CLI menus use numbered options with emoji prefixes
- Comments in code can be English or Russian

### Roulette Domain Constants

- **Red numbers**: `{1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}` (defined in `RouletteUtils.RED_NUMBERS`)
- **Black numbers**: `{2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}` (in `RouletteUtils.BLACK_NUMBERS`)
- **Green**: Only 0 (European roulette - no 00)
- **Dozens**: 1-12, 13-24, 25-36 (zero returns None)
- Number validation: `0 <= n <= 36`

### Data Format Standards

```python
# Spin record (Python)
{
    "number": 17,           # int (0-36)
    "color": "black",       # "red" | "black" | "green"
    "time": "2025-01-15T10:30:00",  # ISO format
    "table_id": "test_session",      # session identifier
    "source": "browser_console"      # data origin
}

# Bet result
{
    "type": "color",        # "color" | "number" | "dozen"
    "numbers": ["red"],     # list of bet targets
    "amount": 10.0,         # float bet amount
    "payout": 20.0          # float payout (0 if lost)
}
```

### Dependency Management

- **Required**: `sqlite3` (built-in), `datetime`, `json`, `pathlib`
- **Optional**: `numpy` - graceful degradation if missing (see `ai_assistant.py`)
- **Heavy deps**: `pandas`, `matplotlib`, `scikit-learn` in requirements.txt but not strictly required
- Install strategy: `pip install -r requirements.txt` (but system works with stdlib only)

### Error Handling Patterns

```python
# Graceful numpy fallback
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️ numpy не установлен, используем базовые функции")

# Calculate mean
if NUMPY_AVAILABLE:
    avg = np.mean(values)
else:
    avg = sum(values) / len(values)
```

## Integration Points

### Browser Console → localStorage

- **JavaScript Function**: IIFE (Immediately Invoked Function Expression) pattern
- **Storage Key**: `"rouletteData"` in localStorage
- **Global Functions**: Attached to `window` object for console access
- **Duplicate Detection**: `Math.abs(new Date(r.timestamp) - new Date()) < 10000` (10 sec window)
- **DOM Scraping**: `querySelector('div:first-child')` to get latest spin only

### Browser → Python Data Bridge

1. Browser: `exportRouletteData()` → copies JSON to clipboard
2. Manual: Create/update `roulette_console_data.json` with pasted data
3. Python: `console_to_analysis.py` reads JSON → converts timestamps → writes to SQLite
4. Conversion logic: Assigns fake timestamps (1 min per spin) from `datetime.now()` backwards

### Python Internal Architecture

- **Multi-source data**: JSON import from browser + live API integration + cloud sync
- **SQLite schema**: Multiple tables (roulette_spins, strategy_results, team_sessions, chat_messages)
- **Strategy pattern**: Base class `GameStrategy` with `make_bet()` and `update_balance()` methods
- **Factory pattern**: `PredefinedStrategies.martingale_red()` returns configured strategy instances
- **Async operations**: aiohttp for cloud sync, real-time data streams
- **Test data generation**: `DataCollector.generate_test_data(num_spins=500, days=7)` for development

### Online Collaboration Setup

- **GitHub Codespaces**: `.devcontainer/devcontainer.json` with Python 3.11 + Node 18
- **GitPod**: `.gitpod.yml` with auto-install tasks
- **Replit**: `package.json` exists but minimal config
- **Port forwarding**: 8000 (Python server), 5000 (Flask), 3000 (Node), 8080 (alt server), 8888 (Jupyter)
- **Extensions**: Live Share, Python, Pylance, Code Runner pre-configured

## Debugging & Troubleshooting

### Common Issues

#### JavaScript Console Errors

- **"Element not found"**: Selector `.game-area__history-line--Lkj9A` may change per casino site
- **Fix**: Inspect DOM, update selector in CONFIG object
- **Duplicate spins**: Check 10-second duplicate prevention window in `isDuplicate` logic

#### Python Import Errors

```bash
# Missing dependencies
pip install -r requirements.txt

# Module not found in src/
sys.path.append(str(Path(__file__).parent / "src"))  # Pattern used in all scripts
```

#### Database Issues

- **"Database locked"**: Close other connections, use single CLI session
- **Empty stats**: Generate test data via menu option 1 → 2
- **Location**: All `.db` files in `data/` directory

#### Data Transfer Issues

- **JSON format errors**: Ensure clean copy/paste from console, no truncation
- **Missing file**: Create `roulette_console_data.json` in project root
- **Encoding**: Use UTF-8 for Russian characters

### Monitoring Commands

```javascript
// Browser console
showRouletteStats(); // Current collection status
console.log(localStorage.getItem("rouletteData")); // Raw stored data
saveRouletteStats(); // Copy formatted stats to clipboard
```

```python
# Python CLI (in src/main.py menus)
# Option 1.3: View statistics
# Option 2: Test strategies (shows balance/profit tracking)
# Option 3.4: Full AI report
```

### Development Tips

- **Start with test data**: Menu 1 → 2 generates 500 spins instantly
- **Strategy testing**: Use `test_strategies()` in `test_system.py` for quick validation
- **Module isolation**: Each `src/*.py` file imports minimal dependencies (except `ai_assistant.py`)
- **Documentation**: Read `docs/explanation.md` for plain-language explanations of each module
- **Educational focus**: System designed for learning statistics, not real gambling (warnings in docs)

## Quick Reference

### Essential Commands

```bash
# Setup
python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt

# Test before coding
py test_system.py

# Run services
py src/main.py             # Interactive CLI menu
py api_server.py           # Flask API server (http://localhost:5000)
py cloud_data_manager.py   # Cloud sync demo

# Bridge browser data to Python
py console_to_analysis.py
```

### Flask API Endpoints

- `GET  /api/health` - Health check
- `POST /api/spins` - Add roulette spin
- `GET  /api/spins` - Get spins with filtering
- `GET  /api/statistics` - Statistical analysis
- `POST /api/strategies` - Add strategy result
- `POST /api/sessions` - Create team session
- `GET  /api/chat` - Get chat messages
- `POST /api/chat` - Send chat message
- `GET  /api/export/<format>` - Export data (JSON/CSV/Excel)

### VS Code Tasks Available

- 🚀 Launch API Server - Starts Flask API on port 5000
- 🌐 Launch Web Server - Serves webapp on port 8080
- 🎲 Launch All Services - Starts both API and web servers
- 🧪 Test System - Runs test_system.py
- 📦 Install Dependencies - Runs pip install

### Key Patterns to Follow

1. **Russian UI**: All user messages use emoji + Cyrillic (e.g., `"✅ Готово!"`)
2. **Graceful degradation**: Check optional dependencies with try/except, provide fallbacks
3. **CLI menus**: Numbered options with `input()` loops, return 0 to go back
4. **Strategy pattern**: Extend `GameStrategy` base class for new betting strategies
5. **Test data first**: Generate synthetic data before collecting real browser data

## Integration Points

### Browser → Python Bridge

- **Data format**: JSON with timestamp conversion in `console_to_analysis.py`
- **localStorage key**: `"rouletteData"` survives page refreshes
- **Duplicate prevention**: 10-second window for same timestamp

### API → Frontend Communication

- **CORS enabled** for cross-origin requests
- **Real-time updates** via polling (WebSocket integration planned)
- **Pagination** supported on all list endpoints
- **Error handling** with consistent JSON error format

### Cloud Synchronization

- **Async patterns**: All cloud operations use `asyncio` and `aiohttp`
- **Fallback strategy**: Firebase primary, GitHub Gist backup
- **Data integrity**: Local SQLite as source of truth

## Quick Reference

### Essential Commands

```bash
# System validation
python test_system.py

# Start main analyzer
python src/main.py

# Bridge browser → Python
python console_to_analysis.py

# Start API server
python api_server.py

# Start web server (from webapp/)
python -m http.server 8080
```

### Key Files to Understand First

1. `test_system.py` - Shows expected module behavior and imports
2. `src/utils.py` - Roulette domain knowledge and constants
3. `api_server.py` - REST API endpoints and database schema
4. `auto_collector_console_code.js` - Browser collection logic
5. `src/main.py` - CLI menu structure and user workflows

### Development Guidelines

1. **Test first**: Always run `test_system.py` before coding
2. **Russian UI**: All user messages use emoji + Cyrillic
3. **Graceful degradation**: Handle missing dependencies with fallbacks
4. **Educational focus**: System designed for learning statistics, not real gambling
5. **Team collaboration**: Support multi-user sessions and real-time features

When working with this codebase, prioritize data accuracy, maintain Russian language conventions, and remember this is an educational system for learning statistics and probability patterns.
