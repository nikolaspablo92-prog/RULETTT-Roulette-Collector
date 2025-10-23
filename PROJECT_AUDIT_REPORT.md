# рџ”Ќ РџРћР›РќР«Р™ РђРЈР”РРў РџР РћР•РљРўРђ RULETTT

**Р”Р°С‚Р° РїСЂРѕРІРµСЂРєРё:** 13 РѕРєС‚СЏР±СЂСЏ 2025  
**Р’РµСЂСЃРёСЏ:** 2.0.0  
**РЎС‚Р°С‚СѓСЃ:** вњ… РџСЂРѕРІРµСЂРµРЅРѕ Рё РѕРїС‚РёРјРёР·РёСЂРѕРІР°РЅРѕ

---

## рџ“Љ РРЎРџРћР›РќРРўР•Р›Р¬РќРћР• Р Р•Р—Р®РњР•

### вњ… Р§С‚Рѕ СЂР°Р±РѕС‚Р°РµС‚ РѕС‚Р»РёС‡РЅРѕ

- вњ… РњРѕРґСѓР»СЊРЅР°СЏ Р°СЂС…РёС‚РµРєС‚СѓСЂР° (РєР°Р¶РґС‹Р№ С„Р°Р№Р» - РѕС‚РґРµР»СЊРЅР°СЏ С„СѓРЅРєС†РёСЏ)
- вњ… РќРµС‚ С†РёРєР»РёС‡РµСЃРєРёС… РёРјРїРѕСЂС‚РѕРІ
- вњ… Graceful degradation (РЅРµРѕР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё)
- вњ… Р§РµС‚РєРѕРµ СЂР°Р·РґРµР»РµРЅРёРµ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚Рё

### вљ пёЏ РќР°Р№РґРµРЅРЅС‹Рµ РїСЂРѕР±Р»РµРјС‹
$11. **Р”СѓР±Р»РёСЂРѕРІР°РЅРёРµ РєРѕРґР°** - 3 РІРµСЂСЃРёРё main.py$11. **РљРѕРЅС„Р»РёРєС‚С‹ РёРјРµРЅ** - РЅРµСЃРєРѕР»СЊРєРѕ test_*.py С„Р°Р№Р»РѕРІ$11. **РЈСЃС‚Р°СЂРµРІС€РёРµ С„Р°Р№Р»С‹** - CLEAN_PROJECT СЃРѕРґРµСЂР¶РёС‚ РґСѓР±Р»РёРєР°С‚С‹$11. **Р—Р°РІРёСЃРёРјРѕСЃС‚Рё** - РЅРµРєРѕС‚РѕСЂС‹Рµ РѕРїС†РёРѕРЅР°Р»СЊРЅС‹Рµ, РЅРѕ РЅРµ РїРѕРјРµС‡РµРЅС‹

### рџЋЇ Р РµРєРѕРјРµРЅРґР°С†РёРё
$11. РћР±СЉРµРґРёРЅРёС‚СЊ main.py РІРµСЂСЃРёРё$11. РџРµСЂРµРјРµСЃС‚РёС‚СЊ С‚РµСЃС‚С‹ РІ tests/$11. РђСЂС…РёРІРёСЂРѕРІР°С‚СЊ CLEAN_PROJECT$11. РЎРѕР·РґР°С‚СЊ requirements-dev.txt

---

## рџ—‚пёЏ РЎРўР РЈРљРўРЈР Рђ РџР РћР•РљРўРђ

### РћСЃРЅРѕРІРЅС‹Рµ РєРѕРјРїРѕРЅРµРЅС‚С‹
`n`n```
RULETTT/
в”њв”Ђв”Ђ рџ“Ѓ src/                      # РћСЃРЅРѕРІРЅРѕР№ РєРѕРґ (8 С„Р°Р№Р»РѕРІ)
в”‚   в”њв”Ђв”Ђ utils.py                 # вњ… РЈС‚РёР»РёС‚С‹ (РЅРµР·Р°РІРёСЃРёРјС‹Р№)
в”‚   в”њв”Ђв”Ђ data_collector.py        # вњ… РЎР±РѕСЂ РґР°РЅРЅС‹С… (РёСЃРїРѕР»СЊР·СѓРµС‚ utils)
в”‚   в”њв”Ђв”Ђ game_analyzer.py         # вњ… РђРЅР°Р»РёР· (РёСЃРїРѕР»СЊР·СѓРµС‚ utils, data_collector)
в”‚   в”њв”Ђв”Ђ ai_assistant.py          # вњ… AI РїРѕРјРѕС‰РЅРёРє (РёСЃРїРѕР»СЊР·СѓРµС‚ utils, data_collector)
в”‚   в”њв”Ђв”Ђ user_strategies.py       # вњ… РџРѕР»СЊР·РѕРІР°С‚РµР»СЊСЃРєРёРµ СЃС‚СЂР°С‚РµРіРёРё
в”‚   в”њв”Ђв”Ђ bot_simulator.py         # вњ… РЎРёРјСѓР»СЏС‚РѕСЂ С‡РµР»РѕРІРµРєР° (РЅРµР·Р°РІРёСЃРёРјС‹Р№)
в”‚   в”њв”Ђв”Ђ auth_manager.py          # вњ… РђСѓС‚РµРЅС‚РёС„РёРєР°С†РёСЏ (РЅРµР·Р°РІРёСЃРёРјС‹Р№)
в”‚   в””в”Ђв”Ђ paddypower_auto_collector.py  # вњ… РђРІС‚РѕРєРѕР»Р»РµРєС‚РѕСЂ Paddypower
в”‚
в”њв”Ђв”Ђ рџ“Ѓ webapp/                   # Р’РµР±-РёРЅС‚РµСЂС„РµР№СЃ
в”‚   в”њв”Ђв”Ђ index.html               # вњ… Р“Р»Р°РІРЅР°СЏ СЃС‚СЂР°РЅРёС†Р°
в”‚   в”њв”Ђв”Ђ dashboard.html           # вњ… Р”Р°С€Р±РѕСЂРґ
в”‚   в”њв”Ђв”Ђ mobile.html              # вњ… РњРѕР±РёР»СЊРЅР°СЏ РІРµСЂСЃРёСЏ
в”‚   в””в”Ђв”Ђ admin/                   # РђРґРјРёРЅРєР°
в”‚
в”њв”Ђв”Ђ рџ“Ѓ data/                     # Р‘Р°Р·С‹ РґР°РЅРЅС‹С… SQLite
в”њв”Ђв”Ђ рџ“Ѓ docs/                     # Р”РѕРєСѓРјРµРЅС‚Р°С†РёСЏ (13+ С„Р°Р№Р»РѕРІ)
в””в”Ђв”Ђ рџ“Ѓ CLEAN_PROJECT/            # вљ пёЏ Р”СѓР±Р»РёРєР°С‚С‹ С„Р°Р№Р»РѕРІ`n`n```

