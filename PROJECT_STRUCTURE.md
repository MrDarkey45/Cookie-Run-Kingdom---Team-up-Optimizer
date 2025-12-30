# Project Structure

## 📁 Complete File Organization

```
Cookie-Run-Kingdom-Team-Optimizer/
│
├── README.md                           # Main project documentation
├── PROJECT_STRUCTURE.md               # This file
├── run_web_ui.sh                      # Quick launcher (run from root)
│
├── 📊 Core Files
│   ├── crk-cookies.csv                # Cookie database (177 cookies)
│   ├── cookie_analysis.py             # Data analysis script
│   ├── team_optimizer.py              # Main optimization engine
│   └── cookie_analysis.png            # Generated visualization
│
├── 📚 docs/                           # Documentation
│   ├── OPTIMIZATION_GUIDE.md          # Algorithm comparison & guide
│   ├── WEB_UI_GUIDE.md                # Web UI user manual
│   └── WEB_UI_FEATURES.md             # Web UI features documentation
│
├── 💡 examples/                       # Example scripts
│   ├── example_advanced_mode.py       # Advanced scoring examples
│   └── example_optimization_methods.py # Algorithm comparisons
│
├── 🌐 web_ui/                         # Web Application
│   ├── app.py                         # Flask backend server
│   ├── start_web_ui.sh                # Web UI launcher
│   ├── templates/
│   │   └── index.html                 # Main HTML page
│   └── static/
│       ├── styles.css                 # CSS styling
│       └── app.js                     # JavaScript logic
│
├── 📤 output/                         # Generated files
│   └── *.json                         # Exported team compositions
│
└── __pycache__/                       # Python bytecode cache

```

---

## 🎯 File Descriptions

### **Root Directory**

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation and quick start guide |
| `PROJECT_STRUCTURE.md` | This file - detailed project structure |
| `run_web_ui.sh` | Quick launcher script (runs `web_ui/start_web_ui.sh`) |
| `crk-cookies.csv` | Cookie database with 177 cookies and their attributes |
| `cookie_analysis.py` | Data analysis and visualization script |
| `team_optimizer.py` | Core optimization engine with 4 algorithms |
| `cookie_analysis.png` | Generated pie/bar charts from analysis |

---

### **docs/** - Documentation

| File | Purpose |
|------|---------|
| `OPTIMIZATION_GUIDE.md` | Complete guide to all 4 algorithms, performance comparison, usage examples |
| `WEB_UI_GUIDE.md` | User manual for the web interface |
| `WEB_UI_FEATURES.md` | Detailed web UI feature documentation |

---

### **examples/** - Example Scripts

| File | Purpose |
|------|---------|
| `example_advanced_mode.py` | Demonstrates hybrid scoring with cookie levels/skills |
| `example_optimization_methods.py` | Compares all optimization methods with benchmarks |

**Run these to see the optimizer in action:**
```bash
cd examples
python3 example_advanced_mode.py
python3 example_optimization_methods.py
```

---

### **web_ui/** - Web Application

| File | Purpose |
|------|---------|
| `app.py` | Flask backend server with REST API |
| `start_web_ui.sh` | Launcher script (checks Flask, starts server) |
| `templates/index.html` | Main web page structure |
| `static/styles.css` | CSS styling with glassmorphism design |
| `static/app.js` | Frontend JavaScript (search, optimize, render) |

**Launch the web UI:**
```bash
# From root
./run_web_ui.sh

# Or from web_ui directory
cd web_ui
./start_web_ui.sh
```

---

### **output/** - Generated Files

Export destination for optimized team data:
- `optimized_teams.json` - Team compositions with scores
- `top_teams.json` - Top-ranked teams
- `*.csv` - CSV exports

**Create exports:**
```bash
python3 team_optimizer.py --export output/my_teams.json
```

---

## 🚀 Quick Navigation

### **Want to...**

