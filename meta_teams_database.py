"""
Meta Teams Database for Cookie Run: Kingdom (2025)

This module contains current PvP Arena meta teams, their weaknesses,
and recommended counter strategies based on January 2025 competitive data.

Sources:
- https://www.ldplayer.net/blog/cookierun-kingdom-arena-meta-teams.html
- https://www.noff.gg/cookie-run-kingdom/tier-list
- https://gamerant.com/cookie-run-kingdom-best-team-builds-kingdom-arena-meta/
"""

from typing import Dict, List, Optional

# Meta team compositions for 2025 Arena
META_TEAMS = {
    "Silent Berry Milk": {
        "tier": "S+",
        "archetype": "Control + Burst Damage",
        "description": "Top tier Arena team combining lockdown, shields, healing, and debuffs",
        "core_cookies": [
            "Silent Salt Cookie",
            "Shadow Milk Cookie",
            "Hollyberry Cookie (Ascended)"
        ],
        "typical_composition": [
            "Silent Salt Cookie",
            "Shadow Milk Cookie",
            "Hollyberry Cookie (Ascended)",
            "Doughael",
            "Eternal Sugar Cookie"
        ],
        "alternative_cookies": {
            "Hollyberry Cookie (Ascended)": ["Hollyberry Cookie"],
            "Doughael": ["Pure Vanilla Cookie (Ascended)", "Marshmallow Bunny Cookie"]
        },
        "strengths": [
            "Exceptional crowd control",
            "High burst damage from Silent Salt",
            "Strong shields and damage reduction",
            "Healing and sustain",
            "Debuffs enemy team"
        ],
        "weaknesses": [
            "Vulnerable to dispel/cleanse",
            "Requires high investment",
            "Weak against taunt defenders"
        ],
        "counter_roles": ["Debuff cleanse", "Dispel", "Taunt"],
        "counter_cookies": [
            "Cream Ferret Cookie",  # Anti-CC cleanse
            "Elder Faerie Cookie",   # Taunt to lure Shadow Milk
            "Pure Vanilla Cookie (Ascended)",  # Shields and cleanse
            "Burning Spice Cookie"   # High burst to eliminate threats fast
        ],
        "recommended_treasures": [
            "Pilgrim's Scroll",
            "Sugar Swan's Shining Feather",
            "Jelly Watch"
        ],
        "treasure_rationale": "Cooldown reduction critical for Shadow Milk lockdown cycling"
    },

    "Pure Damage Build": {
        "tier": "S+",
        "archetype": "Glass Cannon Burst",
        "description": "Maximum damage output with minimal support, focusing on quick eliminations",
        "core_cookies": [
            "Burning Spice Cookie",
            "Shadow Milk Cookie",
            "Pure Vanilla Cookie (Ascended)"
        ],
        "typical_composition": [
            "Burning Spice Cookie",
            "Pure Vanilla Cookie (Ascended)",
            "Shadow Milk Cookie",
            "Dark Cacao Cookie (Ascended)",
            "Wind Archer"
        ],
        "alternative_cookies": {
            "Wind Archer": ["Stormbringer Cookie", "Black Pearl Cookie"],
            "Dark Cacao Cookie (Ascended)": ["Dark Cacao Cookie", "Moonlight Cookie"]
        },
        "strengths": [
            "Extremely high burst damage",
            "Single-target elimination",
            "AoE damage potential",
            "Debuffs on support units"
        ],
        "weaknesses": [
            "Low sustain/healing",
            "Vulnerable to coordinated burst",
            "Relies on killing enemies before they respond",
            "Weak frontline"
        ],
        "counter_roles": ["Tank", "Healing", "DMG Resist"],
        "counter_cookies": [
            "Hollyberry Cookie (Ascended)",  # DMG reduction + shields
            "Mystic Flour Cookie",           # Control + sustain
            "Financier Cookie",              # Tank + damage immunity
            "Cotton Cookie"                  # Healing + summons
        ],
        "recommended_treasures": [
            "Squishy Jelly Watch",
            "Old Pilgrim's Scroll",
            "Gatekeeper Ghost's Horn"
        ],
        "treasure_rationale": "ATK boost and cooldown to maximize damage windows"
    },

    "Millennial Tree Tank": {
        "tier": "S",
        "archetype": "Sustain + Attrition",
        "description": "High HP tank team with strong shields and steady damage for prolonged fights",
        "core_cookies": [
            "Millennial Tree Cookie",
            "Hollyberry Cookie (Ascended)"
        ],
        "typical_composition": [
            "Millennial Tree Cookie",
            "Hollyberry Cookie (Ascended)",
            "Pure Vanilla Cookie (Ascended)",
            "Shadow Milk Cookie",
            "Eternal Sugar Cookie"
        ],
        "alternative_cookies": {
            "Hollyberry Cookie (Ascended)": ["Dark Cacao Cookie (Ascended)"],
            "Pure Vanilla Cookie (Ascended)": ["Pure Vanilla Cookie", "Doughael"]
        },
        "strengths": [
            "Extremely high HP pool",
            "Strong shields",
            "Sustained healing",
            "Survives heavy bursts",
            "Outlasts opponents"
        ],
        "weaknesses": [
            "Slow damage output",
            "Vulnerable to sustained DPS",
            "Can be outlasted by better sustain",
            "Weak against shield breakers"
        ],
        "counter_roles": ["Sustained DPS", "Shield Break", "Healing Reduction"],
        "counter_cookies": [
            "Burning Spice Cookie",      # High sustained damage
            "Black Pearl Cookie",        # Scaling damage over time
            "Frost Queen Cookie",        # AoE + CC
            "Stormbringer Cookie"        # Electrifying sustained damage
        ],
        "recommended_treasures": [
            "Sugar Swan's Shining Feather",
            "Sacred Pomegranate Branch",
            "Librarian's Enchanted Robes"
        ],
        "treasure_rationale": "Healing amplification and debuff resist for maximum sustain"
    },

    "Thunderstrike Team": {
        "tier": "A+",
        "archetype": "AoE Electro Damage",
        "description": "Combines electrifying AoE damage with healing support",
        "core_cookies": [
            "Stormbringer Cookie",
            "Doughael"
        ],
        "typical_composition": [
            "Stormbringer Cookie",
            "Hollyberry Cookie (Ascended)",
            "Doughael",
            "Shadow Milk Cookie",
            "Eternal Sugar Cookie"
        ],
        "alternative_cookies": {
            "Doughael": ["Pure Vanilla Cookie (Ascended)", "Cotton Cookie"],
            "Eternal Sugar Cookie": ["Mystic Flour Cookie"]
        },
        "strengths": [
            "Strong AoE damage",
            "Frontline defense",
            "Healing support",
            "Electrifying damage effects"
        ],
        "weaknesses": [
            "Vulnerable to single-target burst",
            "Requires setup time",
            "Can be rushed down"
        ],
        "counter_roles": ["Burst Damage", "Stun", "Interrupt"],
        "counter_cookies": [
            "Silent Salt Cookie",        # High single-target damage
            "Mystic Flour Cookie",       # Control + interrupt
            "Burning Spice Cookie",      # Quick elimination
            "Shadow Milk Cookie"         # Lockdown key targets
        ],
        "recommended_treasures": [
            "Gatekeeper Ghost's Horn",
            "Old Pilgrim's Scroll",
            "Squishy Jelly Watch"
        ],
        "treasure_rationale": "ATK boost for AoE damage amplification"
    },

    "Defensive Wall": {
        "tier": "A",
        "archetype": "Defense + Sustain",
        "description": "Strong defense with sustained offensive power and debuff application",
        "core_cookies": [
            "Hollyberry Cookie (Ascended)",
            "Pure Vanilla Cookie (Ascended)",
            "Shadow Milk Cookie"
        ],
        "typical_composition": [
            "Hollyberry Cookie (Ascended)",
            "Doughael",
            "Pure Vanilla Cookie (Ascended)",
            "Eternal Sugar Cookie",
            "Shadow Milk Cookie"
        ],
        "alternative_cookies": {
            "Hollyberry Cookie (Ascended)": ["Hollyberry Cookie", "Dark Cacao Cookie (Ascended)"],
            "Doughael": ["Cotton Cookie", "Parfait Cookie"]
        },
        "strengths": [
            "Excellent frontline defense",
            "Dual healing sources",
            "Damage buffs",
            "Enemy debuffs",
            "High survivability"
        ],
        "weaknesses": [
            "Lower damage output",
            "Slower win condition",
            "Vulnerable to sustained pressure",
            "Can be outscaled"
        ],
        "counter_roles": ["Sustained DPS", "Shield Break", "Armor Penetration"],
        "counter_cookies": [
            "Black Pearl Cookie",        # Scaling magic damage
            "Moonlight Cookie",          # Sustained DPS + CC
            "Frost Queen Cookie",        # AoE + stun
            "Burning Spice Cookie"       # Armor penetration
        ],
        "recommended_treasures": [
            "Sacred Pomegranate Branch",
            "Sugar Swan's Shining Feather",
            "Librarian's Enchanted Robes"
        ],
        "treasure_rationale": "Maximize healing and debuff resistance"
    },

    "Black Pearl Hypercarry": {
        "tier": "A",
        "archetype": "Magic Nuke",
        "description": "Classic Black Pearl team focused on area control and scaling damage",
        "core_cookies": [
            "Black Pearl Cookie",
            "Sea Fairy Cookie"
        ],
        "typical_composition": [
            "Black Pearl Cookie",
            "Sea Fairy Cookie",
            "Frost Queen Cookie",
            "Clotted Cream Cookie",
            "Financier Cookie"
        ],
        "alternative_cookies": {
            "Frost Queen Cookie": ["Moonlight Cookie", "Stormbringer Cookie"],
            "Clotted Cream Cookie": ["Pure Vanilla Cookie (Ascended)"],
            "Financier Cookie": ["Dark Cacao Cookie (Ascended)", "Wildberry Cookie"]
        },
        "strengths": [
            "Massive AoE damage",
            "Strong area control",
            "Stun chains",
            "Scaling damage over time"
        ],
        "weaknesses": [
            "Vulnerable to stun immunity",
            "Weak against high HP tanks",
            "Requires setup time",
            "Susceptible to cleanse/dispel"
        ],
        "counter_roles": ["Stun Immunity", "High HP Tank", "Dispel"],
        "counter_cookies": [
            "Dark Cacao Cookie (Ascended)",   # Stun immunity + tank
            "Wildberry Cookie",                # Stun immunity + protection
            "Financier Cookie",                # Damage immunity
            "Cream Ferret Cookie"              # Cleanse + debuff removal
        ],
        "recommended_treasures": [
            "Old Pilgrim's Scroll",
            "Gatekeeper Ghost's Horn",
            "Sugar Swan's Shining Feather"
        ],
        "treasure_rationale": "Maximize magic damage and cooldown efficiency"
    },

    "Beast Dominance": {
        "tier": "S+",
        "archetype": "Multi-Beast Meta",
        "description": "Combines multiple Beast cookies for overwhelming power",
        "core_cookies": [
            "Shadow Milk Cookie",
            "Mystic Flour Cookie",
            "Eternal Sugar Cookie"
        ],
        "typical_composition": [
            "Shadow Milk Cookie",
            "Mystic Flour Cookie",
            "Eternal Sugar Cookie",
            "Silent Salt Cookie",
            "Burning Spice Cookie"
        ],
        "alternative_cookies": {
            "Burning Spice Cookie": ["Hollyberry Cookie (Ascended)", "Pure Vanilla Cookie (Ascended)"]
        },
        "strengths": [
            "Overwhelming individual power",
            "Multiple win conditions",
            "Excellent synergy between Beasts",
            "Dominates current meta"
        ],
        "weaknesses": [
            "Extremely high investment required",
            "Vulnerable to anti-meta counters",
            "Can be countered by specific team comps"
        ],
        "counter_roles": ["Cleanse", "Immunity", "Taunt"],
        "counter_cookies": [
            "Cream Ferret Cookie",              # Anti-CC specialist
            "Elder Faerie Cookie",              # Taunt to redirect
            "Pure Vanilla Cookie (Ascended)",   # Shields and immunity
            "Financier Cookie"                  # Damage immunity
        ],
        "recommended_treasures": [
            "Old Pilgrim's Scroll",
            "Squishy Jelly Watch",
            "Jelly Watch"
        ],
        "treasure_rationale": "Cooldown reduction critical for chaining Beast abilities"
    }
}


