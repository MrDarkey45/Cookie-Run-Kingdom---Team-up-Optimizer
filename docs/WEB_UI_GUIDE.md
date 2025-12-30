# Cookie Run: Kingdom Team Optimizer - Web UI Guide

## 🌐 Overview

A beautiful, interactive web interface for optimizing Cookie Run: Kingdom team compositions using advanced algorithms.

---

## 🚀 Quick Start

### 1. Start the Web Server

```bash
python3 app.py
```

### 2. Open Your Browser

Navigate to: **http://127.0.0.1:5000**

### 3. Start Optimizing!

---

## 📖 How to Use

### **Step 1: Choose Optimization Settings**

#### **Optimization Method**
- **Random Sampling** - Fast exploration, diverse results
- **Greedy Algorithm** - Power-focused, consistent
- **Genetic Algorithm** ⭐ - Best quality (recommended)
- **Exhaustive Search** - Guaranteed optimal (requires 3+ cookies)

#### **Candidates / Generations**
- Number of teams to generate (random/greedy) or generations (genetic)
- Higher = better quality but slower
- Recommended: 100 for genetic

#### **Teams to Show**
- How many top teams to display (1-50)
- Default: 5

---

### **Step 2: Select Required Cookies (Optional)**

Use the **"Build Around"** feature to create teams featuring specific cookies:

1. **Search** for cookies by name, role, or position
2. **Click** on cookies to add them to your required list
3. The optimizer will ensure these cookies are in EVERY team

**Use Cases:**
- "I just got Shadow Milk Cookie - build me a team!"
- "Find the best team with Pure Vanilla and Dark Cacao"
- "I have these 3 Beast cookies maxed - who should I add?"

**Limits:**
- Maximum 5 required cookies
- Exhaustive search requires 3+ for practical performance

---

### **Step 3: Click "Optimize Teams"**

The system will:
1. Generate candidate teams using your chosen method
2. Score each team based on:
   - Role diversity (30 points)
   - Position coverage (25 points)
   - Cookie power (35 points)
   - Bonus modifiers (10 points)
3. Display the top teams sorted by score

---

## 🎨 Understanding the Results

### **Team Card Elements**

Each team card displays:

