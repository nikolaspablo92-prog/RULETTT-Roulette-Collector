# GitHub Copilot Instructions

## Project Overview

This is a **Roulette Data Collector** system - a hybrid JavaScript/Python project for automated casino roulette data collection and strategy analysis. The project uses browser-based JavaScript collectors and Python analyzers to gather and process gambling data from various casino APIs.

## Architecture & Components

### Core Components
- **JavaScript Browser Collector** (`auto_collector_console_code.js`) - Browser console script for real-time roulette data collection
- **Python Strategy Analyzer** - Data analysis and pattern recognition system  
- **API Integration Layer** - Connects to multiple casino platforms (Stake.com, BC.Game, Roobet, etc.)
- **Data Storage** - JSON-based data persistence with browser localStorage integration

### Data Flow
1. **Collection**: JavaScript runs in browser console, polls casino APIs every 30 seconds
2. **Storage**: Data saved to browser localStorage and exported as JSON
3. **Analysis**: Python scripts process exported JSON for pattern analysis
4. **Reporting**: Statistical analysis and strategy recommendations

## Key Files & Patterns

### JavaScript Collector (`auto_collector_console_code.js`)
- **Entry Point**: Copy entire file contents to browser console
- **Global Functions**: `stopRouletteCollector()`, `exportRouletteData()`, `showRouletteStats()`, `saveRouletteStats()`, `clearRouletteData()`
- **Auto-Persistence**: Saves data to localStorage automatically
- **Rate Limiting**: 30-second intervals to avoid API throttling

### API Integration (`verified_apis.md`)
- **Primary Targets**: Stake.com GraphQL, BC.Game REST API, Roobet endpoints
- **Authentication**: Most APIs are public, no auth required
- **Rate Limits**: ~60 requests/minute for Stake.com
- **Error Handling**: Implement exponential backoff for failed requests

### Project Structure Convention
```
RULETTT/                                    # Main project directory
├── auto_collector_console_code.js         # Browser data collector
├── verified_apis.md                       # API documentation
├── START_COLLECTOR.txt                    # Quick start guide
├── SHARE_PROJECT.txt                      # Distribution instructions
└── [Python analyzers]                     # Strategy analysis scripts
```

## Development Workflows

### Starting Data Collection
1. Open target casino website in browser
2. Open browser console (F12)
3. Copy/paste entire `auto_collector_console_code.js`
4. Data collection begins automatically every 30 seconds
5. Use `showRouletteStats()` to monitor progress

### Exporting Data for Analysis
```javascript
exportRouletteData()    // Exports JSON for Python processing
saveRouletteStats()     // Copies statistics to clipboard
```

### Python Analysis Setup
- Import exported JSON data
- Run statistical analysis on number patterns
- Generate strategy recommendations
- Calculate win/loss probabilities

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
- **Stake.com**: GraphQL endpoint at `/_api/graphql`
- **BC.Game**: REST API at `/api/casino/roulette/history`
- **Roobet**: Live games API at `/api/games/live`

### Data Exchange Format
```json
{
  "timestamp": 1234567890,
  "number": 25,
  "color": "red",
  "source": "stake.com",
  "session_id": "abc123"
}
```

### Cross-Component Communication
- JavaScript → Python: JSON export files
- Python → User: Statistical reports and recommendations
- Browser → APIs: RESTful HTTP requests and GraphQL queries

## Debugging & Troubleshooting

### Common Issues
- **API Rate Limiting**: Reduce polling frequency if receiving 429 errors
- **CORS Errors**: Use browser extensions or run from casino domain
- **Data Loss**: Check localStorage quota and clear old data if needed
- **Syntax Errors**: Ensure clean copy/paste of JavaScript code

### Monitoring Commands
```javascript
showRouletteStats()     // Display current collection status
console.log(localStorage.getItem('rouletteData'))  // Check stored data
```

When working with this codebase, prioritize data accuracy, respect API rate limits, and maintain the existing Russian language conventions throughout all user interfaces.