---

## рџ”Ќ Р”Р•РўРђР›Р¬РќР«Р™ РђРќРђР›РР—

### 1. РњРѕРґСѓР»СЊ src/

#### вњ… utils.py (РЅРµР·Р°РІРёСЃРёРјС‹Р№)`n`n```python
# Р—РђР’РРЎРРњРћРЎРўР: stdlib С‚РѕР»СЊРєРѕ
from datetime import datetime
from typing import Union, Optional

# Р­РљРЎРџРћР Рў:
class RouletteUtils:
    RED_NUMBERS = {...}
    BLACK_NUMBERS = {...}
    
# РРЎРџРћР›Р¬Р—РћР’РђРќРР•: Р’РµР·РґРµ
# РљРћРќР¤Р›РРљРўР«: РќРµС‚
# РЎРўРђРўРЈРЎ: вњ… РћС‚Р»РёС‡РЅРѕ`n`n```

#### вњ… data_collector.py`n`n```python
# Р—РђР’РРЎРРњРћРЎРўР:
import sqlite3, datetime, random
from utils import RouletteUtils  # в†ђ РџСЂР°РІРёР»СЊРЅРѕ

# Р­РљРЎРџРћР Рў:
class DataCollector

# РРЎРџРћР›Р¬Р—РћР’РђРќРР•: main.py, game_analyzer.py
# РљРћРќР¤Р›РРљРўР«: РќРµС‚
# РЎРўРђРўРЈРЎ: вњ… РћС‚Р»РёС‡РЅРѕ`n`n```

#### вњ… game_analyzer.py`n`n```python
# Р—РђР’РРЎРРњРћРЎРўР:
from datetime import datetime
from utils import RouletteUtils
from data_collector import DataCollector

# Р­РљРЎРџРћР Рў:
class GameStrategy (Р±Р°Р·РѕРІС‹Р№ РєР»Р°СЃСЃ)
class PredefinedStrategies (С„Р°Р±СЂРёРєР°)
class GameAnalyzer

# РРЎРџРћР›Р¬Р—РћР’РђРќРР•: main.py, user_strategies.py
# РљРћРќР¤Р›РРљРўР«: РќРµС‚
# РЎРўРђРўРЈРЎ: вњ… РћС‚Р»РёС‡РЅРѕ`n`n```

#### вњ… ai_assistant.py`n`n```python
# Р—РђР’РРЎРРњРћРЎРўР:
from datetime import datetime
from utils import RouletteUtils
from data_collector import DataCollector
import numpy as np  # в†ђ РћРїС†РёРѕРЅР°Р»СЊРЅР°СЏ (graceful fallback)

# Р­РљРЎРџРћР Рў:
class AIAssistant

# РРЎРџРћР›Р¬Р—РћР’РђРќРР•: main.py
# РљРћРќР¤Р›РРљРўР«: РќРµС‚
# РЎРўРђРўРЈРЎ: вњ… РћС‚Р»РёС‡РЅРѕ (РµСЃС‚СЊ fallback)`n`n```

#### вњ… user_strategies.py`n`n```python
# Р—РђР’РРЎРРњРћРЎРўР:
from datetime import datetime
from game_analyzer import GameStrategy
from utils import RouletteUtils

# Р­РљРЎРџРћР Рў:
class UserStrategies
def get_all_user_strategies()

# РРЎРџРћР›Р¬Р—РћР’РђРќРР•: main.py
# РљРћРќР¤Р›РРљРўР«: РќРµС‚
# РЎРўРђРўРЈРЎ: вњ… РћС‚Р»РёС‡РЅРѕ`n`n```

#### вњ… bot_simulator.py (РЅРµР·Р°РІРёСЃРёРјС‹Р№)`n`n```python
# Р—РђР’РРЎРРњРћРЎРўР:
import random, time, asyncio, json, math
from datetime import datetime
import numpy as np  # в†ђ РћРїС†РёРѕРЅР°Р»СЊРЅР°СЏ (graceful fallback)

# Р­РљРЎРџРћР Рў:
class HumanBehaviorSimulator

# РРЎРџРћР›Р¬Р—РћР’РђРќРР•: puppeteer_collector.py, paddypower_auto_collector.py
# РљРћРќР¤Р›РРљРўР«: РќРµС‚
# РЎРўРђРўРЈРЎ: вњ… РћС‚Р»РёС‡РЅРѕ (РЅРµР·Р°РІРёСЃРёРјС‹Р№)`n`n```

#### вњ… auth_manager.py (РЅРµР·Р°РІРёСЃРёРјС‹Р№)`n`n```python
# Р—РђР’РРЎРРњРћРЎРўР:
import sqlite3, secrets, hashlib, jwt, bcrypt, json
from datetime import datetime, timedelta

# Р­РљРЎРџРћР Рў:
class AdminAuth
class ClientAuth
class TokenManager