# Cookie-specific counter relationships
COOKIE_COUNTERS = {
    "Shadow Milk Cookie": {
        "counters": [
            "Cream Ferret Cookie",  # Cleanse his lockdown
            "Elder Faerie Cookie",  # Taunt to redirect
            "Shadow Milk Cookie"    # Only he can counter himself in PvP
        ],
        "threat_level": 10,
        "primary_threats": ["Single-target lockdown", "Revival mechanic", "Debuff application"],
        "counter_strategy": "Use taunt defenders to lure him away from key targets, or cleanse debuffs immediately"
    },

    "Black Pearl Cookie": {
        "counters": [
            "Dark Cacao Cookie (Ascended)",
            "Wildberry Cookie",
            "Financier Cookie",
            "Hollyberry Cookie (Ascended)"
        ],
        "threat_level": 8,
        "primary_threats": ["AoE magic damage", "Stun chains", "Scaling damage"],
        "counter_strategy": "Use stun-immune tanks or high HP cookies to absorb damage"
    },

    "Eternal Sugar Cookie": {
        "counters": [
            "Cream Ferret Cookie",
            "Pure Vanilla Cookie (Ascended)",
            "Burning Spice Cookie"
        ],
        "threat_level": 9,
        "primary_threats": ["Shackle/disable", "Debuff application", "Team buffs"],
        "counter_strategy": "Cleanse debuffs quickly or use burst damage to eliminate her fast"
    },

    "Silent Salt Cookie": {
        "counters": [
            "Hollyberry Cookie (Ascended)",
            "Dark Cacao Cookie (Ascended)",
            "Financier Cookie"
        ],
        "threat_level": 9,
        "primary_threats": ["Targets highest ATK", "Heavy single-target damage", "Lunar Slash"],
        "counter_strategy": "Use high-defense tanks to absorb Lunar Slash damage"
    },

    "Mystic Flour Cookie": {
        "counters": [
            "Marshmallow Bunny Cookie",
            "Pure Vanilla Cookie (Ascended)",
            "Cream Ferret Cookie"
        ],
        "threat_level": 7,
        "primary_threats": ["Control abilities", "Sustain", "Debuffs"],
        "counter_strategy": "Burst damage before she can establish control, or use cleanse"
    },

    "Burning Spice Cookie": {
        "counters": [
            "Hollyberry Cookie (Ascended)",
            "Dark Cacao Cookie (Ascended)",
            "Shadow Milk Cookie"
        ],
        "threat_level": 8,
        "primary_threats": ["Single-target burst", "Armor penetration", "High damage"],
        "counter_strategy": "Use damage reduction and shields, or lockdown with Shadow Milk"
    },

    "Frost Queen Cookie": {
        "counters": [
            "Dark Cacao Cookie (Ascended)",
            "Wildberry Cookie",
            "Cream Ferret Cookie"
        ],
        "threat_level": 6,
        "primary_threats": ["AoE stun", "Freeze", "Magic damage"],
        "counter_strategy": "Stun immunity or cleanse abilities"
    },

    "Hollyberry Cookie (Ascended)": {
        "counters": [
            "Burning Spice Cookie",
            "Black Pearl Cookie",
            "Moonlight Cookie"
        ],
        "threat_level": 7,
        "primary_threats": ["45% DMG Focus", "DMG reduction", "Shields"],
        "counter_strategy": "Use sustained DPS or armor penetration to overcome shields"
    },

    "Stormbringer Cookie": {
        "counters": [
            "Silent Salt Cookie",
            "Burning Spice Cookie",
            "Shadow Milk Cookie"
        ],
        "threat_level": 7,
        "primary_threats": ["Electrifying AoE", "Sustained damage"],
        "counter_strategy": "Burst damage to eliminate before AoE ramps up"
    }
}