**Analyze cookie data?**
```bash
python3 cookie_analysis.py
```

**Optimize teams (CLI)?**
```bash
python3 team_optimizer.py --method genetic --top 5
```

**Use the web interface?**
```bash
./run_web_ui.sh
```

**See examples?**
```bash
cd examples && python3 example_advanced_mode.py
```

**Read documentation?**
```bash
# Algorithm guide
cat docs/OPTIMIZATION_GUIDE.md

# Web UI guide
cat docs/WEB_UI_GUIDE.md
```

---

## 📦 Dependencies by Component

### **Core (Required)**
- `pandas` - Data manipulation
- `matplotlib` - Plotting
- `seaborn` - Statistical visualization

### **Web UI (Optional)**
- `flask` - Web server

### **Install All:**
```bash
pip3 install pandas matplotlib seaborn flask --break-system-packages
```

---

## 🎨 File Relationships

```
crk-cookies.csv
    ↓ (loaded by)
cookie_analysis.py → cookie_analysis.png
    ↓ (also loaded by)
team_optimizer.py
    ↓ (imported by)
web_ui/app.py ← templates/index.html
    ↓              ↑
examples/*.py   static/*.css, *.js
```

---

## 🔧 Modification Guide

### **Add New Cookies**
1. Edit `crk-cookies.csv`
2. Add row: `name,rarity,role,position,N/A,,`

### **Change Scoring Formula**
1. Edit `team_optimizer.py`
2. Modify `Team.calculate_score()`

### **Customize Web UI**
1. Colors: `web_ui/static/styles.css` (`:root` variables)
2. Layout: `web_ui/templates/index.html`
3. Logic: `web_ui/static/app.js`

### **Add New Algorithm**
1. Edit `team_optimizer.py`
2. Add method to `TeamOptimizer` class
3. Update `find_best_teams()` method choices

---

## 📊 Data Flow

### **CLI Workflow**
```
User command
    ↓
team_optimizer.py
    ↓ (loads)
crk-cookies.csv
    ↓ (creates)
Cookie objects
    ↓ (generates)
Team combinations
    ↓ (scores)
Ranked teams
    ↓ (displays/exports)
Console / JSON file
```

### **Web UI Workflow**
```
User browser
    ↓ (HTTP request)
web_ui/app.py
    ↓ (calls)
team_optimizer.py
    ↓ (loads)
crk-cookies.csv
    ↓ (processes)
Optimized teams
    ↓ (JSON response)
static/app.js
    ↓ (renders)
Beautiful HTML display
```

---

## 🎯 Entry Points

| What | Command | Location |
|------|---------|----------|
| Data Analysis | `python3 cookie_analysis.py` | Root |
| CLI Optimizer | `python3 team_optimizer.py` | Root |
| Web UI | `./run_web_ui.sh` | Root |
| Web UI (alt) | `./start_web_ui.sh` | web_ui/ |
| Examples | `python3 example_*.py` | examples/ |

---

## 💾 Cache Files

- `__pycache__/` - Python bytecode cache (auto-generated, safe to delete)
- `.DS_Store` - macOS file metadata (auto-generated, safe to delete)
- `.claude/` - Claude AI planning cache (can be deleted)

---

## 🗂️ Clean Project Structure

To get a clean view:
```bash
# Remove cache files
rm -rf __pycache__ .DS_Store

# Remove output files
rm -rf output/*.json

# Reset to original state
git clean -fdx  # If using git
```

---

## 📝 Notes

- All paths are relative to project root
- Web UI files reference parent directory for imports
- Output directory auto-created if missing
- Examples are self-contained and can run independently

---

## 🎉 Summary

The project is organized into logical sections:
- **Root** - Core functionality (analysis, optimization)
- **docs/** - All documentation
- **examples/** - Runnable demos
- **web_ui/** - Complete web application
- **output/** - Generated/exported files

**Clean, modular, and easy to navigate!**
