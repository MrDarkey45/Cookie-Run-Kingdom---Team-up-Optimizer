# Web UI Features & Screenshots Guide

## 🎨 Visual Design

The Cookie Run: Kingdom Team Optimizer features a **modern, gradient-based design** with:

- **Glassmorphism effects** - Frosted glass cards with blur
- **Vibrant gradients** - Purple to pink background
- **Smooth animations** - Hover effects and transitions
- **Responsive layout** - Works on desktop and mobile
- **Color-coded rarities** - Each tier has unique colors

---

## 🎯 Main Features

### **1. Header Section**
```
🍪 Cookie Run: Kingdom
   Team Optimizer
   Build the ultimate team with AI-powered optimization
```

- Eye-catching gradient text
- Clear title and subtitle
- Professional appearance

---

### **2. Optimization Settings Panel**

**Three Main Controls:**

1. **Optimization Method Dropdown**
   - Random Sampling (Fast)
   - Greedy Algorithm (Power-focused)
   - Genetic Algorithm (Best) ⭐ [Default]
   - Exhaustive Search (Requires 3+ cookies)

2. **Candidates / Generations Input**
   - Number field (10-10,000)
   - Default: 100
   - Tooltip explains what it does

3. **Teams to Show Input**
   - Number field (1-50)
   - Default: 5
   - Controls result count

---

### **3. Required Cookies ("Build Around") Feature**

**Search Bar:**
- Type to filter cookies instantly
- Searches name, role, and position

**Cookie List:**
- Scrollable list of all 177 cookies
- Each entry shows:
  - Colored rarity badge (dot)
  - Cookie name (bold)
  - Metadata (role • position • power)
  - "+" button to add

**Selected Cookies Display:**
- Shows selected cookies as tags
- Each tag displays:
  - Cookie name
  - Color-coded border (by rarity)
  - "×" button to remove
- If empty: "No cookies selected" message

**Example:**
```
🔒 Required Cookies (Build Around)
[Search cookies...]

Selected:
[Shadow Milk Cookie ×] [Pure Vanilla Cookie ×]
```

---

### **4. Optimize Button**

```
🚀 Optimize Teams
```

- Full-width, gradient button
- Hover effect (lifts up)
- Click triggers optimization

---

### **5. Loading Indicator**

When processing:
```
   ⟳ (spinning animation)
   Generating optimal teams...
```

- Appears during optimization
- Disappears when complete
- Smooth fade-in/out

---

### **6. Results Section**

**Header:**
```
🏆 Optimized Teams
Generated 100 teams • Showing top 5 results
```

**Team Cards:**

Each team card contains:

#### **Card Header**
```
#1                Score: 96.0/100
```
- Rank (gradient text)
- Score (green, large)

#### **Cookie Grid** (5 cookies displayed)

Each cookie card shows:
```
┌─────────────────┐
│  [Required]     │ ← If selected
│   ⚫ (rarity)    │ ← Colored circle
│   Shadow Milk   │ ← Name
│   Beast          │ ← Rarity (colored)
│   Magic • Middle│ ← Role • Position
│   ⚡ 7.00        │ ← Power
└─────────────────┘
```

- Hover effect (scales up 5%)
- Required cookies have gold border
- Rarity determines card accent color

#### **Team Statistics** (bottom of card)

Four stat boxes:
```
┌──────────────┬──────────────┬──────────┬───────────┐
│ Role         │ Position     │ Has Tank │ Has Healer│
│ Diversity    │ Coverage     │          │           │
│   5/5        │    3/3       │    ✓     │     ✓     │
└──────────────┴──────────────┴──────────┴───────────┘
```

---

### **7. Statistics Panel** (Bottom)

```
📊 Cookie Collection Stats

┌─────────────┬───────────────┬──────────────┬─────────────────┐
│ Total       │ Average       │ Unique       │ Beast/Ancient   │
│ Cookies     │ Power         │ Roles        │ Cookies         │
│   177       │    3.42       │     12       │      15         │
└─────────────┴───────────────┴──────────────┴─────────────────┘
```

- Displays collection overview
- Updates on page load
- Glassmorphism card design

---

## 🎨 Color Palette

