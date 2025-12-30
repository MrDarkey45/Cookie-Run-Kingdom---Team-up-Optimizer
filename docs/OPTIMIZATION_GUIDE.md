# Team Optimization Methods Guide

## Overview

The team optimizer now supports **4 different algorithms** for finding optimal cookie teams, plus the ability to **build around specific cookies**. Each method has different strengths and use cases.

---

## Optimization Methods

### 1. **Random Sampling** (Default)
```bash
python3 team_optimizer.py --method random --generate 1000 --top 10
```

**How it works:**
- Generates N random 5-cookie teams
- Scores each team
- Returns top performers

**Pros:**
- ⚡ Very fast (0.01s for 1000 teams)
- Good baseline for comparison
- Explores diverse team compositions

**Cons:**
- May miss optimal solutions
- Results vary between runs

**Best for:**
- Quick exploration
- Large-scale team discovery
- Generating variety

**Typical Score:** 85-89/100

---

### 2. **Greedy Algorithm**
```bash
python3 team_optimizer.py --method greedy --generate 1000 --top 10
```

**How it works:**
- Starts with highest-power cookies
- Fills remaining slots strategically
- Favors rarity and power

**Pros:**
- ⚡ Very fast (0.01s for 1000 teams)
- Prioritizes strong cookies
- Consistent results

**Cons:**
- May get stuck in local optima
- Less role diversity than other methods

**Best for:**
- Power-focused teams
- When you want high-rarity cookies
- Quick recommendations

**Typical Score:** 88-91/100

---

### 3. **Genetic Algorithm** (⭐ Recommended)
```bash
python3 team_optimizer.py --method genetic --generate 100 --top 10
```

**How it works:**
- Starts with random population of teams
- "Breeds" best performers (crossover)
- Introduces random mutations
- Evolves over multiple generations

**Pros:**
- 🏆 **Best scores** (92-96/100)
- Avoids local optima
- Great for "build-around" scenarios
- Balances power + synergy

**Cons:**
- Slower (0.02-0.1s for 50-100 generations)
- Slightly more complex

**Best for:**
- Finding absolute best teams
- Building around specific cookies
- When quality > speed

**Typical Score:** 92-96/100 ⭐

---

### 4. **Exhaustive Search** (Guaranteed Optimal)
```bash
# ONLY use with required cookies!
python3 team_optimizer.py --method exhaustive --require "Shadow Milk Cookie,Pure Vanilla Cookie,Dark Cacao Cookie"
```

**How it works:**
- Generates **ALL** possible team combinations
- Tests every single one
- Returns guaranteed optimal result

**Pros:**
- 💯 Guaranteed optimal solution
- No guesswork
- Perfect for final decisions

**Cons:**
- ⚠️ **EXTREMELY SLOW** without required cookies
  - 0 required: 138,313,260 combinations
  - 3 required: 15,051 combinations (manageable!)
  - 4 required: 173 combinations (instant!)

**Best for:**
- Finding THE BEST team with 3+ required cookies
- Final validation
- When you must have certainty

**Typical Score:** 96-99/100 (true optimal)

---

## Building Around Specific Cookies

### Use Case: "I just got Shadow Milk Cookie - what team should I build?"

```bash
python3 team_optimizer.py --require "Shadow Milk Cookie" --method genetic --generate 100 --top 5
```

**Result:**
```
🔒 Required cookies: Shadow Milk Cookie

🏆 Top Team (Score: 92.5/100)
1. Shadow Milk Cookie (Beast, Magic, Middle) - Power: 7.00    [REQUIRED]
2. Pure Vanilla Cookie (Ancient, Healing, Rear) - Power: 6.50  [RECOMMENDED]
3. Burning Spice Cookie (Beast, Charge, Front) - Power: 7.00   [RECOMMENDED]
4. Hollyberry Cookie (Ancient, Defense, Front) - Power: 6.50   [RECOMMENDED]
5. White Lily Cookie (Ancient, Bomber, Middle) - Power: 6.00   [RECOMMENDED]
```

The optimizer found the **4 best teammates** for Shadow Milk Cookie!

---

### Multiple Required Cookies

```bash
python3 team_optimizer.py --require "Pure Vanilla Cookie,Dark Cacao Cookie" --method genetic --top 3
```

**Use case:** "I have these 2 cookies maxed - who should I add?"

---

### Fill Around Your Collection

```bash
python3 team_optimizer.py --require "Mystic Flour Cookie,Burning Spice Cookie,Shadow Milk Cookie" --method exhaustive
```

**Use case:** "I have these 3 Beast cookies - what's the PERFECT team?"

With 3 required cookies, exhaustive search is fast (15K combinations) and gives you the **guaranteed optimal** result!

---

## Performance Comparison

| Method | Teams/Time | Best Score | Speed | Use When |
|--------|------------|-----------|-------|----------|
| Random | 1000 teams | 85-89/100 | 0.01s | Quick exploration |
| Greedy | 1000 teams | 88-91/100 | 0.01s | Power-focused |
| **Genetic** | 100 gen | **92-96/100** | 0.02s | **Best overall** ⭐ |
| Exhaustive* | All combos | 96-99/100 | Varies | With 3+ required |

