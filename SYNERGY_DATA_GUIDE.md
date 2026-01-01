# Cookie Synergy Data Guide

## Overview

The `cookie_synergy_data.json` file contains element types, synergy groups, and special combo data for Cookie Run: Kingdom cookies. This data powers the **Advanced Synergy System** and the **Synergy-Optimized** team generation method.

---

## File Structure

```json
{
  "elements": { ... },
  "synergy_groups": { ... },
  "special_combos": { ... }
}
```

---

## 1. Elements

**Purpose**: Assign elemental types to cookies for element-matching bonuses.

**Structure**:
```json
"elements": {
  "Cookie Name": "Element Type",
  ...
}
```

**Supported Elements** (11 total):
- `Light` - Holy/healing themed cookies
- `Fire` - Burn and high damage
- `Water` - Ocean/aquatic themed
- `Ice` - Freeze and chill effects
- `Earth` - Ground/rock themed
- `Grass` - Nature/plant themed
- `Wind` - Air/speed themed
- `Electricity` - Lightning/shock themed
- `Darkness` - Shadow/dark magic
- `Steel` - Metal/defense themed
- `Poison` - Toxic effects

**Scoring**:
- 3+ cookies with same element = **15 points**
- 2 cookies with same element = **7 points**
- Mixed elements = **0 points**

**Example**:
```json
"Pure Vanilla Cookie": "Light",
"Mystic Flour Cookie": "Light",
"Eclair Cookie": "Light"
```
Team with these 3 cookies gets 15 element synergy points.

---

## 2. Synergy Groups

**Purpose**: Group cookies by affiliation, faction, or theme for group bonuses.

**Structure**:
```json
"synergy_groups": {
  "Cookie Name": ["Group1", "Group2"],
  ...
}
```

**Common Groups**:
- **Beast**: `Beast`, `Beast-Yeast` (5 Beast cookies)
- **Ancient**: `Ancient`, `Vanilla Kingdom`, `Hollyberry Kingdom`, `Dark Cacao Kingdom`, `Golden Cheese Kingdom`, `Faerie Kingdom`
- **Dragon**: `Dragon` (6 Dragon cookies)
- **Kingdoms**: `Vanilla Kingdom`, `Hollyberry Kingdom`, `Dark Cacao Kingdom`, `Golden Cheese Kingdom`, `Silver Kingdom`, `Faerie Kingdom`, `Crème Republic`
- **Special Squads**: `Citrus Squad`, `Sea Cookies`, `Winter Cookies`, `Drizzle Team`, `Wicked`

**Scoring**:
- 3+ cookies from same group = **12 points** (can stack multiple groups)
- 2 cookies from same group = **5 points** (can stack multiple groups)
- Max total = **20 points**

**Example**:
```json
"Pure Vanilla Cookie": ["Ancient", "Vanilla Kingdom"],
"Custard Cookie III": ["Vanilla Kingdom"],
"Cream Unicorn Cookie": ["Vanilla Kingdom"]
```
Team with these 3 cookies: 3 from `Vanilla Kingdom` = 12 points.

---

## 3. Special Combos

**Purpose**: Define named team combinations that activate powerful bonuses.

**Structure**:
```json
"special_combos": {
  "Cookie Name": ["Combo Name"],
  ...
}
```

**Defined Combos**:

### Citrus Party (20 points)
**Required**: Lemon Cookie
**Optional**: Orange Cookie, Lime Cookie, Grapefruit Cookie
**Activation**: Lemon + any 1+ other citrus cookie

```json
"Lemon Cookie": ["Citrus Party"],
"Orange Cookie": ["Citrus Party"],
"Lime Cookie": ["Citrus Party"],
"Grapefruit Cookie": ["Citrus Party"]
```

### The Protector of the Golden City (15 points)
**Required**: Golden Cheese Cookie
**Optional**: Burnt Cheese Cookie, Smoked Cheese Cookie
**Activation**: Golden Cheese + any 1+ cheese cookie

```json
"Golden Cheese Cookie": ["The Protector of the Golden City"],
"Burnt Cheese Cookie": ["The Protector of the Golden City"],
"Smoked Cheese Cookie": ["The Protector of the Golden City"]
```

