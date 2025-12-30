# Cookie Run: Kingdom Team Optimizer - UI V2 Guide

## 🎨 What's New in V2

The UI has been completely redesigned with a **tabbed interface and sidebar layout** for a more compact, accessible experience with **zero scrolling required**.

---

## ✨ Key Improvements

### **Before (V1)**
- ❌ Long vertical scrolling
- ❌ Cookie lists hidden in scrollable containers
- ❌ Separate sections stacked vertically
- ❌ Modal popups for stats
- ❌ Hard to see all options at once

### **After (V2)**
- ✅ Everything visible on one screen
- ✅ Grid view shows many cookies at once
- ✅ Tabs separate features clearly
- ✅ Side panel for stats editing
- ✅ Settings always accessible in sidebar

---

## 🗂️ Tab Structure

### **Tab 1: Team Optimizer** ⚙️
Build optimal 5-cookie teams from your collection.

**Layout:**
```
┌────────────┬──────────────────────────────────┐
│ Settings   │ Cookie Selection (Grid)          │
│ ───────    │                                  │
│ Method: ▼  │ 🔍 Search: [________]           │
│ Gens: [__] │ [All ▼] [All ▼] [All ▼]         │
│ Teams: [_] │                                  │
│ ☐ Exclude  │ [🍪][🍪][🍪][🍪][🍪][🍪][🍪]  │
│            │ [🍪][🍪][🍪][🍪][🍪][🍪][🍪]  │
│ Required:  │ [🍪][🍪][🍪][🍪][🍪][🍪][🍪]  │
│ [Cookie 1] │                                  │
│ [Cookie 2] │ ─────────────────────────────    │
│            │ Results (Auto-expand first)      │
│ [Optimize] │ ▼ Team #1 - Score: 95.3         │
│            │   [5 cookies + stats]            │
└────────────┴──────────────────────────────────┘
```

**Features:**
- **Grid View**: See 30+ cookies at once (vs 10 in list view)
- **Live Filtering**: Search + 3 dropdown filters
- **Visual Selection**: Selected cookies highlighted with color
- **Sidebar Settings**: Always visible, no scrolling needed
- **Accordion Results**: Teams collapsed, expand to view details

### **Tab 2: Counter-Team** ⚔️
Generate teams to counter enemy compositions.

**Same Layout as Team Optimizer:**
- Left sidebar: Counter method settings
- Main area: Enemy cookie selection grid
- Results: Counter-teams with strategy explanations + treasure recommendations

**Unique Features:**
- Enemy team composition analysis
- Weakness identification
- Treasure recommendations per counter-team

### **Tab 3: Cookie Manager** 📋
View all cookies and manage stats.

**Layout:**
```
┌────────────┬──────────────────────────────────┬──────────┐
│ Stats Info │ Cookie Collection (Grid)         │ Stats    │
│ ───────    │                                  │ Panel    │
│ [45] with  │ 🔍 Search: [________]           │ (Slide-  │
│ stats      │ [All ▼] [Stats ▼]               │  in)     │
│            │                                  │          │
│            │ [🍪⚡][🍪][🍪⚡][🍪][🍪]        │ Cookie:  │
│            │ [🍪⚡][🍪][🍪][🍪⚡][🍪]        │ Shadow   │
│            │ [🍪][🍪⚡][🍪][🍪][🍪⚡]        │ Milk     │
│            │                                  │          │
│ [Clear All]│ (⚡ = has stats)                 │ Lv: [90] │
│            │                                  │ Skill:[] │
│            │                                  │ Stars:[] │
└────────────┴──────────────────────────────────┴──────────┘
```

**Features:**
- **Visual Stats Indicator**: ⚡ badge on cookies with stats
- **Filter by Stats**: Show only cookies with/without stats
- **Side Panel Editor**: Click any cookie to edit stats (no modal!)
- **Quick Stats View**: See how many cookies have stats configured

---

## 🎯 UI Components

### **Cookie Grid Card**
```
┌─────────┐
│  🍪     │ ← Cookie icon (emoji for now)
│ Shadow  │ ← Name (truncated if long)
│  Milk   │
│ Beast • │ ← Role • Position
│  Magic  │
├─────────┤
│▓▓▓▓▓▓▓▓▓│ ← Rarity color bar
└─────────┘
```