*Only practical with required cookies

---

## Recommendations by Scenario

### Scenario 1: "What's the best team in the game?"
```bash
python3 team_optimizer.py --method genetic --generate 100 --top 1
```
**Why:** Genetic algorithm finds highest-scoring teams consistently

---

### Scenario 2: "I want 10 different strong team options"
```bash
python3 team_optimizer.py --method random --generate 5000 --top 10
```
**Why:** Random sampling creates diversity

---

### Scenario 3: "Build around my favorite cookie"
```bash
python3 team_optimizer.py --require "Your Cookie Name" --method genetic --generate 100 --top 5
```
**Why:** Genetic algorithm optimizes teammates for your cookie

---

### Scenario 4: "I have these 3 cookies maxed - what's THE BEST team?"
```bash
python3 team_optimizer.py --require "Cookie1,Cookie2,Cookie3" --method exhaustive
```
**Why:** Exhaustive search guarantees optimal with 3+ required (only ~15K combos)

---

### Scenario 5: "Fast recommendation for beginners"
```bash
python3 team_optimizer.py --method greedy --generate 1000 --top 5
```
**Why:** Greedy is fast and focuses on high-rarity cookies

---

## Advanced Tips

### 1. Combine Methods for Best Results
```bash
# First pass: Genetic to find top 100
python3 team_optimizer.py --method genetic --generate 200 --top 100 --export output/candidates.json

# Second pass: Exhaustive on best cookie combinations
# (Extract common cookies from top teams, then exhaustive search)
```

### 2. Build-Around + Export
```bash
python3 team_optimizer.py --require "Shadow Milk Cookie" --method genetic --generate 100 --top 10 --export output/shadow_milk_teams.json
```
Save all top teams for later comparison!

### 3. Tune Genetic Algorithm Parameters
In Python code:
```python
optimizer = TeamOptimizer('crk-cookies.csv')

# More generations = better results (but slower)
teams = optimizer._generate_genetic_teams(
    generations=200,        # Try 200 generations
    population_size=100,    # Larger population
    required_cookies=['Shadow Milk Cookie']
)
```

### 4. Filter + Optimize
```python
# Only use Epic+ cookies
epic_plus = [c for c in optimizer.all_cookies if c.rarity in {'Epic', 'Super Epic', 'Ancient', 'Beast', 'Legendary'}]
optimizer.all_cookies = epic_plus

# Now optimize with filtered pool
best_teams = optimizer.find_best_teams(n=10, method='genetic')
```

---

## Algorithm Details

### Genetic Algorithm Explained

1. **Initialize Population** (50 random teams)
2. **Evaluate Fitness** (score each team)
3. **Selection** (keep top 20% as "elites")
4. **Crossover** (breed new teams from elites)
   - Parent 1: [A, B, C, D, E]
   - Parent 2: [F, G, H, I, J]
   - Child: [A, B, H, I, J] (random mix)
5. **Mutation** (10% chance to replace 1 cookie)
6. **Repeat** for N generations
7. **Return** final population

**Why it works:**
- Good teams pass their cookies to next generation
- Crossover combines strengths from multiple teams
- Mutation prevents getting stuck
- Evolution naturally finds high-scoring combinations

---

### Exhaustive Search Explained

**Combinatorics:**
```
C(n, r) = n! / (r! × (n-r)!)

Examples:
- C(177, 5) = 138,313,260 combinations (all cookies)
- C(174, 2) = 15,051 combinations (3 cookies required)
- C(173, 1) = 173 combinations (4 cookies required)
```

**Why use required cookies:**
- Drastically reduces search space
- Makes exhaustive search practical
- Still guarantees optimal result

---

## When Each Method Wins

| Criterion | Winner | Why |
|-----------|--------|-----|
| **Best Score** | Genetic/Exhaustive | Finds global optimum |
| **Fastest** | Random/Greedy | Simple sampling |
| **Most Consistent** | Genetic | Converges to quality |
| **Guaranteed Optimal** | Exhaustive | Tests everything |
| **Build-Around** | Genetic | Optimizes teammates |
| **Exploration** | Random | Maximum diversity |

---

## Summary

🏆 **Default Recommendation:** Use `--method genetic --generate 100`

- Best balance of speed and quality
- Scores 92-96/100 consistently
- Works great with required cookies
- Only takes ~0.02-0.1 seconds

💡 **For "Build-Around" scenarios:** Always use genetic with `--require`

🔬 **For guaranteed optimal:** Use exhaustive with 3+ required cookies

⚡ **For quick exploration:** Use random with high `--generate` value

---

## Code Examples

See [example_optimization_methods.py](example_optimization_methods.py) for runnable examples of:
- Comparing all methods
- Building around specific cookies
- Exhaustive search demonstrations
- Practical use cases

Run it:
```bash
python3 example_optimization_methods.py
```
