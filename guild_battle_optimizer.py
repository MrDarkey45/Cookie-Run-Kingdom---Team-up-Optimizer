"""
Guild Battle Optimizer Module for Cookie Run: Kingdom

This module generates optimal teams for Guild Battle bosses based on:
- Boss-specific mechanics and vulnerabilities
- Damage maximization strategies
- Required cookie attributes (water element, AOE, DEF shred, etc.)
- Counter strategies for each of the 4 Guild Battle bosses

Bosses:
    - Red Velvet Dragon
    - Avatar of Destiny
    - Living Abyss
    - Machine-God of the Eternal Void
"""

from typing import List, Dict, Tuple, Optional
from team_optimizer import Cookie, Team, TeamOptimizer
import random


# ==================== BOSS PROFILES ====================

GUILD_BOSSES = {
    'Red Velvet Dragon': {
        'description': '75% damage reflection, high DEF. Avoid burst damage, use DEF shred and indirect damage.',
        'mechanics': [
            'Red Dragon\'s Scales: Reflects 75% of damage back to attacker',
            'Extremely high DEF requiring DEF reduction',
            'Susceptible to most debuffs',
            'Summons Red Velvet Wraiths',
            'Dragon Breath: Continuous damage (350% ATK per hit)'
        ],
        'strategy': [
            'Prioritize DEF reduction (Dark Choco, Candy Apple) before deploying high-damage skills',
            'Use indirect damage (poison, electrifying effects) that bypass damage reflection',
            'Employ intangible state skills to avoid reflection damage',
            'Avoid burst-damage specialists unless DEF debuffs are active'
        ],
        'preferred_attributes': ['def_shred', 'indirect_damage'],
        'avoid_attributes': [],
        's_tier_cookies': [
            'Black Sapphire Cookie', 'Prune Juice Cookie', 'Shadow Milk Cookie',
            'Candy Apple Cookie', 'Dark Choco Cookie'
        ],
        'a_tier_cookies': [
            'Affogato Cookie', 'Eclair Cookie', 'Black Lemonade Cookie',
            'Poison Mushroom Cookie', 'Vampire Cookie'
        ]
    },

    'Avatar of Destiny': {
        'description': 'Immune to debuffs (triggers Reversal). Use periodic damage, shields, and ATK SPD buffs.',
        'mechanics': [
            'Destiny: Reversal - Immune to debuffs, stacks counters (3 stacks = 50% max HP damage + stun)',
            'Destiny: Weakness - Takes 45% increased damage',
            'Destiny: Doom - 100% max HP true damage (instant KO without shields)',
            'Summons 5 indestructible Stones of Destiny (33 hit durability each)',
            'Periodic damage (poison/burn) does NOT trigger Reversal counter'
        ],
        'strategy': [
            'Use Crème Brûlée Cookie\'s Accelerando skill (designed for this boss)',
            'Stack ATK SPD buffs (Mint Choco, Star Coral)',
            'Avoid debuff-focused cookies (Black Raisin, Captain Caviar, Linzer)',
            'Use shields to protect against Doom instant-KO (Blackberry, Star Coral)',
            'Multi-hit skills to destroy Stones of Destiny (Pudding à la Mode, Macaron)'
        ],
        'preferred_attributes': ['attack_speed_buff', 'shield_provider', 'indirect_damage'],
        'avoid_attributes': ['debuff_heavy'],
        's_tier_cookies': [
            'Crème Brûlée Cookie', 'Pudding à la Mode Cookie', 'Star Coral Cookie',
            'Cream Ferret Cookie', 'Mint Choco Cookie'
        ],
        'a_tier_cookies': [
            'Twizzly Gummy Cookie', 'Marshmallow Cookie', 'Blackberry Cookie',
            'Macaron Cookie', 'Fire Spirit Cookie'
        ]
    },

    'Living Abyss': {
        'description': '95% damage reduction on boss. Target ooze blobs with AOE damage and crowd control.',
        'mechanics': [
            'Chill of the Abyss: Immune to debuffs except Burn and Vampiric Bite',
            '95% damage reduction on boss - direct attacks ineffective',
            'Abyssal Hive: Spawns 8 Licorice Ooze blobs (19.3% damage transfer to boss)',
            'Ooze blobs gain Weakness stacks (up to 50) from incapacitating debuffs',
            'Devour: Swallows highest HP target for 5 seconds'
        ],
        'strategy': [
            'Prioritize AOE damage over single-target attacks',
            'Target ooze blobs instead of the boss directly',
            'Use continuous incapacitating abilities to stack Weakness on blobs',
            'Skills scaling with multiple targets are most effective',
            'Focus on eliminating oozes for sustained damage'
        ],
        'preferred_attributes': ['aoe_damage'],
        'avoid_attributes': ['single_target_focus'],
        's_tier_cookies': [
            'Blueberry Pie Cookie', 'Black Forest Cookie', 'Twizzly Gummy Cookie',
            'Eternal Sugar Cookie', 'Wedding Cake Cookie'
        ],
        'a_tier_cookies': [
            'Black Pearl Cookie', 'Frost Queen Cookie', 'Sea Fairy Cookie',
            'Pumpkin Pie Cookie', 'Espresso Cookie'
        ]
    },

    'Machine-God of the Eternal Void': {
        'description': 'Water-element focus. Multi-part boss weak to water, immune to electric.',
        'mechanics': [
            'Unstable Engineering: Immune to most debuffs except water-based',
            'Takes extra damage from water-element attacks',
            'Immune to electric damage',
            'Multi-part boss - AOE hits multiple targets simultaneously',
            'Difficulty scales significantly after level 50'
        ],
        'strategy': [
            'Use water-element cookies exclusively for optimal damage',
            'Seltzer + Menthol synergy: Stinging Fizz + Menthol Censer = massive Water DMG',
            'Stack water damage buffs (Cream Soda +30%, Frilled Jellyfish +32.5%)',
            'Sea Fairy Rally Effect: +45% ATK to team',
            'Skill rotation: Sea Fairy → Seltzer (59.625s) → Frilled Jellyfish → Menthol (59.200s) → Cream Soda (58.625s)'
        ],
        'preferred_attributes': ['water_element', 'aoe_damage'],
        'avoid_attributes': ['electric_element'],
        's_tier_cookies': [
            'Menthol Cookie', 'Seltzer Cookie', 'Cream Soda Cookie',
            'Frilled Jellyfish Cookie', 'Sea Fairy Cookie'
        ],
        'a_tier_cookies': [
            'Oyster Cookie', 'Sorbet Shark Cookie', 'Peppermint Cookie',
            'Squid Ink Cookie', 'Cream Ferret Cookie'
        ]
    }
}