**States:**
- Normal: Semi-transparent white background
- Hover: Raised with accent glow
- Selected: Accent border + background
- Has Stats: ⚡ badge in top-right corner

### **Sidebar Settings**
- **280px wide** on desktop
- **Collapsible** on tablet (overlays content)
- **Full-width** on mobile
- Settings grouped logically
- Dividers separate sections

### **Accordion Results**
```
▼ Team #1 - Score: 95.3        [Expanded]
  ┌─────────────────────────────────────┐
  │ [5 cookie cards displayed]          │
  │ Stats: Roles, Positions, Tank, etc. │
  └─────────────────────────────────────┘

▶ Team #2 - Score: 92.1        [Collapsed]
▶ Team #3 - Score: 89.4        [Collapsed]
```

**Behavior:**
- First team auto-expands
- Click header to toggle expand/collapse
- Arrow rotates to indicate state

### **Stats Side Panel**
```
┌─────────────────────────┐
│ Cookie Stats         [×]│ ← Close button
├─────────────────────────┤
│ Shadow Milk Cookie      │
│ Rarity: Beast           │
│ Role: Magic             │
│                         │
│ Cookie Level: [90]      │
│ Skill Level:  [90]      │
│ Star Level:   [5]       │
│                         │
│ Toppings:               │
│ [Swift Chocolate] [12]  │
│ [+ Add Topping]         │
│                         │
│ ☐ Add to Required       │
│                         │
│ [Save Stats] [Delete]   │
└─────────────────────────┘
```

**Behavior:**
- Slides in from right when cookie clicked
- 400px wide
- Overlay on mobile (full width)
- Smooth animation

---

## 🎨 Visual Design

### **Color Palette**
- **Primary Background**: `#1a1a2e` (dark navy)
- **Secondary Background**: `#16213e` (darker navy)
- **Accent Color**: `#e94560` (pink/red)
- **Accent Hover**: `#ff6b81` (lighter pink)
- **Text Light**: `#f1f1f1` (off-white)
- **Text Muted**: `#a0a0a0` (gray)

### **Gradients**
- **Header Title**: Pink to orange gradient
- **Primary Button**: Pink to lighter pink
- **Tab Active**: Transparent with accent border

### **Effects**
- **Backdrop Blur**: Frosted glass effect on panels
- **Card Hover**: Lift with glow shadow
- **Smooth Transitions**: 0.3s for all state changes
- **Border Glow**: Accent color on focus/selection

---

## 📱 Responsive Design

### **Desktop (1200px+)**
- Full sidebar (280px)
- Grid: 6-8 cookies per row
- All tabs visible with labels

### **Tablet (768-1199px)**
- Collapsible sidebar (overlays content)
- Grid: 4-6 cookies per row
- Tab labels visible

### **Mobile (<768px)**
- Vertical layout (sidebar stacks on top)
- Grid: 3-4 cookies per row
- Tab icons only (no labels)
- Stats panel full-width

---

## ⌨️ Interactions

### **Cookie Selection**
1. Click cookie card → Toggles selection
2. Selected cards get accent border + background
3. Max 5 cookies (alert if exceeded)
4. Chips appear in sidebar with × button

### **Filtering**
1. Type in search → Instant filter
2. Change dropdown → Instant filter
3. Filters combine (AND logic)
4. Exclude Ascended affects all tabs

### **Team Results**
1. Click accordion header → Expand/collapse
2. First team auto-expanded
3. Smooth animation
4. Can expand multiple teams simultaneously

### **Stats Management**
1. Click cookie (Manager tab) → Panel slides in
2. Edit values → Realtime validation
3. Add toppings → Max 5 slots
4. Save → Panel closes, grid updates
5. Delete → Confirmation dialog

---

## 🚀 Performance Optimizations

### **Grid Rendering**
- Only visible cookies rendered
- Filtered results update instantly
- No re-render of unchanged elements

### **Lazy Loading** (Future)
- First 50 cookies loaded immediately
- Scroll to load more (virtualized)
- Improves initial page load

### **State Management**
- Global state for cookies/selections
- Efficient re-renders (only changed elements)
- Local storage for preferences (future)

---

## 🔄 Migration from V1

The old UI is still accessible at `/v1` for comparison:
- Main route (`/`) → New V2 UI
- `/v1` route → Old V1 UI

**What's Preserved:**
- ✅ All API endpoints unchanged
- ✅ Cookie stats format compatible
- ✅ Optimization methods identical
- ✅ Results format unchanged

