# GitHub Copilot Instructions

## Project Overview

This is a **RULETTT Roulette Data Collector** system - a comprehensive hybrid JavaScript/Python project for automated casino roulette data collection, analysis, and collaborative strategy development. The system supports multiple collection methods, real-time analysis, and online collaboration through cloud development environments.

## Architecture & Components

### Core Components
- **JavaScript Browser Collector** (`auto_collector_console_code.js`) - Browser console script for DOM-based data collection
- **Python Analysis Suite** (`src/`) - Modular analyzers with SQLite persistence and AI assistance
- **API Integration Layer** - Multiple casino API connectors with automatic discovery tools
- **Web Interface** (`webapp/`) - HTML dashboard for collection monitoring and collaboration
- **Data Storage** - Multi-tier: localStorage → JSON export → SQLite databases

### Data Flow
1. **Collection**: JavaScript scrapes DOM elements every 30 seconds OR Python collectors use API endpoints
2. **Export**: Browser data copied to JSON files via clipboard integration
3. **Analysis**: Python modules process data with strategy testing and pattern recognition
4. **Collaboration**: Real-time sharing through GitHub Codespaces, GitPod, or Replit

## Key Files & Patterns

### JavaScript Browser Collector
- **Main Script**: `auto_collector_console_code.js` (326 lines) - DOM scraper with CSS selector `.game-area__history-line--Lkj9A`
- **Global Functions**: `stopRouletteCollector()`, `exportRouletteData()`, `showRouletteStats()`, `saveRouletteStats()`, `clearRouletteData()`
- **Collection Logic**: Finds first child element (latest number), prevents duplicates within 10-second window
- **Auto-Export**: Copies formatted data to clipboard for easy transfer to Python analysis

### Python Analysis Framework (`src/`)
- **Main System**: `main_single_table.py` - Orchestrates all components with menu-driven interface
- **Data Layer**: `data_collector.py` - SQLite operations with automatic schema management
- **Analysis Engine**: `game_analyzer.py` - Strategy testing (Martingale, Fibonacci, D'Alembert, Labouchere)
- **AI Assistant**: `ai_assistant.py` - Pattern recognition and recommendations
- **Bridge Script**: `console_to_analysis.py` - Imports browser JSON data into Python system

### API Discovery Tools
- **Setup Wizards**: `quick_api_setup.py`, `universal_api_setup.py`, `browser_api_guide.py`
- **Test Suite**: `debug_api.py`, `test_connection.py` - Validates configurations and endpoints
- **Known APIs**: `verified_apis.md` - Stake.com GraphQL, BC.Game REST, Pragmatic Play Live
- **Auto-Discovery**: Network traffic analysis guides for finding new casino APIs

### Project Structure
```
RULETTT/
├── auto_collector_console_code.js         # Browser DOM collector
├── console_to_analysis.py                 # Data bridge (JSON→SQLite) 
├── src/                                   # Python analysis suite
│   ├── main_single_table.py              # Main orchestrator
│   ├── data_collector.py                 # SQLite operations
│   └── game_analyzer.py                  # Strategy engines
├── webapp/index.html                     # Web dashboard
├── data/*.db                             # SQLite databases
└── verified_apis.md                      # API documentation
```

## Development Workflows

### Browser Collection Method
1. **Start Collection**: Copy entire `auto_collector_console_code.js` to browser console on casino site
2. **Monitor**: Use `showRouletteStats()` to check collection progress (updates every 30 seconds)
3. **Export**: Run `exportRouletteData()` to copy JSON data to clipboard
4. **Transfer**: Paste data into `roulette_console_data.json` file

### Python Analysis Workflow
```bash
# Import browser data and run analysis
python console_to_analysis.py

# Or run full system with menu
python src/main_single_table.py
```

### API Collection Setup
```bash
# Discover APIs through browser network analysis
python browser_api_guide.py

# Quick setup for known casino
python quick_api_setup.py

# Test API connection
python debug_api.py
```

### Online Collaboration Setup
- **GitHub Codespaces**: 60 hours free, full VS Code integration
- **GitPod**: 50 hours free, browser-based development  
- **Replit**: Free public projects, built-in web server
- **Live Share**: Local collaboration with VS Code extension

## Project-Specific Conventions

### Russian Language Interface
- All user-facing text and documentation in Russian
- Console output uses Cyrillic characters and emoji
- Error messages and logs in Russian

### Data Format Standards
- **Timestamps**: Unix timestamps for all game results
- **Numbers**: Roulette results stored as integers (0-36)
- **Colors**: "red", "black", "green" string values
- **JSON Structure**: Consistent schema for cross-component compatibility

### API Integration Patterns
- **Headers**: Always include proper User-Agent for casino APIs
- **Delays**: Mandatory 1-second delays between API calls
- **Error Handling**: Try/catch blocks with Russian error messages
- **Rate Limiting**: Respect casino API limits to avoid blocking

### Browser Console Deployment
- **Global Scope**: All functions attached to `window` object
- **Persistence**: localStorage for data survival across sessions  
- **Error Recovery**: Auto-restart on API failures
- **Memory Management**: Limit stored results to prevent browser crashes

## Integration Points

### Casino API Endpoints
- **Stake.com**: GraphQL endpoint `/_api/graphql` with 60 req/min limit
- **BC.Game**: REST API `/api/casino/roulette/history` 
- **Pragmatic Play**: Live casino API with JSESSIONID authentication
- **Paddy Power**: Configured endpoints in `paddypower_config.json`

### Data Exchange Formats
**Browser Export JSON:**
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "number": 25,
  "color": "red",
  "sequence": 1,
  "exported_at": "2024-01-15T11:00:00Z"
}
```

**SQLite Schema (Python):**
- `roulette_results`: timestamp, number, color, table_id, session_id
- `game_sessions`: session_id, start_time, end_time, total_spins
- `strategy_results`: strategy_name, profit_loss, win_rate, max_drawdown

### Cross-Component Communication
- **JavaScript → Python**: JSON clipboard export → file import → SQLite
- **Python → User**: Console menus, statistical reports, strategy recommendations  
- **Browser → Casino**: DOM scraping (preferred) or direct API calls
- **Collaboration**: Git repository sync across cloud development platforms

## Debugging & Troubleshooting

### Common Issues
- **DOM Selector Changes**: Update CSS selector `.game-area__history-line--Lkj9A` if casino updates UI
- **API Authentication**: Use `setup_pragmatic_auth.py` for Pragmatic Play JSESSIONID setup
- **Data Loss**: Check localStorage quota with browser DevTools → Application → Storage
- **Collection Gaps**: Verify 30-second interval timing and duplicate prevention logic
- **Export Failures**: Ensure clipboard permissions and clean JSON formatting

### Development Commands
```javascript
// Browser console monitoring
showRouletteStats()                          // Current collection status
exportRouletteData()                         // Copy data to clipboard  
localStorage.getItem('rouletteData')         // Raw stored data
stopRouletteCollector()                      // Stop collection
```

```bash
# Python debugging
python debug_api.py                         # Test API connections
python test_connection.py                   # Validate configurations
python src/main_single_table.py            # Full system menu
python console_to_analysis.py              # Import browser data
```

### Testing Workflows
1. **DOM Collection**: Test on live casino → check console output → verify data export
2. **API Collection**: Configure endpoint → test connection → collect sample data
3. **Analysis**: Import JSON → run strategies → validate SQLite storage
4. **Collaboration**: Share repository → test online platform setup → verify real-time sync

When working with this codebase, prioritize data accuracy, respect API rate limits, and maintain the existing Russian language conventions throughout all user interfaces.