# Treasure recommendations for different strategies
TREASURE_STRATEGIES = {
    "Offensive Burst": {
        "primary": "Old Pilgrim's Scroll",
        "secondary": "Squishy Jelly Watch",
        "tertiary": "Gatekeeper Ghost's Horn",
        "rationale": "Maximize ATK and cooldown for burst damage windows"
    },
    "Control/Lockdown": {
        "primary": "Jelly Watch",
        "secondary": "Old Pilgrim's Scroll",
        "tertiary": "Sugar Swan's Shining Feather",
        "rationale": "Cooldown reduction to cycle control abilities faster"
    },
    "Sustain/Tank": {
        "primary": "Sugar Swan's Shining Feather",
        "secondary": "Sacred Pomegranate Branch",
        "tertiary": "Librarian's Enchanted Robes",
        "rationale": "Healing amplification and debuff resistance"
    },
    "Anti-CC": {
        "primary": "Librarian's Enchanted Robes",
        "secondary": "Sugar Swan's Shining Feather",
        "tertiary": "Sacred Pomegranate Branch",
        "rationale": "Debuff resistance and cleanse support"
    }
}


def get_meta_team(team_name: str) -> Optional[Dict]:
    """
    Retrieve meta team information by name.

    Args:
        team_name: Name of the meta team

    Returns:
        Dict containing team information, or None if not found
    """
    return META_TEAMS.get(team_name)