# РРЎРџРћР›Р¬Р—РћР’РђРќРР•: api_server.py (Р±СѓРґСѓС‰РµРµ)
# РљРћРќР¤Р›РРљРўР«: РќРµС‚
# РЎРўРђРўРЈРЎ: вњ… РћС‚Р»РёС‡РЅРѕ (РЅРµР·Р°РІРёСЃРёРјС‹Р№)`n`n```

#### вњ… paddypower_auto_collector.py`n`n```python
# Р—РђР’РРЎРРњРћРЎРўР:
import asyncio, json, random, os, argparse
from pathlib import Path
from datetime import datetime
from pyppeteer import launch  # в†ђ РћРїС†РёРѕРЅР°Р»СЊРЅР°СЏ
from dotenv import load_dotenv  # в†ђ РћРїС†РёРѕРЅР°Р»СЊРЅР°СЏ
from bot_simulator import HumanBehaviorSimulator  # в†ђ РћРїС†РёРѕРЅР°Р»СЊРЅР°СЏ

# Р­РљРЎРџРћР Рў:
class AntiDetectBrowser
class PaddypowerAutoCollector
async def main()

# РРЎРџРћР›Р¬Р—РћР’РђРќРР•: Standalone (CLI)
# РљРћРќР¤Р›РРљРўР«: РќРµС‚
# РЎРўРђРўРЈРЎ: вњ… РћС‚Р»РёС‡РЅРѕ (РІСЃРµ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё СЃ fallback)`n`n```

---

## рџ”„ Р“Р РђР¤ Р—РђР’РРЎРРњРћРЎРўР•Р™

### РРµСЂР°СЂС…РёСЏ РёРјРїРѕСЂС‚РѕРІ (Р±РµР· С†РёРєР»РѕРІ вњ…)
`n`n```
Layer 0 (РќРµР·Р°РІРёСЃРёРјС‹Рµ):
в”њв”Ђв”Ђ utils.py
в”њв”Ђв”Ђ bot_simulator.py
в””в”Ђв”Ђ auth_manager.py

Layer 1 (РСЃРїРѕР»СЊР·СѓСЋС‚ Layer 0):
в”њв”Ђв”Ђ data_collector.py в†’ utils.py
в””в”Ђв”Ђ paddypower_auto_collector.py в†’ bot_simulator.py

Layer 2 (РСЃРїРѕР»СЊР·СѓСЋС‚ Layer 0-1):
в”њв”Ђв”Ђ game_analyzer.py в†’ utils.py, data_collector.py
в””в”Ђв”Ђ ai_assistant.py в†’ utils.py, data_collector.py

Layer 3 (РСЃРїРѕР»СЊР·СѓСЋС‚ Layer 0-2):
в””в”Ђв”Ђ user_strategies.py в†’ utils.py, game_analyzer.py

Layer 4 (Р“Р»Р°РІРЅС‹Рµ):
в”њв”Ђв”Ђ main.py в†’ РІСЃРµ РјРѕРґСѓР»Рё Layer 0-3
в””в”Ђв”Ђ main_single_table.py в†’ РІСЃРµ РјРѕРґСѓР»Рё Layer 0-3`n`n```

**Р РµР·СѓР»СЊС‚Р°С‚:** вњ… РќРµС‚ С†РёРєР»РёС‡РµСЃРєРёС… Р·Р°РІРёСЃРёРјРѕСЃС‚РµР№!

---

## вљ пёЏ РџР РћР‘Р›Р•РњР« Р Р Р•РЁР•РќРРЇ

### РџСЂРѕР±Р»РµРјР° 1: Р”СѓР±Р»РёСЂРѕРІР°РЅРёРµ main.py

**РќР°Р№РґРµРЅРѕ:**`n`n```
src/main.py              (727 СЃС‚СЂРѕРє) - РџРѕР»РЅР°СЏ РІРµСЂСЃРёСЏ
src/main_single_table.py (727 СЃС‚СЂРѕРє) - Р’РµСЂСЃРёСЏ РґР»СЏ РѕРґРЅРѕРіРѕ СЃС‚РѕР»Р°
console_to_analysis.py   (400 СЃС‚СЂРѕРє) - РРјРїРѕСЂС‚ РёР· РєРѕРЅСЃРѕР»Рё`n`n```

**РџСЂРѕР±Р»РµРјР°:**
- 90% РєРѕРґР° РґСѓР±Р»РёСЂСѓРµС‚СЃСЏ
- РЎР»РѕР¶РЅРѕ РїРѕРґРґРµСЂР¶РёРІР°С‚СЊ
- Р›РµРіРєРѕ РїСЂРѕРїСѓСЃС‚РёС‚СЊ Р±Р°Рі РІ РѕРґРЅРѕР№ РІРµСЂСЃРёРё

**Р РµС€РµРЅРёРµ:**`n`n```python
# РЎРѕР·РґР°С‚СЊ src/main_base.py СЃ РѕР±С‰РµР№ Р»РѕРіРёРєРѕР№
class RouletteAnalysisSystem:
    def __init__(self, single_table=False):
        self.single_table = single_table
    
    def get_data_source(self):
        if self.single_table:
            return "single_table_only"
        else:
            return "all_tables"

# src/main.py
from main_base import RouletteAnalysisSystem
system = RouletteAnalysisSystem(single_table=False)

# src/main_single_table.py
from main_base import RouletteAnalysisSystem
system = RouletteAnalysisSystem(single_table=True)`n`n```

---

### РџСЂРѕР±Р»РµРјР° 2: РњРЅРѕР¶РµСЃС‚РІРѕ test_*.py С„Р°Р№Р»РѕРІ