### Silver Knighthood (25 points)
**Required**: Mercurial Knight Cookie AND Silverbell Cookie
**Activation**: Both must be present

```json
"Mercurial Knight Cookie": ["Silver Knighthood"],
"Silverbell Cookie": ["Silver Knighthood"]
```

### Team Drizzle (25 points)
**Required**: All three members
**Activation**: Choco Drizzle + Green Tea Mousse + Pudding à la Mode

```json
"Choco Drizzle Cookie": ["Team Drizzle"],
"Green Tea Mousse Cookie": ["Team Drizzle"],
"Pudding à la Mode Cookie": ["Team Drizzle"]
```

### The Deceitful Trio (25 points)
**Required**: All three members
**Activation**: Shadow Milk + Black Sapphire + Candy Apple

```json
"Shadow Milk Cookie": ["The Deceitful Trio"],
"Black Sapphire Cookie": ["The Deceitful Trio"],
"Candy Apple Cookie": ["The Deceitful Trio"]
```

**Scoring**:
- Only the **highest** special combo bonus applies (no stacking)
- Max = **25 points**

---

## Total Synergy Scoring

**Maximum Possible Score**: 60 points

- Element Synergy: 0-15 points
- Group Synergy: 0-20 points (can stack multiple groups)
- Special Combos: 0-25 points (highest only)

**Example Team**:
```
Team: Lemon Cookie, Orange Cookie, Lime Cookie, Grapefruit Cookie, Wizard Cookie

Element Synergy:
- 5x Electricity = 15 points

Group Synergy:
- 4x Citrus Squad = 12 points

Special Combos:
- Citrus Party activated = 20 points

Total: 47/60 synergy score
```

---

## How to Add New Cookies

### 1. Add Element
```json
"elements": {
  "New Cookie Name": "Fire"  // Choose from 11 element types
}
```

### 2. Add Synergy Groups (optional)
```json
"synergy_groups": {
  "New Cookie Name": ["Dragon", "Beast-Yeast"]  // Can have multiple groups
}
```

### 3. Add to Special Combo (optional)
```json
"special_combos": {
  "New Cookie Name": ["Citrus Party"]  // If part of existing combo
}
```

Or create a new combo by editing [team_optimizer.py:650](team_optimizer.py#L650) `special_combo_score` property.

---

## Current Coverage

- **Elements**: 67 cookies (out of 177)
- **Synergy Groups**: 50 cookies
- **Special Combos**: 15 cookies (5 combos defined)

**Note**: Cookies without synergy data will have 0 synergy scores but still function normally in team optimization.

---

## Validation

The file is validated on load by `TeamOptimizer._load_synergy_data()`:
- Checks for valid JSON format
- Verifies cookie names exist in cookie database
- Handles missing/malformed data gracefully

---

## Visual Representation in UI

When teams are displayed in the web UI, synergy scores appear as:
- **Red gradient bar**: Element synergy (0-15)
- **Teal gradient bar**: Group synergy (0-20)
- **Gold gradient bar**: Special combo (0-25)
- **Total synergy**: Sum of all three (0-60)

Element badges and synergy tags also appear on individual cookie cards.

---

## Performance Notes

- Synergy data is loaded once at startup
- No impact on team generation speed
- Synergy-Optimized method may be slightly slower than Greedy (prioritizes quality over speed)

---

## Future Expansion

To improve coverage:
1. Add elements for remaining 110 cookies (currently 67/177)
2. Define more synergy groups (kingdom affiliations, event themes)
3. Create new special combos based on game updates
4. Consider element effectiveness system (Fire > Ice, etc.)

---

## Related Files

- [team_optimizer.py:606-716](team_optimizer.py#L606) - Synergy scoring properties
- [team_optimizer.py:1370-1616](team_optimizer.py#L1370) - Synergy-optimized generation
- [web_ui/app.py:76-106](web_ui/app.py#L76) - API endpoint integration
- [web_ui/static/app_v2.js:10-53](web_ui/static/app_v2.js#L10) - UI visualization
- [README.md:175-204](README.md#L175) - Feature documentation
