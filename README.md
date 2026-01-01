# Cookie Run: Kingdom - Team Optimizer

A comprehensive Python application for optimizing Cookie Run: Kingdom team compositions using advanced algorithms and machine learning techniques.

---

## 📁 Project Structure

> **📌 For detailed project organization, see [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)**

```
/Models/
├── README.md                    # This file
├── PROJECT_OVERVIEW.md          # Detailed project structure & guide
├── crk-cookies.csv             # Cookie database (177 cookies)
├── cookie_abilities.csv        # Cookie abilities & skills data
├── crk_treasures.csv           # Treasure database (21 treasures)
├── cookie_synergy_data.json    # Element & synergy group data (67+ cookies)
├── cookie_analysis.py          # Data analysis and visualization
├── team_optimizer.py           # Core optimization engine (with synergy system)
├── counter_team_generator.py   # Counter-team generation
├── guild_battle_optimizer.py   # Guild Battle boss-specific teams
├── synergy_calculator.py       # Team synergy calculations
│
├── docs/                        # Documentation
│   ├── OPTIMIZATION_GUIDE.md   # Algorithm comparison guide
│   ├── WEB_UI_GUIDE.md         # Web interface user guide
│   ├── WEB_UI_FEATURES.md      # Web UI feature documentation
│   ├── TREASURE_QUICKSTART.md  # Treasure system quick guide
│   ├── TREASURE_INTEGRATION_SUMMARY.md  # Treasure implementation
│   └── ASCENDED_COOKIE_FIX.md  # Ascended cookie bug fix details
│
├── scripts/                     # Utility scripts
│   ├── fix_ascended_cookies.py      # Fixes Ascended cookie duplicates
│   └── fix_abilities_ascended.py    # Fixes abilities CSV naming
│
├── tests/                       # Test scripts
│   ├── test_treasure_scoring.py
│   ├── test_counter_treasures.py
│   └── test_api_treasures.py
│
├── examples/                    # Example scripts
│   ├── example_advanced_mode.py         # Advanced scoring demo
│   └── example_optimization_methods.py  # Algorithm comparison
│
├── web_ui/                      # Web application
│   ├── app.py                  # Flask backend server
│   ├── start_web_ui.sh         # Launch script
│   ├── templates/
│   │   └── index.html          # Main web page
│   └── static/
│       ├── styles.css          # CSS styling
│       └── app.js              # JavaScript logic
│
├── output/                      # Generated files
│   └── *.json                  # Exported team data
│
└── __pycache__/                # Python cache
```

---

## 🚀 Quick Start

### **🎯 First Time User? Start Here!**

**Step 1: Install Python Dependencies**
```bash
pip3 install pandas matplotlib seaborn flask
```

**Step 2: Launch the Web Interface**
```bash
cd web_ui
python3 app.py
```

**Step 3: Open Your Browser**
Go to: **http://localhost:5000**

**Step 4: Try These Quick Examples:**

1. **Find the Best Team Overall**
   - Click the "Team Optimizer" tab
   - Set Method to: **Genetic Algorithm** (best results)
   - Click **"Generate Teams"**
   - See top teams ranked by score!

2. **Build Around Your Favorite Cookie**
   - Search for your cookie (e.g., "Shadow Milk")
   - Click it to add as required
   - Click **"Generate Teams"**
   - Get teams built around your cookie!

3. **Maximize Team Synergy** ⭐ NEW!
   - Click the "Team Optimizer" tab
   - Set Method to: **Synergy-Optimized**
   - Click **"Generate Teams"**
   - Watch animated synergy bars show element matching, group bonuses, and special combos!

4. **Create F2P-Friendly Teams** ⭐ NEW!
   - Set "Max Rarity" to: **Epic and Below**
   - Click **"Generate Teams"**
   - Get powerful teams without Legendary/Ancient/Beast cookies!

