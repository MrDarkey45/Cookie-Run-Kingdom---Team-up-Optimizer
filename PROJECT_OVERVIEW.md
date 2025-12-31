# Cookie Run: Kingdom - Team Optimizer

## 📁 Project Structure

```
Models/
├── 📄 Core Files (Main Application)
│   ├── cookie_analysis.py          # Original cookie data analysis
│   ├── team_optimizer.py           # Team optimization engine
│   ├── counter_team_generator.py   # Counter-team generation logic
│   ├── synergy_calculator.py       # Team synergy calculations
│   │
├── 📊 Data Files (CSV)
│   ├── crk-cookies.csv            # Main cookie database (177 cookies)
│   ├── cookie_abilities.csv        # Cookie abilities & skills data
│   ├── crk_treasures.csv          # Treasure database (21 treasures)
│   │
├── 🌐 Web Interface
│   └── web_ui/
│       ├── app.py                 # Flask backend API
│       ├── templates/
│       │   └── index.html         # Main web UI template
│       └── static/
│           ├── app.js             # Frontend JavaScript
│           └── styles.css         # UI styling
│
├── 🧪 Tests & Utilities
│   ├── tests/
│   │   ├── test_treasure_scoring.py
│   │   ├── test_counter_treasures.py
│   │   └── test_api_treasures.py
│   │
│   └── scripts/
│       ├── fix_ascended_cookies.py      # Fixed duplicate Ascended cookies
│       └── fix_abilities_ascended.py    # Fixed abilities CSV naming
│
└── 📚 Documentation
    ├── docs/
    │   ├── ASCENDED_COOKIE_FIX.md       # Ascended cookie bug fix details
    │   ├── TREASURE_QUICKSTART.md       # Treasure system quick guide
    │   └── TREASURE_INTEGRATION_SUMMARY.md  # Full treasure implementation
    │
    ├── README.md                    # Main project README
    └── PROJECT_OVERVIEW.md          # This file
```

---

## 🎯 Core Features

### 1. **Team Optimization**
- Generate optimal 5-cookie teams based on multiple strategies
- Methods: Random Sampling, Greedy, Genetic Algorithm, Exhaustive Search
- Scoring based on role diversity, position coverage, power, and synergy

### 2. **Counter-Team Generator**
- Analyze enemy team composition
- Identify weaknesses and generate counter-strategies
- Recommend specific cookies and treasures to counter enemy teams

### 3. **Treasure System**
- 21 treasures with stat bonuses and special effects
- Teams can equip up to 3 treasures
- Intelligent treasure recommendations based on team composition

### 4. **Cookie Stats Management**
- Track individual cookie stats (Level, Skill Level, Star Level, Toppings)
- Advanced mode uses stats for personalized team scoring
- Optional: works without stats using base rarity values

### 5. **Synergy Calculator**
- Role synergy matrix (tank + healer, DPS + support, etc.)
- Element matching bonuses
- Ability-based synergies (CC + Burst Damage, Heal + Shield, etc.)

---

## 🚀 Quick Start

### **Run Web UI**
```bash
cd web_ui
./start_web_ui.sh
# Or manually:
python3 app.py
```

Then open browser to: `http://localhost:5000`

### **Run Python Scripts**
```bash
# Find best teams
python3 team_optimizer.py

# Generate counter-teams
python3 counter_team_generator.py

# Calculate synergy
python3 synergy_calculator.py
```

---

## 📊 Data Files

### **crk-cookies.csv** (177 cookies)
Columns: `cookie_name`, `cookie_rarity`, `cookie_role`, `cookie_position`, `cookie_element`, `skill_description`, `toppings`

**Special Note:** Ascended cookies are separate entries with "(Ascended)" suffix:
- `Pure Vanilla Cookie` (Ancient)
- `Pure Vanilla Cookie (Ascended)` (Ancient (Ascended))

### **cookie_abilities.csv** (177 abilities)
Columns: `cookie_name`, `skill_name`, `skill_type`, `crowd_control`, `grants_immunity`, `provides_healing`, `provides_shield`, `anti_heal`, `anti_tank`, `dispel`, `target_type`, `key_mechanic`