def get_cookie_counters(cookie_name: str) -> Optional[Dict]:
    """
    Get counter information for a specific cookie.

    Args:
        cookie_name: Name of the cookie

    Returns:
        Dict containing counter information, or None if not found
    """
    return COOKIE_COUNTERS.get(cookie_name)


def analyze_enemy_team_threats(enemy_cookies: List[str]) -> Dict:
    """
    Analyze enemy team and identify threat levels.

    Args:
        enemy_cookies: List of enemy cookie names

    Returns:
        Dict containing threat analysis
    """
    total_threat = 0
    threats_breakdown = {
        'burst_damage': 0,
        'sustained_damage': 0,
        'crowd_control': 0,
        'healing': 0,
        'tank': 0,
        'high_threat_cookies': []
    }

    for cookie in enemy_cookies:
        counter_info = COOKIE_COUNTERS.get(cookie)
        if counter_info:
            threat = counter_info['threat_level']
            total_threat += threat

            if threat >= 8:
                threats_breakdown['high_threat_cookies'].append({
                    'name': cookie,
                    'threat_level': threat,
                    'threats': counter_info['primary_threats']
                })

    # Estimate threat types based on cookie names/roles
    if any('Shadow Milk' in c or 'Mystic Flour' in c or 'Frost Queen' in c for c in enemy_cookies):
        threats_breakdown['crowd_control'] = 8

    if any('Burning Spice' in c or 'Silent Salt' in c for c in enemy_cookies):
        threats_breakdown['burst_damage'] = 9

    if any('Black Pearl' in c or 'Moonlight' in c or 'Stormbringer' in c for c in enemy_cookies):
        threats_breakdown['sustained_damage'] = 7

    if any('Hollyberry' in c or 'Dark Cacao' in c for c in enemy_cookies):
        threats_breakdown['tank'] = 8

    if any('Doughael' in c or 'Pure Vanilla' in c or 'Cotton' in c for c in enemy_cookies):
        threats_breakdown['healing'] = 7

    return {
        'total_threat_level': total_threat,
        'average_threat': total_threat / len(enemy_cookies) if enemy_cookies else 0,
        'threats_breakdown': threats_breakdown
    }