5. **Counter an Enemy Team**
   - Click the "Counter-Team Generator" tab
   - Select 5 enemy cookies
   - Click **"Generate Counter-Teams"**
   - See recommended counters with strategies!

6. **Guild Battle Optimization** ⭐
   - Click the "Guild Battle" tab
   - Select your boss (Red Velvet Dragon, Avatar of Destiny, Living Abyss, Machine-God)
   - Choose cookies or let the optimizer suggest S-tier picks
   - Get boss-specific team recommendations with strategies!

**That's it!** You're ready to optimize! 🎉

---

### **Option 1: Web Interface (Recommended)**

```bash
cd web_ui
./start_web_ui.sh
```

Then open: **http://localhost:5000**

### **Option 2: Command Line**

```bash
# Generate best teams
python3 team_optimizer.py --method genetic --generate 100 --top 5

# Build around specific cookie
python3 team_optimizer.py --require "Shadow Milk Cookie" --method genetic --top 5

# Multiple required cookies
python3 team_optimizer.py --require "Pure Vanilla Cookie,Dark Cacao Cookie" --top 3
```

### **Option 3: Python API**

```python
from team_optimizer import TeamOptimizer

optimizer = TeamOptimizer('crk-cookies.csv')
best_teams = optimizer.find_best_teams(n=10, method='genetic')

for team in best_teams:
    print(team)
```

---

## ✨ Features

### **🧠 5 Optimization Algorithms**

1. **Random Sampling** - Fast exploration (0.01s for 1000 teams)
2. **Greedy Algorithm** - Power-focused selection
3. **Genetic Algorithm** ⭐ - Best results (92-96/100 scores)
4. **Synergy-Optimized** ⭐ NEW! - Maximizes element matching, synergy groups, and special combos
5. **Exhaustive Search** - Guaranteed optimal (with 3+ required cookies)

### **⚡ Hybrid Scoring System**

**Basic Mode** (Rarity-only):
- Works out-of-the-box with CSV data
- Scores based on cookie rarity tiers

**Advanced Mode** (Level/Skill stats):
- Include cookie level (1-70)
- Include skill level (1-60)
- Include topping quality (0-5)
- Formula: `Power = (Rarity × 40%) + (Skill × 35%) + (Level × 15%) + (Toppings × 10%)`

### **🎯 Build-Around Feature**

Create teams featuring YOUR favorite cookies:
- Specify 1-5 required cookies
- Optimizer fills remaining slots optimally
- Perfect for "I just got X cookie - what team?" scenarios

### **📊 Team Scoring (100-point scale)**

- **Role Diversity** (0-30 points) - Variety of combat roles
- **Position Coverage** (0-25 points) - Front/Middle/Rear balance
- **Power Score** (0-35 points) - Cookie strength
- **Bonus Modifiers** (0-10 points) - Tank, healer, DPS bonuses

### **🌟 Advanced Synergy System** ⭐ NEW!

Teams are scored on **60-point advanced synergy scale**:

- **Element Synergy** (0-15 points) - 3+ cookies with same element (Light, Fire, Water, Ice, Earth, Grass, Wind, Electricity, Darkness, Steel, Poison)
- **Synergy Groups** (0-20 points) - Cookies from same affiliation (Beast, Dragon, Ancient, Kingdom factions, Citrus Squad, etc.)
- **Special Combos** (0-25 points) - Activate powerful team combos:
  - **Citrus Party** - Lemon + Orange + Lime + Grapefruit
  - **The Protector of the Golden City** - Golden Cheese + Burnt Cheese + Smoked Cheese
  - **Silver Knighthood** - Mercurial Knight + Silverbell
  - **Team Drizzle** - Choco Drizzle + Green Tea Mousse + Pudding à la Mode
  - **The Deceitful Trio** - Shadow Milk + Black Sapphire + Candy Apple

**Visual Synergy Breakdown** - All team results show color-coded progress bars displaying element, group, and combo synergy scores with animated gradients.

### **🎯 Maximum Rarity Filter** ⭐ NEW!