# ==================== GUILD BATTLE OPTIMIZER CLASS ====================

class GuildBattleOptimizer:
    """Generates optimal teams for Guild Battle bosses."""

    def __init__(self, optimizer: TeamOptimizer):
        """
        Initialize the Guild Battle optimizer.

        Args:
            optimizer: TeamOptimizer instance with loaded cookies
        """
        self.optimizer = optimizer
        self.all_cookies = optimizer.all_cookies
        self.all_treasures = optimizer.all_treasures

    def get_boss_info(self, boss_name: str) -> Dict:
        """
        Get detailed information about a Guild Battle boss.

        Args:
            boss_name: Name of the boss

        Returns:
            dict: Boss profile with mechanics and strategies
        """
        return GUILD_BOSSES.get(boss_name, {})

    def score_cookie_for_boss(self, cookie: Cookie, boss_name: str) -> float:
        """
        Score a cookie's effectiveness against a specific boss.

        Args:
            cookie: Cookie to evaluate
            boss_name: Name of the boss

        Returns:
            float: Score from 0-100 (higher is better)
        """
        boss = GUILD_BOSSES.get(boss_name, {})
        if not boss:
            return 50.0  # Neutral score if boss not found

        base_score = 50.0

        # S-tier cookies get massive bonus
        if cookie.name in boss['s_tier_cookies']:
            base_score += 40.0

        # A-tier cookies get good bonus
        elif cookie.name in boss['a_tier_cookies']:
            base_score += 25.0

        # Check preferred attributes
        for attr in boss['preferred_attributes']:
            if hasattr(cookie, attr) and getattr(cookie, attr):
                base_score += 10.0

        # Penalize avoided attributes
        for attr in boss['avoid_attributes']:
            if hasattr(cookie, attr) and getattr(cookie, attr):
                base_score -= 15.0

        # Bonus for high power score
        base_score += cookie.get_power_score() * 2  # Small bonus for power

        return min(100.0, max(0.0, base_score))

    def generate_guild_battle_team(
        self,
        boss_name: str,
        required_cookies: Optional[List[str]] = None,
        num_teams: int = 5
    ) -> List[Dict]:
        """
        Generate optimized teams for a Guild Battle boss.

        Args:
            boss_name: Name of the boss to counter
            required_cookies: List of cookie names that must be included
            num_teams: Number of team variations to generate

        Returns:
            list: List of team dictionaries with scores and strategies
        """
        boss = GUILD_BOSSES.get(boss_name)
        if not boss:
            raise ValueError(f"Unknown boss: {boss_name}")

        # Get required cookies
        required = []
        if required_cookies:
            for name in required_cookies:
                cookie = next((c for c in self.all_cookies if c.name == name), None)
                if cookie:
                    required.append(cookie)

        # Score all cookies for this boss
        cookie_scores = []
        for cookie in self.all_cookies:
            if cookie not in required:
                score = self.score_cookie_for_boss(cookie, boss_name)
                cookie_scores.append((cookie, score))

        # Sort by score (highest first)
        cookie_scores.sort(key=lambda x: x[1], reverse=True)

        # Generate teams
        teams = []
        used_combinations = set()

        for attempt in range(num_teams * 10):  # Try multiple times
            if len(teams) >= num_teams:
                break

            # Start with required cookies
            team_cookies = required.copy()

            # Add top-scored cookies with some randomness
            available = [c for c, s in cookie_scores if c not in team_cookies]

            # Weighted random selection (higher scores = higher probability)
            while len(team_cookies) < 5 and available:
                # Take top candidates with bias toward higher scores
                top_candidates = available[:min(15, len(available))]

                # Weight by position (exponential decay)
                weights = [2 ** (15 - i) for i in range(len(top_candidates))]
                selected = random.choices(top_candidates, weights=weights, k=1)[0]

                team_cookies.append(selected)
                available.remove(selected)

            if len(team_cookies) != 5:
                continue

            # Check for duplicates
            team_key = tuple(sorted([c.name for c in team_cookies]))
            if team_key in used_combinations:
                continue

            used_combinations.add(team_key)

            # Create team and score it
            try:
                team = Team(team_cookies)
                team_score = self.score_team_for_boss(team, boss_name)

                teams.append({
                    'team': team,
                    'score': team_score,
                    'boss': boss_name,
                    'strategy': self.generate_team_strategy(team, boss_name)
                })
            except ValueError:
                continue

        # Sort teams by score
        teams.sort(key=lambda x: x['score'], reverse=True)

        return teams[:num_teams]

    def score_team_for_boss(self, team: Team, boss_name: str) -> float:
        """
        Score a team's effectiveness against a boss.

        Args:
            team: Team to evaluate
            boss_name: Name of the boss

        Returns:
            float: Team score (0-100)
        """
        boss = GUILD_BOSSES.get(boss_name, {})

        # Average individual cookie scores
        cookie_scores = [self.score_cookie_for_boss(c, boss_name) for c in team.cookies]
        avg_score = sum(cookie_scores) / len(cookie_scores)

        # Bonus for team synergy
        synergy_bonus = min(10.0, team.synergy_score / 5)

        # Bonus for having S-tier cookies
        s_tier_count = sum(1 for c in team.cookies if c.name in boss['s_tier_cookies'])
        s_tier_bonus = s_tier_count * 5.0

        # Check attribute coverage
        coverage_bonus = 0
        for attr in boss['preferred_attributes']:
            if any(hasattr(c, attr) and getattr(c, attr) for c in team.cookies):
                coverage_bonus += 3.0

        total_score = avg_score + synergy_bonus + s_tier_bonus + coverage_bonus

        return min(100.0, total_score)

    def generate_team_strategy(self, team: Team, boss_name: str) -> str:
        """
        Generate strategic recommendations for a team against a boss.

        Args:
            team: The team composition
            boss_name: Name of the boss

        Returns:
            str: Strategy description
        """
        boss = GUILD_BOSSES.get(boss_name, {})

        cookie_names = [c.name for c in team.cookies]
        s_tier_in_team = [c for c in cookie_names if c in boss['s_tier_cookies']]

        strategy_parts = []

        # Mention S-tier cookies
        if s_tier_in_team:
            if len(s_tier_in_team) == 1:
                strategy_parts.append(f"★ {s_tier_in_team[0]} is your key damage dealer.")
            else:
                strategy_parts.append(f"★ Focus on: {', '.join(s_tier_in_team[:2])}")

        # Add boss-specific strategy
        if boss['strategy']:
            strategy_parts.append(boss['strategy'][0])

        return ' '.join(strategy_parts) if strategy_parts else boss['description']