def recommend_counter_team(enemy_cookies: List[str]) -> Dict:
    """
    Recommend counter team based on enemy composition.

    Args:
        enemy_cookies: List of enemy cookie names

    Returns:
        Dict with recommended counter cookies and strategy
    """
    counter_recommendations = {
        'recommended_cookies': [],
        'strategy': "",
        'treasures': [],
        'priority_targets': []
    }

    # Analyze threats
    threat_analysis = analyze_enemy_team_threats(enemy_cookies)

    # Collect all recommended counters
    all_counters = []
    for cookie in enemy_cookies:
        counter_info = COOKIE_COUNTERS.get(cookie)
        if counter_info:
            all_counters.extend(counter_info['counters'])
            if counter_info['threat_level'] >= 8:
                counter_recommendations['priority_targets'].append(cookie)

    # Count most recommended counters
    from collections import Counter
    counter_counts = Counter(all_counters)
    top_counters = counter_counts.most_common(5)

    counter_recommendations['recommended_cookies'] = [c[0] for c in top_counters]

    # Determine strategy based on threat types
    threats = threat_analysis['threats_breakdown']

    if threats['crowd_control'] >= 7:
        counter_recommendations['strategy'] = "Use Cream Ferret Cookie for cleanse and anti-CC. Prioritize debuff removal and immunity."
        counter_recommendations['treasures'] = ["Librarian's Enchanted Robes", "Sugar Swan's Shining Feather"]

    elif threats['burst_damage'] >= 8:
        counter_recommendations['strategy'] = "Use high HP tanks with damage reduction. Hollyberry (Ascended) or Dark Cacao (Ascended) essential."
        counter_recommendations['treasures'] = ["Sugar Swan's Shining Feather", "Sacred Pomegranate Branch"]

    elif threats['sustained_damage'] >= 7:
        counter_recommendations['strategy'] = "Focus on burst damage to eliminate threats quickly. Shadow Milk lockdown critical."
        counter_recommendations['treasures'] = ["Old Pilgrim's Scroll", "Jelly Watch"]

    else:
        counter_recommendations['strategy'] = "Balanced team composition. Match their sustain or out-damage them."
        counter_recommendations['treasures'] = ["Old Pilgrim's Scroll", "Sugar Swan's Shining Feather"]

    return counter_recommendations