#### **Header**
- **Rank** - Position in top teams (#1 is best)
- **Score** - Overall team quality (out of 100)

#### **Cookie Cards**
Each cookie shows:
- **Colored badge** - Rarity indicator
- **Name** - Cookie name
- **Rarity** - Tier level (Beast, Ancient, etc.)
- **Role** - Combat role (Magic, Charge, etc.)
- **Position** - Battle position (Front/Middle/Rear)
- **Power** - Individual strength score
- **"REQUIRED" badge** - If you selected this cookie

#### **Team Statistics**
- **Role Diversity** - Number of unique roles (5/5 is best)
- **Position Coverage** - Positions covered (3/3 is best)
- **Has Tank** - ✓ if team has Defense/Charge in Front
- **Has Healer** - ✓ if team has Healing/Support cookie

---

## 💡 Pro Tips

### **For Best Results:**

1. **Use Genetic Algorithm** with 100-200 generations
   - Consistently finds 92-96/100 scoring teams
   - Only takes 0.02-0.1 seconds

2. **Build Around Your Best Cookies**
   - Select 1-3 of your strongest/favorite cookies
   - Let the optimizer find perfect teammates

3. **Exhaustive Search Strategy**
   - Only use with 3+ required cookies
   - Guarantees the ABSOLUTE best team
   - With 3 required: ~15K combinations (fast!)
   - With 4 required: ~173 combinations (instant!)

4. **Compare Multiple Methods**
   - Try genetic first (best quality)
   - Compare with greedy (power-focused)
   - Use random for diverse options

---

## 🎯 Example Workflows

### **Scenario 1: "What's the best team in the game?"**
1. Method: Genetic Algorithm
2. Generations: 100
3. Required Cookies: None
4. Teams to Show: 10

**Result:** Top 10 highest-scoring teams across all cookies

---

### **Scenario 2: "Build around Shadow Milk Cookie"**
1. Method: Genetic Algorithm
2. Generations: 100
3. Required Cookies: Shadow Milk Cookie
4. Teams to Show: 5

**Result:** 5 best teams that include Shadow Milk Cookie

---

### **Scenario 3: "I have these 3 Beast cookies - what's THE BEST team?"**
1. Method: Exhaustive Search
2. Required Cookies: Mystic Flour, Burning Spice, Shadow Milk
3. Teams to Show: 5

**Result:** Guaranteed optimal teams with those 3 cookies

---

### **Scenario 4: "Show me diverse team options"**
1. Method: Random Sampling
2. Candidates: 5000
3. Required Cookies: None
4. Teams to Show: 20

**Result:** Wide variety of high-scoring teams

---

## 🎨 Color Legend

The UI uses color coding to represent cookie rarities:

- **Pink/Red** - Beast tier
- **Gold** - Ancient (Ascended)
- **Orange** - Ancient
- **Purple** - Legendary
- **Orange-Red** - Dragon
- **Hot Pink** - Super Epic
- **Medium Purple** - Epic
- **Blue** - Special
- **Green** - Rare
- **Gray** - Common

---

## 📊 Statistics Panel

The bottom panel shows your collection statistics:

- **Total Cookies** - Available cookies in database
- **Average Power** - Mean power score
- **Unique Roles** - Number of different combat roles
- **Beast/Ancient Cookies** - Count of top-tier cookies

---

## ⚙️ Technical Details

### **Tech Stack**
- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Algorithms:** Genetic, Greedy, Random, Exhaustive
- **Styling:** Modern gradient design with glassmorphism

### **API Endpoints**
- `GET /` - Main page
- `GET /api/cookies` - List all cookies
- `POST /api/optimize` - Generate optimized teams
- `GET /api/cookie/<name>` - Cookie details
- `GET /api/stats` - Collection statistics

### **Performance**
- Random (1000 teams): ~0.01s
- Greedy (1000 teams): ~0.01s
- Genetic (100 gen): ~0.02-0.1s
- Exhaustive (3+ required): Varies

---

## 🔧 Customization

### **Modify Team Size**
Currently fixed at 5 cookies per team (game requirement).

### **Adjust Scoring Weights**
Edit `team_optimizer.py` to change:
- Role diversity weight
- Position coverage weight
- Power score weight
- Bonus modifiers

### **Add New Cookies**
Update `crk-cookies.csv` with new cookie data.

### **Change Color Scheme**
Edit `static/styles.css` - modify CSS variables in `:root`

---

## 🐛 Troubleshooting

### **"Port 5000 already in use"**
Change port in `app.py`:
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

### **"No cookies displayed"**
- Check that `crk-cookies.csv` is in the same directory
- Verify file is not corrupted
- Check browser console for errors (F12)

### **"Optimization taking too long"**
- Reduce number of candidates/generations
- Use genetic instead of exhaustive
- Add more required cookies for exhaustive search

### **"Teams look wrong"**
- Verify scoring formula in `team_optimizer.py`
- Check cookie data in CSV for accuracy
- Review team validation logic

---

## 🚀 Future Enhancements

Potential features to add:

- [ ] Save favorite teams
- [ ] Export teams to PDF/image
- [ ] Compare two teams side-by-side
- [ ] Cookie stats visualization (charts)
- [ ] Advanced filtering (by element, rarity, etc.)
- [ ] Dark/Light theme toggle
- [ ] Mobile-responsive improvements
- [ ] Animation effects
- [ ] User authentication
- [ ] Team sharing via URL

---

## 📝 Notes

- The UI auto-refreshes results after each optimization
- All processing happens server-side for accuracy
- Genetic algorithm results may vary slightly between runs
- Exhaustive search with 0-2 required cookies is NOT recommended

---

## 🎉 Enjoy!

Create the ultimate Cookie Run: Kingdom teams with AI-powered optimization! 🍪

**Questions?** Check the main `OPTIMIZATION_GUIDE.md` for algorithm details.