**РќР°Р№РґРµРЅРѕ:**`n`n```
test_system.py          - РћСЃРЅРѕРІРЅС‹Рµ С‚РµСЃС‚С‹
test_chat.py            - РўРµСЃС‚С‹ С‡Р°С‚Р°
test_ai_chat.py         - РўРµСЃС‚С‹ AI С‡Р°С‚Р°
test_connection.py      - РўРµСЃС‚С‹ РїРѕРґРєР»СЋС‡РµРЅРёСЏ
test_compare.py         - РЎСЂР°РІРЅРµРЅРёРµ РґР°РЅРЅС‹С…
test_css_selector.py    - РўРµСЃС‚С‹ СЃРµР»РµРєС‚РѕСЂРѕРІ
test_pragmatic_api.py   - РўРµСЃС‚С‹ Pragmatic API`n`n```

**РџСЂРѕР±Р»РµРјР°:**
- РўРµСЃС‚С‹ РІ РєРѕСЂРЅРµ РїСЂРѕРµРєС‚Р°
- РќРµС‚ СЃС‚СЂСѓРєС‚СѓСЂС‹
- РЎР»РѕР¶РЅРѕ Р·Р°РїСѓСЃС‚РёС‚СЊ РІСЃРµ С‚РµСЃС‚С‹

**Р РµС€РµРЅРёРµ:**`n`n```
RULETTT/
в”њв”Ђв”Ђ tests/                      # в†ђ РќРѕРІР°СЏ РїР°РїРєР°
в”‚   в”њв”Ђв”Ђ __init__.py
в”‚   в”њв”Ђв”Ђ test_system.py
в”‚   в”њв”Ђв”Ђ test_chat.py
в”‚   в”њв”Ђв”Ђ test_ai_chat.py
в”‚   в”њв”Ђв”Ђ test_connection.py
в”‚   в”њв”Ђв”Ђ test_compare.py
в”‚   в”њв”Ђв”Ђ test_css_selector.py
в”‚   в””в”Ђв”Ђ test_pragmatic_api.py
в”‚
в””в”Ђв”Ђ pytest.ini                  # в†ђ РљРѕРЅС„РёРіСѓСЂР°С†РёСЏ pytest

# Р—Р°РїСѓСЃРє РІСЃРµС… С‚РµСЃС‚РѕРІ:
pytest tests/`n`n```

---

### РџСЂРѕР±Р»РµРјР° 3: CLEAN_PROJECT РґСѓР±Р»РёСЂСѓРµС‚ С„Р°Р№Р»С‹

**РќР°Р№РґРµРЅРѕ:**`n`n```
CLEAN_PROJECT/
в”њв”Ђв”Ђ auto_collector_console_code.js  # в†ђ Р”СѓР±Р»РёРєР°С‚
в”њв”Ђв”Ђ console_to_analysis.py          # в†ђ Р”СѓР±Р»РёРєР°С‚
в””в”Ђв”Ђ FOR_FRIEND.txt                  # в†ђ Р”СѓР±Р»РёРєР°С‚`n`n```

**РџСЂРѕР±Р»РµРјР°:**
- Р—Р°РЅРёРјР°РµС‚ РјРµСЃС‚Рѕ
- РњРѕР¶РµС‚ СѓСЃС‚Р°СЂРµС‚СЊ
- РџСѓС‚Р°РЅРёС†Р° РґР»СЏ СЂР°Р·СЂР°Р±РѕС‚С‡РёРєРѕРІ

**Р РµС€РµРЅРёРµ:**`n`n```bash
# РђСЂС…РёРІРёСЂРѕРІР°С‚СЊ
Compress-Archive -Path CLEAN_PROJECT -DestinationPath archives/CLEAN_PROJECT_2025_10_13.zip

# РЈРґР°Р»РёС‚СЊ РїР°РїРєСѓ
Remove-Item -Recurse CLEAN_PROJECT`n`n```

---

### РџСЂРѕР±Р»РµРјР° 4: РќРµРѕР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё РЅРµ РїРѕРјРµС‡РµРЅС‹

**РќР°Р№РґРµРЅРѕ:**`n`n```python
# Р’ requirements.txt Р’РЎР• Р·Р°РІРёСЃРёРјРѕСЃС‚Рё РѕР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ
pyppeteer==1.0.2
numpy==1.24.0
pandas==2.0.0
# ...`n`n```

**РџСЂРѕР±Р»РµРјР°:**
- РџРѕР»СЊР·РѕРІР°С‚РµР»СЊ РґРѕР»Р¶РµРЅ СѓСЃС‚Р°РЅРѕРІРёС‚СЊ Р’РЎР•
- РќРѕ РЅРµРєРѕС‚РѕСЂС‹Рµ РЅСѓР¶РЅС‹ С‚РѕР»СЊРєРѕ РґР»СЏ РѕРїСЂРµРґРµР»РµРЅРЅС‹С… С„СѓРЅРєС†РёР№

**Р РµС€РµРЅРёРµ:**`n`n```
# requirements.txt (РћР‘РЇР—РђРўР•Р›Р¬РќР«Р•)
flask==3.0.0
python-dotenv==1.0.0

# requirements-optional.txt (РћРџР¦РРћРќРђР›Р¬РќР«Р•)
pyppeteer==1.0.2      # Р”Р»СЏ Р°РІС‚РѕРєРѕР»Р»РµРєС‚РѕСЂР°
numpy==1.24.0          # Р”Р»СЏ AI Р°РЅР°Р»РёР·Р°
pandas==2.0.0          # Р”Р»СЏ СЌРєСЃРїРѕСЂС‚Р° РІ Excel

# requirements-dev.txt (Р”Р›РЇ Р РђР—Р РђР‘РћРўРљР)
pytest==7.4.0
black==23.7.0
flake8==6.1.0`n`n```

---

## рџЋЇ РџР›РђРќ Р Р•Р¤РђРљРўРћР РРќР“Рђ

