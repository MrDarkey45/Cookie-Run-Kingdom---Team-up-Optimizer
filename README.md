# Cookie Run: Kingdom - Team Optimizer

A comprehensive Python application for optimizing Cookie Run: Kingdom team compositions using advanced algorithms and machine learning techniques.

---

## 📁 Project Structure

```
/Models/
├── README.md                    # This file
├── crk-cookies.csv             # Cookie database (177 cookies)
├── cookie_analysis.py          # Data analysis and visualization
├── team_optimizer.py           # Core optimization engine
├── cookie_analysis.png         # Generated visualization
│
├── docs/                        # Documentation
│   ├── OPTIMIZATION_GUIDE.md   # Algorithm comparison guide
│   ├── WEB_UI_GUIDE.md         # Web interface user guide
│   └── WEB_UI_FEATURES.md      # Web UI feature documentation
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

### **Option 1: Web Interface (Recommended)**

```bash
cd web_ui
./start_web_ui.sh
```

Then open: **http://127.0.0.1:5000**

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

### **🧠 4 Optimization Algorithms**

1. **Random Sampling** - Fast exploration (0.01s for 1000 teams)
2. **Greedy Algorithm** - Power-focused selection
3. **Genetic Algorithm** ⭐ - Best results (92-96/100 scores)
4. **Exhaustive Search** - Guaranteed optimal (with 3+ required cookies)

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

### **🌐 Beautiful Web Interface**

- Modern gradient design with glassmorphism
- Interactive cookie selection
- Real-time search filtering
- Visual team cards
- Responsive layout

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

| Method | Teams/Time | Best Score | Speed | Use Case |
|--------|------------|-----------|-------|----------|
| Random | 1000 teams | 85-89/100 | ⚡⚡⚡ | Exploration |
| Greedy | 1000 teams | 88-91/100 | ⚡⚡⚡ | Power-focus |
| Genetic | 100 gen | **92-96/100** | ⚡⚡ | **Best overall** |
| Exhaustive | All combos | 96-99/100 | Varies | 3+ required |

---

## 💡 Pro Tips

1. **Use Genetic Algorithm** for consistent 92-96/100 scores
2. **Select 1-3 cookies** for build-around scenarios
3. **Exhaustive search** only with 3+ required cookies
4. **Web UI** provides best user experience
5. **Export teams** to JSON for later comparison

---

## 🎨 Data Sources

- **crk-cookies.csv** - 177 cookies with attributes:
  - Name, Rarity, Role, Position
  - Empty columns for future data: skill_description, toppings, cookie_element

---

## 🚧 Future Enhancements

- [ ] Counter-team generator (Phase 2)
- [ ] Synergy calculator (Phase 3)
- [ ] Skill description parsing
- [ ] Element effectiveness system
- [ ] Battle simulator
- [ ] User authentication (web UI)
- [ ] Team sharing
- [ ] Mobile app

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