Restrict team generation to specific rarity tiers:

- **Epic and Below** - Only Common, Rare, Special, and Epic cookies
- **Legendary and Below** - Exclude Dragon, Ancient, and Beast cookies
- **Filter applies to:**
  - Cookie selection grids (Team Optimizer and Counter-Team tabs)
  - Team generation algorithms
  - Counter-team recommendations

Perfect for:
- F2P-friendly team compositions
- Challenge runs with rarity restrictions
- Testing non-meta cookie combinations

### **🌐 Beautiful Web Interface**

- Modern gradient design with glassmorphism
- Interactive cookie selection with element badges ⭐ NEW!
- Real-time search filtering by name, rarity, role, position
- Visual team cards with animated synergy breakdown ⭐ NEW!
- Rarity filter dropdown (Epic and Below, Legendary and Below, etc.) ⭐ NEW!
- Responsive layout
- Bookmark system for saving favorite teams ⭐
- Export teams to text files ⭐

### **📈 Data Analysis**

- Distribution visualizations (pie charts, bar graphs)
- Statistical summaries
- Collection analytics

---

## 🛠️ Installation

### **Requirements**

- Python 3.7+
- pandas
- matplotlib
- seaborn
- flask (for web UI)

### **Install Dependencies**

```bash
pip3 install pandas matplotlib seaborn flask --break-system-packages
```

Or if you prefer a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pandas matplotlib seaborn flask
```

---

## 📚 Usage Examples

### **1. Data Analysis**

```bash
python3 cookie_analysis.py
```

Generates `cookie_analysis.png` with visualizations.

### **2. Team Optimization (CLI)**

```bash
# Best overall team
python3 team_optimizer.py --method genetic --generate 100 --top 1

# Build around Shadow Milk Cookie
python3 team_optimizer.py --require "Shadow Milk Cookie" --method genetic --top 5

# Exhaustive search with 3 cookies
python3 team_optimizer.py --method exhaustive --require "Cookie1,Cookie2,Cookie3"

# Export to JSON
python3 team_optimizer.py --method genetic --top 10 --export output/teams.json
```

### **3. Advanced Mode Examples**

```bash
cd examples
python3 example_advanced_mode.py
python3 example_optimization_methods.py
```

### **4. Web Interface**

```bash
cd web_ui
./start_web_ui.sh
```

Features:
- Search and select required cookies
- Choose optimization method
- Adjust parameters
- View beautiful team visualizations

---

## 📖 Documentation

- **[OPTIMIZATION_GUIDE.md](docs/OPTIMIZATION_GUIDE.md)** - Complete algorithm comparison
- **[WEB_UI_GUIDE.md](docs/WEB_UI_GUIDE.md)** - Web interface user guide
- **[WEB_UI_FEATURES.md](docs/WEB_UI_FEATURES.md)** - UI feature documentation

---

## 🎯 Use Cases

### **Scenario 1: New Player**
"I just started - what's a good team?"
```bash
python3 team_optimizer.py --method greedy --top 5
```

### **Scenario 2: Got a Beast Cookie**
"I pulled Shadow Milk Cookie - build me a team!"
```bash
python3 team_optimizer.py --require "Shadow Milk Cookie" --method genetic --top 5
```

### **Scenario 3: Have Specific Cookies Maxed**
"I have Pure Vanilla, Dark Cacao, and Hollyberry maxed - who should I add?"
```bash
python3 team_optimizer.py --require "Pure Vanilla Cookie,Dark Cacao Cookie,Hollyberry Cookie" --method exhaustive
```

### **Scenario 4: Find THE BEST Team**
"What's the absolute best team composition?"
```bash
python3 team_optimizer.py --method genetic --generate 200 --top 1
```

---

## 🧪 Testing

Run the examples to verify everything works:

```bash
# Test basic optimization
python3 team_optimizer.py --method random --generate 100 --top 3

# Test genetic algorithm
python3 team_optimizer.py --method genetic --generate 50 --top 3