### **crk_treasures.csv** (21 treasures)
Columns: `treasure_name`, `rarity`, `activation_type`, `tier_ranking`, `effect_category`, stat bonuses, special abilities

---

## 🔧 Recent Fixes

### **Ascended Cookie Fix** ([docs/ASCENDED_COOKIE_FIX.md](docs/ASCENDED_COOKIE_FIX.md))
- **Problem:** Duplicate cookies caused by CSV merge
- **Solution:** Updated `cookie_abilities.csv` to use correct Ascended names
- **Result:** All 177 cookies load correctly, filtering works properly

### **Path Resolution Fix**
- **Problem:** Web server couldn't find `cookie_abilities.csv` and `crk_treasures.csv`
- **Solution:** Updated `TeamOptimizer` to resolve paths relative to main CSV directory
- **Result:** Server works from any directory

---

## 🎮 Web UI Features

### **Team Optimizer Tab**
1. Select optimization method (Genetic recommended)
2. Choose required cookies (up to 5)
3. Add optional cookie stats for personalized scoring
4. Exclude Ascended cookies checkbox
5. View top teams with scores and synergy breakdowns

### **Counter-Team Generator Tab**
1. Select 5 enemy cookies
2. View enemy analysis (roles, positions, abilities)
3. See identified weaknesses
4. Get recommended counter-strategies
5. View 3-5 counter-teams with treasure recommendations

---

## 📈 Scoring System

### **Team Score** (Max ~135 points)
- Role Diversity: 0-30
- Position Coverage: 0-25
- Power Score: 0-35
- Bonus Modifiers: 0-10
- Treasure Bonus: 0-15
- Synergy Bonus: 0-20

### **Counter Score** (Max 100 points)
- Recommended Cookies: 0-40
- Essential Counter Elements: 0-30
- Team Balance: 0-15
- Rarity Match: 0-15

### **Synergy Score** (Max 110 points)
- Role Synergy: 0-30
- Position Synergy: 0-20
- Element Synergy: 0-25
- Type Synergy: 0-15
- Coverage Synergy: 0-10
- Ability Synergy: 0-10

---

## 🧪 Tests

Run tests to verify functionality:
```bash
# Test treasure scoring
python3 tests/test_treasure_scoring.py

# Test counter-team treasures
python3 tests/test_counter_treasures.py

# Test API treasures endpoint
python3 tests/test_api_treasures.py
```

---

## 🛠️ Utility Scripts

### **scripts/fix_ascended_cookies.py**
Renames Ascended cookies in `crk-cookies.csv` to prevent duplicates.

### **scripts/fix_abilities_ascended.py**
Updates `cookie_abilities.csv` to use correct Ascended cookie names for Awakened skills.

**Note:** These scripts have already been run. Only re-run if you reset the CSV files.

---

## 📚 Documentation

- **README.md** - Main project documentation
- **docs/TREASURE_QUICKSTART.md** - Quick guide to treasure system
- **docs/TREASURE_INTEGRATION_SUMMARY.md** - Full treasure implementation details
- **docs/ASCENDED_COOKIE_FIX.md** - Ascended cookie bug fix explanation

---

## 🎯 Future Enhancements

### **Planned Features:**
1. Treasure selection UI (manual treasure picker)
2. Treasure loadout saving/loading
3. Arena meta analysis
4. Team comparison tool
5. Export teams to image/PDF

### **Potential Additions:**
- Guild Battle team optimizer
- Cookie recommendation quiz
- Team cost calculator
- Topping optimizer

---

## 🐛 Known Issues

None currently! All major bugs fixed.

**Previous Issues (Resolved):**
- ✅ Duplicate Ascended cookies (fixed with naming scheme)
- ✅ CSV path resolution (fixed with base_dir logic)
- ✅ Missing abilities for Ascended cookies (fixed with abilities CSV update)

---

## 📞 Support

For issues or questions:
1. Check documentation in `docs/` folder
2. Review test scripts in `tests/` folder
3. Examine fix scripts in `scripts/` folder
4. File an issue on GitHub (if applicable)

---

*Last Updated: December 30, 2024*
*Version: 2.0 (Treasure System + Ascended Fix)*