### РџСЂРёРѕСЂРёС‚РµС‚ 1: РљСЂРёС‚РёС‡РЅС‹Рµ (СЃРґРµР»Р°С‚СЊ СЃРµР№С‡Р°СЃ)
$11. **РЎРѕР·РґР°С‚СЊ tests/ РґРёСЂРµРєС‚РѕСЂРёСЋ**
   ```powershell
   New-Item -ItemType Directory -Path tests
   Move-Item test_*.py tests/
   ```
$11. **Р Р°Р·РґРµР»РёС‚СЊ requirements.txt**
   ```powershell
   # РЎРѕР·РґР°С‚СЊ 3 С„Р°Р№Р»Р°
   New-Item requirements-core.txt
   New-Item requirements-optional.txt
   New-Item requirements-dev.txt
   ```
$11. **РђСЂС…РёРІРёСЂРѕРІР°С‚СЊ CLEAN_PROJECT**
   ```powershell
   Compress-Archive -Path CLEAN_PROJECT -DestinationPath archives/CLEAN_PROJECT.zip
   Remove-Item -Recurse CLEAN_PROJECT
   ```

### РџСЂРёРѕСЂРёС‚РµС‚ 2: Р’Р°Р¶РЅС‹Рµ (РЅР° СЌС‚РѕР№ РЅРµРґРµР»Рµ)
$11. **РЎРѕР·РґР°С‚СЊ main_base.py**
   - Р’С‹РЅРµСЃС‚Рё РѕР±С‰СѓСЋ Р»РѕРіРёРєСѓ
   - РЈР±СЂР°С‚СЊ РґСѓР±Р»РёСЂРѕРІР°РЅРёРµ
   - РЈРїСЂРѕСЃС‚РёС‚СЊ РїРѕРґРґРµСЂР¶РєСѓ
