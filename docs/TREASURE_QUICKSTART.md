# 🎁 Treasure System - Quick Start Guide

## What Was Added

The optimizer now supports **Treasures** - powerful items that teams can equip (max 3) for stat bonuses and special effects.

---

## Quick Demo

### **1. Test Treasure Scoring (CLI)**

```bash
python3 test_treasure_scoring.py
```

**Expected Output:**
```
Team WITHOUT Treasures: 99.20 points
Team WITH S+ Treasures: 111.83 points (+12.62 bonus)

✓ Treasure bonus correctly applied
```

---

### **2. Test Counter-Team Treasures (CLI)**

```bash
python3 test_counter_treasures.py
```

**Expected Output:**
```
Enemy: Pure Vanilla, Shadow Milk, Cream Ferret, Hollyberry, Parfait

Recommended Treasures:
1. Dream Conductor's Whistle - "Burst damage to overwhelm healing"
2. Old Pilgrim's Scroll - "Burst damage to overwhelm healing"
3. Hollyberrian Royal Necklace - "Shield to survive Shadow Milk burst"

✓ Intelligent counter-treasure recommendations
```

---

### **3. Test API Endpoint**

```bash
python3 test_api_treasures.py
```

**Expected Output:**
```
✓ API endpoint working! Retrieved 21 treasures

Top 5 Treasures:
1. Old Pilgrim's Scroll (S+) - ATK +60%
2. Squishy Jelly Watch (S+) - CDR -25%
3. Dream Conductor's Whistle (S+) - ATK +40%, CRIT +15%
...
```

---

### **4. Test Web UI (Visual)**

```bash
cd web_ui
./start_web_ui.sh
```

**Then in browser:**
1. Go to `http://localhost:5000`
2. Click "Counter-Team Generator" tab
3. Select 5 enemy cookies (e.g., Pure Vanilla, Shadow Milk, etc.)
4. Click "Generate Counter-Teams"
5. **Look for the new "🎁 Recommended Treasures" section** in each team card

**What You Should See:**
- Each counter-team shows 3 recommended treasures
- Tier badges (S+, S, A, B, C) with color gradients
- Reason for each recommendation
- Stat effects displayed as badges

---

## Key Features

### **The "Holy Trinity" (S+ Tier)**

1. **Old Pilgrim's Scroll** - +60% ATK
   - Universal treasure, works with any team
   - Massive damage boost

2. **Squishy Jelly Watch** - -25% Cooldown
   - Faster skill rotation
   - More frequent abilities

3. **Dream Conductor's Whistle** - +40% ATK, +15% CRIT
   - Buffs 2 highest ATK cookies
   - Heals on buffed cookie death

**Pro Tip:** Use all 3 for maximum DPS team effectiveness!

---

## API Usage

### **Get All Treasures**

```bash
curl http://localhost:5000/api/treasures | jq
```

**Returns:**
```json
[
  {
    "name": "Old Pilgrim's Scroll",
    "tier_ranking": "S+",
    "atk_boost": 60.0,
    "primary_effect": "Increases ATK for all Cookies",
    "recommended_archetypes": ["Universal", "DPS", "Burst"],
    ...
  },
  ...
]
```

---

### **Generate Counter-Teams (includes treasures)**

```bash
curl -X POST http://localhost:5000/api/counter-teams \
  -H "Content-Type: application/json" \
  -d '{
    "enemyTeam": ["Pure Vanilla Cookie", "Shadow Milk Cookie", "Hollyberry Cookie", "Frost Queen Cookie", "Parfait Cookie"],
    "numCounterTeams": 3,
    "method": "greedy"
  }' | jq '.counterTeams[0].recommendedTreasures'
```

**Returns:**
```json
[
  {
    "name": "Dream Conductor's Whistle",
    "tier": "S+",
    "score": 30.5,
    "reason": "Burst damage to overwhelm healing",
    "effects": {
      "atk_boost": 40.0,
      "crit_boost": 15.0,
      "cooldown_reduction": 0.0,
      ...
    }
  },
  ...
]
```

---

## Python API

### **Recommend Treasures for a Team**