# Test build-around feature
python3 team_optimizer.py --require "Mystic Flour Cookie" --top 3

# Test web UI (should start server)
cd web_ui && python3 app.py
```

---

## 🔬 Algorithm Performance

| Method | Teams/Time | Best Score | Synergy | Speed | Use Case |
|--------|------------|-----------|---------|-------|----------|
| Random | 1000 teams | 85-89/100 | Variable | ⚡⚡⚡ | Exploration |
| Greedy | 1000 teams | 88-91/100 | Low | ⚡⚡⚡ | Power-focus |
| Genetic | 100 gen | **92-96/100** | Medium | ⚡⚡ | **Best overall** |
| Synergy | 50-100 gen | 90-95/100 | **High** | ⚡⚡ | **Special combos** ⭐ NEW! |
| Exhaustive | All combos | 96-99/100 | Varies | Varies | 3+ required |

---

## 💡 Pro Tips

1. **Use Genetic Algorithm** for consistent 92-96/100 scores
2. **Use Synergy-Optimized** to activate special combos (Citrus Party, Team Drizzle, etc.) ⭐ NEW!
3. **Select 1-3 cookies** for build-around scenarios
4. **Exhaustive search** only with 3+ required cookies
5. **Web UI** provides best user experience with visual synergy breakdown ⭐ NEW!
6. **Export teams** to JSON for later comparison
7. **Try "Epic and Below" filter** for F2P-friendly team compositions ⭐ NEW!
8. **Watch for element badges** - 3+ same element = 15 synergy points ⭐ NEW!
9. **Guild Battle tab** has boss-specific S-tier recommendations ⭐

---

## 🎨 Data Sources

- **crk-cookies.csv** - 177 cookies with attributes:
  - Name, Rarity, Role, Position
  - Empty columns for future data: skill_description, toppings, cookie_element

- **cookie_synergy_data.json** ⭐ NEW! - 67+ cookies with:
  - Element types (Light, Fire, Water, Ice, Earth, Grass, Wind, Electricity, Darkness, Steel, Poison)
  - Synergy groups (Beast, Dragon, Ancient, Kingdom affiliations, special squads)
  - Special combo participants (5 defined combos)

---

## 📝 Notes

- All optimization happens server-side (Flask) or locally (CLI)
- Genetic algorithm is non-deterministic (results may vary)
- Exhaustive search with <3 required cookies = 138M+ combinations!
- Web UI requires Flask installed

---

## 🤝 Contributing

To add new cookies:
1. Edit `crk-cookies.csv`
2. Add row with: `name,rarity,role,position,element,skill,toppings`
3. Restart optimizer/web server

To modify scoring:
1. Edit `team_optimizer.py`
2. Adjust weights in `Team.calculate_score()`

---

## 📄 License

This project is for educational and personal use.

---

## 🎉 Credits

Built with:
- **Python 3** - Core language
- **pandas** - Data manipulation
- **matplotlib/seaborn** - Visualizations
- **Flask** - Web server
- **Genetic Algorithms** - Optimization technique
- **Cookie Run: Kingdom** - Game data

---

## 🆘 Troubleshooting

**Issue:** "ModuleNotFoundError: No module named 'flask'"
```bash
pip3 install flask --break-system-packages
```

**Issue:** "Port 5000 already in use"
- Edit `web_ui/app.py` and change port to 5001

**Issue:** "No teams generated"
- Check CSV file path
- Verify cookie data loaded correctly
- Try reducing required cookies for exhaustive search

**Issue:** "Web UI shows blank page"
- Check browser console (F12) for errors
- Verify templates/static files exist
- Restart Flask server

---

## 🚀 Get Started Now!

```bash
# Quick test
python3 team_optimizer.py --method genetic --top 3

# Launch web UI
cd web_ui && ./start_web_ui.sh
```

**Have fun creating the ultimate Cookie Run: Kingdom teams!** 🍪✨