### **Background**
- Main gradient: Purple (#667eea) → Violet (#764ba2)

### **Rarity Colors**
- Beast: `#ff0066` (Hot Pink)
- Ancient (Ascended): `#ffd700` (Gold)
- Ancient: `#ffaa00` (Orange-Gold)
- Legendary: `#9966ff` (Purple)
- Dragon: `#ff6600` (Orange-Red)
- Super Epic: `#ff1493` (Deep Pink)
- Epic: `#9370db` (Medium Purple)
- Special: `#4169e1` (Royal Blue)
- Rare: `#32cd32` (Lime Green)
- Common: `#808080` (Gray)

### **UI Elements**
- Primary Button: Pink (#ff6b9d) → Red (#c44569)
- Accent: Gold (#feca57)
- Success: Cyan (#00d2d3)
- Text Light: White/Off-white (#ecf0f1)

---

## ⚡ Interactive Elements

### **Hover Effects**

1. **Cookie Items in List**
   - Background lightens
   - Slides right 5px
   - Smooth transition

2. **Cookie Cards in Results**
   - Scales to 105%
   - Background lightens
   - Lifts with shadow

3. **Team Cards**
   - Lifts up 5px
   - Gold border appears
   - Shadow deepens

4. **Buttons**
   - Lifts up 2px
   - Shadow expands
   - Gradient intensifies

### **Click Interactions**

1. **Adding Cookie**
   - Instant feedback
   - Updates selected list
   - Maximum 5 warning if exceeded

2. **Removing Cookie**
   - Click "×" on tag
   - Smoothly removes
   - List updates

3. **Optimize Button**
   - Shows loading spinner
   - Hides results
   - Auto-scrolls to results when done

---

## 📱 Responsive Design

### **Desktop (1400px+)**
- Full grid layouts
- 3-column settings
- 5-column cookie grids

### **Tablet (768px - 1400px)**
- 2-column layouts
- Adaptive cookie grids

### **Mobile (<768px)**
- Single column
- Stacked settings
- 2-column cookie grids
- Larger touch targets

---

## 🎯 User Flow

```
1. User opens http://127.0.0.1:5000
   ↓
2. Sees beautiful header + controls
   ↓
3. [Optional] Searches and selects required cookies
   ↓
4. Adjusts settings (method, candidates, top N)
   ↓
5. Clicks "🚀 Optimize Teams"
   ↓
6. Loading spinner appears
   ↓
7. Results display with team cards
   ↓
8. User reviews top teams, sees stats
   ↓
9. [Optional] Adjusts and re-optimizes
```

---

## 🔥 Pro Features

### **1. Real-Time Search**
- Instant filtering as you type
- No delay or lag
- Searches multiple fields

### **2. Color-Coded Everything**
- Rarity badges
- Card borders
- Text colors
- Visual hierarchy

### **3. Smart Validation**
- Maximum 5 required cookies
- Warns about exhaustive search
- Input limits enforced

### **4. Smooth Animations**
- Fade-in/out
- Scale transforms
- Slide effects
- Spinner rotation

### **5. Auto-Scroll**
- Jumps to results when ready
- Smooth behavior
- Enhanced UX

---

## 💡 Tips for Best Experience

1. **Use Genetic Algorithm** for consistent 92-96/100 scores
2. **Select 1-3 cookies** for "build-around" scenarios
3. **Try different methods** to compare results
4. **Hover over cards** to see interactive effects
5. **Use search bar** to quickly find cookies

---

## 🚀 Launch Instructions

### **Method 1: Direct Python**
```bash
python3 app.py
```

### **Method 2: Launch Script**
```bash
./start_web_ui.sh
```

### **Method 3: Background Mode**
```bash
nohup python3 app.py &
```

Then open: **http://127.0.0.1:5000**

---

## 🎉 Result

A **professional-grade web application** that makes team optimization:
- **Beautiful** - Modern gradient design
- **Interactive** - Smooth animations
- **Intuitive** - Clear workflow
- **Powerful** - 4 optimization algorithms
- **Fast** - Instant results
- **Flexible** - Build around any cookies

Perfect for showcasing Python skills and creating optimal Cookie Run: Kingdom teams! 🍪