```python
from team_optimizer import TeamOptimizer, Team

optimizer = TeamOptimizer('crk-cookies.csv')

# Create a team
cookies = [optimizer.all_cookies[i] for i in range(5)]
team = Team(cookies)

# Get treasure recommendations
treasures = optimizer.recommend_treasures(team, top_n=3)

for treasure, score, reason in treasures:
    print(f"{treasure.name} ({treasure.tier_ranking})")
    print(f"  Score: {score:.1f}")
    print(f"  Reason: {reason}")
    print(f"  ATK: +{treasure.atk_boost_max}%")
    print()
```

---

### **Counter-Team with Treasures**

```python
from counter_team_generator import CounterTeamGenerator

generator = CounterTeamGenerator(optimizer)

# Create enemy team
enemy_cookies = [optimizer.all_cookies[i] for i in range(5)]
enemy_team = Team(enemy_cookies)

# Generate counter-teams
counter_teams = generator.find_counter_teams(enemy_team, n=3)

for team, info in counter_teams:
    print(f"\nCounter Score: {info['counter_score']:.1f}")
    print("Recommended Treasures:")
    for t in info['recommended_treasures']:
        print(f"  - {t['name']}: {t['reason']}")
```

---

## Visual Examples

### **Counter-Team Card (Web UI)**

```
┌─────────────────────────────────────────────────────────┐
│ #1 Counter-Team                                         │
│ Counter: 66.9/100 | Team: 52.7 | Combined: 61.2/100    │
├─────────────────────────────────────────────────────────┤
│ Strategy: Immunity to counter Stun crowd control       │
│                                                         │
│ Cookies: [5 cookie cards]                              │
│                                                         │
│ 🎁 Recommended Treasures                                │
│ ┌───────────────────────────────────────────────┐      │
│ │ Dream Conductor's Whistle              [S+]  │      │
│ │ Burst damage to overwhelm healing            │      │
│ │ [ATK +40%] [CRIT +15%] [DMG Resist +20%]     │      │
│ └───────────────────────────────────────────────┘      │
│                                                         │
│ ┌───────────────────────────────────────────────┐      │
│ │ Old Pilgrim's Scroll                   [S+]  │      │
│ │ Burst damage to overwhelm healing            │      │
│ │ [ATK +60%]                                   │      │
│ └───────────────────────────────────────────────┘      │
│                                                         │
│ ┌───────────────────────────────────────────────┐      │
│ │ Hollyberrian Royal Necklace            [A]   │      │
│ │ Shield to survive Shadow Milk burst         │      │
│ │ [DMG Resist +5%] [Shield +15%]               │      │
│ └───────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

---

## Treasure Tier Colors

- **S+**: 🟨 Golden gradient with glow
- **S**: 🟥 Pink/red gradient
- **A**: 🟪 Purple gradient
- **B**: 🟦 Blue gradient
- **C**: 🟩 Green gradient

---

## Common Treasure Recommendations

### **vs Healing-Heavy Teams**
→ Offensive treasures (Old Pilgrim's Scroll, Dream Conductor's Whistle)

### **vs Tank-Heavy Teams**
→ CDR treasures (Squishy Jelly Watch) + ATK boost

### **vs Shadow Milk**
→ Defensive treasures (Hollyberrian Royal Necklace, shields)

### **vs CC-Heavy Teams**
→ Sustain + cleanse treasures (Explorer's Monocle, Bookseller's Monocle)

### **vs Burst Damage Teams**
→ Shields + revival (Sugar Swan's Shining Feather, Sacred Pomegranate Branch)

---

## Files to Check

- **Treasure Database**: `crk_treasures.csv`
- **Test Scripts**: `test_treasure_*.py`
- **Backend Logic**: `team_optimizer.py`, `counter_team_generator.py`
- **API**: `web_ui/app.py`
- **Frontend**: `web_ui/static/app.js`, `web_ui/static/styles.css`

---

## Troubleshooting

**Issue**: Treasures not showing in web UI
**Fix**: Clear browser cache and refresh

**Issue**: API returns empty treasures
**Fix**: Check `crk_treasures.csv` exists in root directory

**Issue**: Python tests fail
**Fix**: Run from the project root directory

---

## Next Steps

The treasure system is **fully functional**. You can now:

1. ✅ Use treasures in team optimization
2. ✅ Get treasure recommendations for counter-teams
3. ✅ View treasures in web UI
4. ✅ Access treasure data via API

**Optional Enhancement:** Add a treasure browser/selector UI for manual treasure selection.

---

*Ready to use! All tests passing. Enjoy the treasure system! 🎁*