**What's Improved:**
- ✅ No scrolling required
- ✅ Grid view vs list view
- ✅ Sidebar vs inline settings
- ✅ Side panel vs modal
- ✅ Tabs vs stacked sections

---

## 🐛 Known Limitations (V2.0)

### **Not Yet Implemented:**
1. Cookie portraits (using emojis for now)
2. Drag & drop cookie reordering
3. Keyboard shortcuts
4. Export teams to image
5. Light mode theme

### **Planned for V2.1:**
- Real cookie images (if assets available)
- Saved team loadouts
- Quick actions menu (right-click)
- Comparison view (2 teams side-by-side)
- Synergy visualization

---

## 💡 Tips & Tricks

### **Quick Cookie Selection**
1. Use filters to narrow down options
2. Search by name for instant find
3. Selected cookies show in sidebar (remove with ×)

### **Efficient Team Building**
1. Add required cookies first
2. Check "Exclude Ascended" if you don't have them
3. Use Genetic method with 100+ generations for best results

### **Stats Management**
1. Click any cookie in Manager tab to edit
2. Filter by "With Stats" to see configured cookies
3. Use "Add to Required" checkbox for quick team building

### **Counter-Team Strategy**
1. Select meta enemy team (common in Arena)
2. Review weaknesses identified
3. Check treasure recommendations for each counter-team

---

## 🎯 User Workflows

### **Workflow 1: Build Best Team**
1. Go to **Team Optimizer** tab
2. (Optional) Select required cookies from grid
3. Set **Method: Genetic**, **Generations: 100**
4. Click **Optimize**
5. Review top teams (first auto-expanded)
6. Click other teams to compare

### **Workflow 2: Counter Enemy Team**
1. Go to **Counter-Team** tab
2. Select 5 enemy cookies from grid
3. Set **Method: Genetic** for best results
4. Click **Generate**
5. Review counter strategies + treasure recommendations
6. Use suggested team in battle

### **Workflow 3: Manage Cookie Stats**
1. Go to **Cookie Manager** tab
2. Click any cookie → Stats panel opens
3. Enter Level, Skill, Stars, Toppings
4. (Optional) Check "Add to Required"
5. Click **Save Stats**
6. Cookie now shows ⚡ badge

---

## 📊 Comparison: V1 vs V2

| Feature | V1 | V2 |
|---------|----|----|
| **Layout** | Vertical scroll | Tabbed + Sidebar |
| **Cookie Display** | List (10 visible) | Grid (30+ visible) |
| **Settings** | Inline panels | Persistent sidebar |
| **Results** | Stacked cards | Accordion (collapsible) |
| **Stats Editor** | Modal popup | Side panel (slide-in) |
| **Tabs** | None (all stacked) | 3 tabs (separate features) |
| **Scrolling** | Required | Minimal/none |
| **Mobile UX** | Difficult | Optimized |
| **Speed** | Good | Better (less DOM) |

---

## 🔧 Technical Details

### **Files Structure**
```
web_ui/
├── app.py (updated routes)
├── templates/
│   ├── index.html (V1 - preserved)
│   └── index_v2.html (V2 - new)
└── static/
    ├── styles.css (V1)
    ├── styles_v2.css (V2)
    ├── app.js (V1)
    └── app_v2.js (V2)
```

### **CSS Architecture**
- CSS Variables for theming
- BEM-like naming conventions
- Mobile-first responsive design
- Smooth transitions on all interactions
- Backdrop filters for glassmorphism

### **JavaScript Architecture**
- Modular functions by feature
- Global state management
- Event delegation for performance
- Async/await for API calls
- Error handling with user feedback

---

## 🎓 For Developers

### **Adding New Features**
1. Add HTML to appropriate tab in `index_v2.html`
2. Style in `styles_v2.css` (follow existing patterns)
3. Add JS functions in `app_v2.js`
4. Update this guide with new feature docs

### **Customization**
- **Colors**: Edit CSS variables in `:root`
- **Sidebar Width**: Change `--sidebar-width` variable
- **Grid Columns**: Adjust `grid-template-columns` in `.cookie-grid`
- **Animations**: Modify `--transition-speed` variable

---

*Last Updated: December 30, 2024*
*Version: 2.0*
*Author: Claude Code Assistant*