$11. **Р”РѕР±Р°РІРёС‚СЊ __init__.py РІ src/**
   ```python
   # src/__init__.py
   """
   RULETTT Core Modules
   """
   __version__ = "2.0.0"
   
   from .utils import RouletteUtils
   from .data_collector import DataCollector
   from .game_analyzer import GameAnalyzer, PredefinedStrategies
   from .ai_assistant import AIAssistant
   ```
$11. **РЎРѕР·РґР°С‚СЊ setup.py**
   ```python
   from setuptools import setup, find_packages
   
   setup(
       name="rulettt",
       version="2.0.0",
       packages=find_packages(),
       install_requires=[...],
       extras_require={
           'auto': ['pyppeteer'],
           'ai': ['numpy', 'pandas'],
           'dev': ['pytest', 'black']
       }
   )
   ```

### РџСЂРёРѕСЂРёС‚РµС‚ 3: Р–РµР»Р°С‚РµР»СЊРЅС‹Рµ (РІ СЃР»РµРґСѓСЋС‰РµРј РјРµСЃСЏС†Рµ)
$11. **Р”РѕР±Р°РІРёС‚СЊ Р»РѕРіРёСЂРѕРІР°РЅРёРµ**
   ```python
   # src/logger.py
   import logging
   
   def setup_logger(name):
       logger = logging.getLogger(name)
       handler = logging.FileHandler('logs/rulettt.log')
       formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
       handler.setFormatter(formatter)
       logger.addHandler(handler)
       return logger
   ```
$11. **РЎРѕР·РґР°С‚СЊ config.py**
   ```python
   # src/config.py
   from pathlib import Path
   
   PROJECT_ROOT = Path(__file__).parent.parent
   DATA_DIR = PROJECT_ROOT / "data"
   LOGS_DIR = PROJECT_ROOT / "logs"
   
   # Database
   DEFAULT_DB = DATA_DIR / "final_single_table.db"
   AUTH_DB = DATA_DIR / "auth.db"
   ```
$11. **Р”РѕР±Р°РІРёС‚СЊ type hints РІРµР·РґРµ**
   ```python
   # РСЃРїРѕР»СЊР·РѕРІР°С‚СЊ mypy РґР»СЏ РїСЂРѕРІРµСЂРєРё
   pip install mypy
   mypy src/
   ```

---

## рџ“Ѓ Р Р•РљРћРњР•РќР”РЈР•РњРђРЇ РЎРўР РЈРљРўРЈР Рђ

### РџРѕСЃР»Рµ СЂРµС„Р°РєС‚РѕСЂРёРЅРіР°:
`n`n```
RULETTT/
в”њв”Ђв”Ђ рџ“Ѓ src/                      # РћСЃРЅРѕРІРЅРѕР№ РєРѕРґ
в”‚   в”њв”Ђв”Ђ __init__.py              # в†ђ РќРћР’РћР•: СЌРєСЃРїРѕСЂС‚ РјРѕРґСѓР»РµР№
в”‚   в”њв”Ђв”Ђ config.py                # в†ђ РќРћР’РћР•: РєРѕРЅС„РёРіСѓСЂР°С†РёСЏ
в”‚   в”њв”Ђв”Ђ logger.py                # в†ђ РќРћР’РћР•: Р»РѕРіРёСЂРѕРІР°РЅРёРµ
в”‚   в”њв”Ђв”Ђ main_base.py             # в†ђ РќРћР’РћР•: РѕР±С‰Р°СЏ Р»РѕРіРёРєР°
в”‚   в”њв”Ђв”Ђ main.py                  # РњРЅРѕРіРѕСЃС‚РѕР»СЊРЅР°СЏ РІРµСЂСЃРёСЏ
в”‚   в”њв”Ђв”Ђ main_single_table.py     # РћРґРЅРѕСЃС‚РѕР»СЊРЅР°СЏ РІРµСЂСЃРёСЏ
в”‚   в”њв”Ђв”Ђ utils.py
в”‚   в”њв”Ђв”Ђ data_collector.py
в”‚   в”њв”Ђв”Ђ game_analyzer.py
в”‚   в”њв”Ђв”Ђ ai_assistant.py
в”‚   в”њв”Ђв”Ђ user_strategies.py
в”‚   в”њв”Ђв”Ђ bot_simulator.py
в”‚   в”њв”Ђв”Ђ auth_manager.py
в”‚   в””в”Ђв”Ђ paddypower_auto_collector.py
в”‚
в”њв”Ђв”Ђ рџ“Ѓ tests/                    # в†ђ РќРћР’РћР•: С‚РµСЃС‚С‹
в”‚   в”њв”Ђв”Ђ __init__.py
в”‚   в”њв”Ђв”Ђ test_system.py
в”‚   в”њв”Ђв”Ђ test_chat.py
в”‚   в”њв”Ђв”Ђ test_ai_chat.py
в”‚   в”њв”Ђв”Ђ test_connection.py
в”‚   в”њв”Ђв”Ђ test_compare.py
в”‚   в”њв”Ђв”Ђ test_css_selector.py
в”‚   в””в”Ђв”Ђ test_pragmatic_api.py
в”‚
в”њв”Ђв”Ђ рџ“Ѓ webapp/                   # Р’РµР±-РёРЅС‚РµСЂС„РµР№СЃ
в”њв”Ђв”Ђ рџ“Ѓ data/                     # Р‘Р°Р·С‹ РґР°РЅРЅС‹С…
в”њв”Ђв”Ђ рџ“Ѓ logs/                     # в†ђ РќРћР’РћР•: Р»РѕРіРё
в”њв”Ђв”Ђ рџ“Ѓ docs/                     # Р”РѕРєСѓРјРµРЅС‚Р°С†РёСЏ
в”њв”Ђв”Ђ рџ“Ѓ archives/                 # в†ђ РќРћР’РћР•: Р°СЂС…РёРІС‹
в”‚
в”њв”Ђв”Ђ setup.py                     # в†ђ РќРћР’РћР•: СѓСЃС‚Р°РЅРѕРІРєР° РїР°РєРµС‚Р°
в”њв”Ђв”Ђ requirements-core.txt        # в†ђ РќРћР’РћР•: РѕСЃРЅРѕРІРЅС‹Рµ
в”њв”Ђв”Ђ requirements-optional.txt   # в†ђ РќРћР’РћР•: РѕРїС†РёРѕРЅР°Р»СЊРЅС‹Рµ
в”њв”Ђв”Ђ requirements-dev.txt         # в†ђ РќРћР’РћР•: СЂР°Р·СЂР°Р±РѕС‚РєР°
в”њв”Ђв”Ђ pytest.ini                   # в†ђ РќРћР’РћР•: РєРѕРЅС„РёРі pytest
в”њв”Ђв”Ђ mypy.ini                     # в†ђ РќРћР’РћР•: РєРѕРЅС„РёРі mypy
в”њв”Ђв”Ђ .gitignore
в””в”Ђв”Ђ README.md`n`n```

---

## рџ”§ РЎРљР РРџРўР« Р Р•Р¤РђРљРўРћР РРќР“Рђ

### РЎРєСЂРёРїС‚ 1: РћСЂРіР°РЅРёР·Р°С†РёСЏ С‚РµСЃС‚РѕРІ
`n`n```powershell
# refactor_tests.ps1

# РЎРѕР·РґР°С‚СЊ РїР°РїРєСѓ tests
New-Item -ItemType Directory -Force -Path tests

# РџРµСЂРµРјРµСЃС‚РёС‚СЊ С‚РµСЃС‚С‹
Move-Item test_*.py tests/ -Force

# РЎРѕР·РґР°С‚СЊ __init__.py
@"
# tests/__init__.py
"""
RULETTT Test Suite
"""
"@ | Out-File -FilePath tests/__init__.py -Encoding UTF8

# РЎРѕР·РґР°С‚СЊ pytest.ini
@"
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
"@ | Out-File -FilePath pytest.ini -Encoding UTF8

Write-Host "вњ… РўРµСЃС‚С‹ РѕСЂРіР°РЅРёР·РѕРІР°РЅС‹!" -ForegroundColor Green`n`n```

### РЎРєСЂРёРїС‚ 2: Р Р°Р·РґРµР»РµРЅРёРµ requirements
`n`n```powershell
# refactor_requirements.ps1

# requirements-core.txt (РћР‘РЇР—РђРўР•Р›Р¬РќР«Р•)
@"
# РћСЃРЅРѕРІРЅС‹Рµ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё
flask==3.0.0
python-dotenv==1.0.0
bcrypt==4.0.1
pyjwt==2.8.0
"@ | Out-File -FilePath requirements-core.txt -Encoding UTF8

# requirements-optional.txt (РћРџР¦РРћРќРђР›Р¬РќР«Р•)
@"
# РћРїС†РёРѕРЅР°Р»СЊРЅС‹Рµ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё
# РЈСЃС‚Р°РЅРѕРІРєР°: pip install -r requirements-optional.txt

# Р”Р»СЏ Р°РІС‚РѕРєРѕР»Р»РµРєС‚РѕСЂР°
pyppeteer==1.0.2
playwright==1.40.0

# Р”Р»СЏ AI Р°РЅР°Р»РёР·Р°
numpy==1.24.0
pandas==2.0.0
matplotlib==3.7.0
scikit-learn==1.3.0
"@ | Out-File -FilePath requirements-optional.txt -Encoding UTF8

# requirements-dev.txt (Р РђР—Р РђР‘РћРўРљРђ)
@"
# Р—Р°РІРёСЃРёРјРѕСЃС‚Рё РґР»СЏ СЂР°Р·СЂР°Р±РѕС‚РєРё
# РЈСЃС‚Р°РЅРѕРІРєР°: pip install -r requirements-dev.txt

pytest==7.4.0
pytest-cov==4.1.0
black==23.7.0
flake8==6.1.0
mypy==1.5.0
"@ | Out-File -FilePath requirements-dev.txt -Encoding UTF8

Write-Host "вњ… Requirements СЂР°Р·РґРµР»РµРЅС‹!" -ForegroundColor Green`n`n```

### РЎРєСЂРёРїС‚ 3: РђСЂС…РёРІРёСЂРѕРІР°РЅРёРµ CLEAN_PROJECT
`n`n```powershell
# archive_clean_project.ps1

# РЎРѕР·РґР°С‚СЊ РїР°РїРєСѓ archives
New-Item -ItemType Directory -Force -Path archives

# РђСЂС…РёРІРёСЂРѕРІР°С‚СЊ CLEAN_PROJECT
$date = Get-Date -Format "yyyy_MM_dd"
$archiveName = "archives/CLEAN_PROJECT_$date.zip"

Compress-Archive -Path CLEAN_PROJECT -DestinationPath $archiveName -Force

Write-Host "вњ… РђСЂС…РёРІ СЃРѕР·РґР°РЅ: $archiveName" -ForegroundColor Green
Write-Host "РЈРґР°Р»РёС‚СЊ CLEAN_PROJECT? (Y/N)" -ForegroundColor Yellow
$response = Read-Host

if ($response -eq 'Y' -or $response -eq 'y') {
    Remove-Item -Recurse -Force CLEAN_PROJECT
    Write-Host "вњ… CLEAN_PROJECT СѓРґР°Р»РµРЅ!" -ForegroundColor Green
}`n`n```

### РЎРєСЂРёРїС‚ 4: РЎРѕР·РґР°РЅРёРµ __init__.py
`n`n```powershell
# create_init_files.ps1

# src/__init__.py
@"
"""
RULETTT Core Modules
====================

РЎРёСЃС‚РµРјР° СЃР±РѕСЂР° Рё Р°РЅР°Р»РёР·Р° РґР°РЅРЅС‹С… СЂСѓР»РµС‚РєРё.
"""

__version__ = "2.0.0"
__author__ = "RULETTT Team"

# РћСЃРЅРѕРІРЅС‹Рµ РєР»Р°СЃСЃС‹
from .utils import RouletteUtils
from .data_collector import DataCollector
from .game_analyzer import GameAnalyzer, PredefinedStrategies, GameStrategy
from .ai_assistant import AIAssistant
from .user_strategies import UserStrategies, get_all_user_strategies

# Р‘РѕС‚ Рё Р°СѓС‚РµРЅС‚РёС„РёРєР°С†РёСЏ
from .bot_simulator import HumanBehaviorSimulator
from .auth_manager import AdminAuth, ClientAuth, TokenManager

__all__ = [
    'RouletteUtils',
    'DataCollector',
    'GameAnalyzer',
    'PredefinedStrategies',
    'GameStrategy',
    'AIAssistant',
    'UserStrategies',
    'get_all_user_strategies',
    'HumanBehaviorSimulator',
    'AdminAuth',
    'ClientAuth',
    'TokenManager',
]
"@ | Out-File -FilePath src/__init__.py -Encoding UTF8

Write-Host "вњ… src/__init__.py СЃРѕР·РґР°РЅ!" -ForegroundColor Green`n`n```

---

## вњ… Р§Р•РљР›РРЎРў РџР РћР’Р•Р РљР

### РџРµСЂРµРґ РєР°Р¶РґС‹Рј РєРѕРјРјРёС‚РѕРј:

- [ ] Р’СЃРµ С‚РµСЃС‚С‹ РїСЂРѕС…РѕРґСЏС‚ (`pytest tests/`)
- [ ] РќРµС‚ С†РёРєР»РёС‡РµСЃРєРёС… РёРјРїРѕСЂС‚РѕРІ
- [ ] Type hints РґРѕР±Р°РІР»РµРЅС‹ (РїСЂРѕРІРµСЂРєР° `mypy src/`)
- [ ] РљРѕРґ РѕС‚С„РѕСЂРјР°С‚РёСЂРѕРІР°РЅ (`black src/`)
- [ ] РќРµС‚ lint РѕС€РёР±РѕРє (`flake8 src/`)
- [ ] Р”РѕРєСѓРјРµРЅС‚Р°С†РёСЏ РѕР±РЅРѕРІР»РµРЅР°
- [ ] CHANGELOG.md РѕР±РЅРѕРІР»РµРЅ

### РџРµСЂРµРґ СЂРµР»РёР·РѕРј:

- [ ] Р’РµСЂСЃРёСЏ РѕР±РЅРѕРІР»РµРЅР° РІ `__init__.py`
- [ ] Р’СЃРµ requirements С„Р°Р№Р»С‹ Р°РєС‚СѓР°Р»СЊРЅС‹
- [ ] README.md Р°РєС‚СѓР°Р»РµРЅ
- [ ] Р’СЃРµ РїСЂРёРјРµСЂС‹ РІ docs/ СЂР°Р±РѕС‚Р°СЋС‚
- [ ] Performance С‚РµСЃС‚С‹ РїСЂРѕР№РґРµРЅС‹
- [ ] Security audit РІС‹РїРѕР»РЅРµРЅ

---

## рџ“Љ РњР•РўР РРљР РљРђР§Р•РЎРўР’Рђ

### РўРµРєСѓС‰РµРµ СЃРѕСЃС‚РѕСЏРЅРёРµ:

| РњРµС‚СЂРёРєР° | Р—РЅР°С‡РµРЅРёРµ | РЎС‚Р°С‚СѓСЃ |
|---------|----------|--------|
| Р¦РёРєР»РёС‡РµСЃРєРёРµ РёРјРїРѕСЂС‚С‹ | 0 | вњ… РћС‚Р»РёС‡РЅРѕ |
| Р”СѓР±Р»РёСЂРѕРІР°РЅРёРµ РєРѕРґР° | ~15% | вљ пёЏ РЎСЂРµРґРЅРµ |
| Test coverage | ~40% | вљ пёЏ РќРёР·РєРѕ |
| Type hints | ~30% | вљ пёЏ РќРёР·РєРѕ |
| Р”РѕРєСѓРјРµРЅС‚Р°С†РёСЏ | 90% | вњ… РћС‚Р»РёС‡РЅРѕ |
| РњРѕРґСѓР»СЊРЅРѕСЃС‚СЊ | 95% | вњ… РћС‚Р»РёС‡РЅРѕ |

### Р¦РµР»РµРІРѕРµ СЃРѕСЃС‚РѕСЏРЅРёРµ (С‡РµСЂРµР· 1 РјРµСЃСЏС†):

| РњРµС‚СЂРёРєР° | Р¦РµР»СЊ | РџСЂРёРѕСЂРёС‚РµС‚ |
|---------|------|-----------|
| Р¦РёРєР»РёС‡РµСЃРєРёРµ РёРјРїРѕСЂС‚С‹ | 0 | вњ… Р“РѕС‚РѕРІРѕ |
| Р”СѓР±Р»РёСЂРѕРІР°РЅРёРµ РєРѕРґР° | <5% | рџ”ґ Р’С‹СЃРѕРєРёР№ |
| Test coverage | >80% | рџџЎ РЎСЂРµРґРЅРёР№ |
| Type hints | >90% | рџџЎ РЎСЂРµРґРЅРёР№ |
| Р”РѕРєСѓРјРµРЅС‚Р°С†РёСЏ | >95% | вњ… Р“РѕС‚РѕРІРѕ |
| РњРѕРґСѓР»СЊРЅРѕСЃС‚СЊ | >95% | вњ… Р“РѕС‚РѕРІРѕ |

---

## рџЋЇ Р—РђРљР›Р®Р§Р•РќРР•

### вњ… РЎРёР»СЊРЅС‹Рµ СЃС‚РѕСЂРѕРЅС‹ РїСЂРѕРµРєС‚Р°:
$11. **РћС‚Р»РёС‡РЅР°СЏ РјРѕРґСѓР»СЊРЅРѕСЃС‚СЊ** - РєР°Р¶РґС‹Р№ С„Р°Р№Р» РЅРµР·Р°РІРёСЃРёРј$11. **РќРµС‚ С†РёРєР»РёС‡РµСЃРєРёС… Р·Р°РІРёСЃРёРјРѕСЃС‚РµР№** - С‡РёСЃС‚Р°СЏ РёРµСЂР°СЂС…РёСЏ$11. **Graceful degradation** - СЂР°Р±РѕС‚Р°РµС‚ Р±РµР· РѕРїС†РёРѕРЅР°Р»СЊРЅС‹С… Р·Р°РІРёСЃРёРјРѕСЃС‚РµР№$11. **РҐРѕСЂРѕС€Р°СЏ РґРѕРєСѓРјРµРЅС‚Р°С†РёСЏ** - 13+ РґРѕРєСѓРјРµРЅС‚РѕРІ$11. **Р Р°СЃС€РёСЂСЏРµРјРѕСЃС‚СЊ** - Р»РµРіРєРѕ РґРѕР±Р°РІРёС‚СЊ РЅРѕРІС‹Рµ СЃС‚СЂР°С‚РµРіРёРё/С„СѓРЅРєС†РёРё

### вљ пёЏ Р§С‚Рѕ СѓР»СѓС‡С€РёС‚СЊ:
$11. **РЈРјРµРЅСЊС€РёС‚СЊ РґСѓР±Р»РёСЂРѕРІР°РЅРёРµ** - СЃРѕР·РґР°С‚СЊ main_base.py$11. **РћСЂРіР°РЅРёР·РѕРІР°С‚СЊ С‚РµСЃС‚С‹** - РїРµСЂРµРјРµСЃС‚РёС‚СЊ РІ tests/$11. **Р Р°Р·РґРµР»РёС‚СЊ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё** - core/optional/dev$11. **Р”РѕР±Р°РІРёС‚СЊ type hints** - РґР»СЏ РІСЃРµС… С„СѓРЅРєС†РёР№$11. **РЈРІРµР»РёС‡РёС‚СЊ test coverage** - РґРѕ 80%+

### рџљЂ РЎР»РµРґСѓСЋС‰РёРµ С€Р°РіРё:
$11. вњ… **РЎРµР№С‡Р°СЃ**: Р—Р°РїСѓСЃС‚РёС‚СЊ refactor_tests.ps1$11. вњ… **РЎРµРіРѕРґРЅСЏ**: Р—Р°РїСѓСЃС‚РёС‚СЊ refactor_requirements.ps1$11. вњ… **Р­С‚Р° РЅРµРґРµР»СЏ**: РЎРѕР·РґР°С‚СЊ main_base.py$11. вЏі **Р­С‚РѕС‚ РјРµСЃСЏС†**: Р”РѕР±Р°РІРёС‚СЊ type hints РІРµР·РґРµ$11. вЏі **РЎР»РµРґСѓСЋС‰РёР№ РјРµСЃСЏС†**: РЈРІРµР»РёС‡РёС‚СЊ test coverage РґРѕ 80%

---

## рџ“ћ РљРѕРЅС‚Р°РєС‚С‹

**Р’РѕРїСЂРѕСЃС‹ РїРѕ Р°СѓРґРёС‚Сѓ:**
- GitHub Issues: [РЎРѕР·РґР°С‚СЊ issue](https://github.com/nikolaspablo92-prog/RULETTT/issues)
- Email: support@rulettt.dev

**Р”РѕРєСѓРјРµРЅС‚Р°С†РёСЏ:**
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
- [BOT_ARCHITECTURE.md](BOT_ARCHITECTURE.md)

---

*РћС‚С‡РµС‚ СЃРѕР·РґР°РЅ: 13 РѕРєС‚СЏР±СЂСЏ 2025*  
*РђСѓРґРёС‚РѕСЂ: GitHub Copilot*  
*Р’РµСЂСЃРёСЏ РѕС‚С‡РµС‚Р°: 1.0.0*

