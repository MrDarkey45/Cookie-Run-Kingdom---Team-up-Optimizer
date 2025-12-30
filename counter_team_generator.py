"""
Counter-Team Generator Module for Cookie Run: Kingdom

This module analyzes enemy team compositions and generates counter-teams based on:
- Role composition (tanks, healers, DPS, support)
- Position distribution (front/middle/rear balance)
- Special cookie threats (Shadow Milk, Beast cookies, etc.)
- Team characteristics (burst damage, CC-heavy, healing-heavy)

Counter Strategy (0-100 confidence):
    Weakness Detection: Identifies exploitable gaps
    Counter Cookie Selection: Suggests specific cookies
    Strategy Recommendations: Explains why counter works
    Counter-Team Scoring: Rates effectiveness against enemy
"""

from typing import List, Dict, Tuple, Optional
from collections import Counter
from team_optimizer import Cookie, Team, TeamOptimizer


# Special cookie categories for counter detection
BEAST_COOKIES = ['Shadow Milk Cookie', 'Eternal Sugar Cookie', 'Mystic Flour Cookie',
                 'Burning Spice Cookie', 'Silent Salt Cookie']

ANTI_HEAL_COOKIES = ['Poison Mushroom Cookie', 'Pumpkin Pie Cookie', 'Stardust Cookie',
                     'Pitaya Dragon Cookie', 'White Lily Cookie']

DEFENSE_SHRED_COOKIES = ['Dark Choco Cookie', 'Candy Apple Cookie', 'Black Lemonade Cookie']

AMBUSH_ASSASSINS = ['Shadow Milk Cookie', 'Vampire Cookie', 'Wind Archer Cookie',
                    'Stormbringer Cookie']

IMMUNITY_PROVIDERS = ['Cream Ferret Cookie', 'Seltzer Cookie', 'Pure Vanilla Cookie']

TAUNT_TANKS = ['Elder Faerie Cookie', 'Wildberry Cookie', 'Dark Cacao Cookie',
               'Milk Cookie', 'Knight Cookie']

CROWD_CONTROL_COOKIES = ['Frost Queen Cookie', 'Silent Salt Cookie', 'Sea Fairy Cookie',
                         'Shadow Milk Cookie']

BURST_DAMAGE_COOKIES = ['Burning Spice Cookie', 'Tarte Tatin Cookie', 'Wind Archer Cookie',
                        'Black Pearl Cookie']

CLEANSE_COOKIES = ['Cream Ferret Cookie', 'Pure Vanilla Cookie', 'Peppermint Cookie',
                   'Sparkling Cookie']

HIGH_HP_TANKS = ['Millennial Tree Cookie', 'Hollyberry Cookie', 'Dark Cacao Cookie',
                 'Elder Faerie Cookie']


class CounterTeamGenerator:
    """Generate counter-teams to exploit enemy weaknesses."""

    def __init__(self, optimizer: TeamOptimizer):
        """
        Initialize the counter-team generator.

        Args:
            optimizer: TeamOptimizer instance with loaded cookies
        """
        self.optimizer = optimizer
        self.all_cookies = optimizer.all_cookies
        self.all_treasures = optimizer.all_treasures

    def analyze_enemy_team(self, enemy_team: Team) -> Dict:
        """
        Analyze enemy team composition to identify characteristics using ability data.

        Args:
            enemy_team: Enemy Team instance to analyze

        Returns:
            dict: Analysis results with team characteristics
        """
        analysis = {
            'healers': 0,
            'healer_list': [],
            'tanks': 0,
            'tank_list': [],
            'dps_count': 0,
            'dps_list': [],
            'front_position': 0,
            'middle_position': 0,
            'rear_position': 0,
            'crowd_control': 0,
            'cc_list': [],
            'cc_types': [],  # Types of CC (Stun, Freeze, Silence, etc.)
            'beast_cookies': 0,
            'beast_list': [],
            'has_shadow_milk': False,
            'anti_heal': 0,
            'anti_heal_list': [],
            'anti_tank': 0,
            'anti_tank_list': [],
            'immunity': False,
            'immunity_types': [],  # Types of immunity granted
            'cleanse': False,
            'cleanse_list': [],
            'taunt': False,
            'burst_damage': False,
            'shield_providers': 0,
            'shield_list': []
        }

        for cookie in enemy_team.cookies:
            # Count healers - use both role AND ability data
            if cookie.role in ['Healing', 'Support'] or cookie.provides_healing:
                analysis['healers'] += 1
                analysis['healer_list'].append(cookie.name)

            # Count tanks
            if cookie.role in ['Defense', 'Charge']:
                analysis['tanks'] += 1
                analysis['tank_list'].append(cookie.name)

            # Count DPS
            if cookie.role in ['Magic', 'Ranged', 'Bomber', 'Ambush']:
                analysis['dps_count'] += 1
                analysis['dps_list'].append(cookie.name)

            # Count positions
            if cookie.position == 'Front':
                analysis['front_position'] += 1
            elif cookie.position == 'Middle':
                analysis['middle_position'] += 1
            elif cookie.position == 'Rear':
                analysis['rear_position'] += 1

            # Crowd control detection - use ability data
            if cookie.crowd_control and cookie.crowd_control != 'None':
                analysis['crowd_control'] += 1
                analysis['cc_list'].append(cookie.name)
                if cookie.crowd_control not in analysis['cc_types']:
                    analysis['cc_types'].append(cookie.crowd_control)

            # Anti-heal detection - use ability data
            if cookie.anti_heal:
                analysis['anti_heal'] += 1
                analysis['anti_heal_list'].append(cookie.name)

            # Anti-tank detection - use ability data
            if cookie.anti_tank:
                analysis['anti_tank'] += 1
                analysis['anti_tank_list'].append(cookie.name)

            # Immunity detection - use ability data
            if cookie.grants_immunity and cookie.grants_immunity != 'None':
                analysis['immunity'] = True
                if cookie.grants_immunity not in analysis['immunity_types']:
                    analysis['immunity_types'].append(cookie.grants_immunity)

            # Dispel/cleanse detection - use ability data
            if cookie.dispel:
                analysis['cleanse'] = True
                analysis['cleanse_list'].append(cookie.name)

            # Shield providers - use ability data
            if cookie.provides_shield:
                analysis['shield_providers'] += 1
                analysis['shield_list'].append(cookie.name)

            # Special cookie detection
            if cookie.rarity == 'Beast':
                analysis['beast_cookies'] += 1
                analysis['beast_list'].append(cookie.name)

            if cookie.name == 'Shadow Milk Cookie':
                analysis['has_shadow_milk'] = True

            # Taunt detection (still using hardcoded list as this is position-based mechanic)
            if cookie.name in TAUNT_TANKS:
                analysis['taunt'] = True

            # Burst damage detection (skill type or hardcoded list)
            if cookie.skill_type == 'Damage' or cookie.name in BURST_DAMAGE_COOKIES:
                analysis['burst_damage'] = True

        return analysis

    def identify_weaknesses(self, enemy_team: Team) -> List[Dict]:
        """
        Identify exploitable weaknesses in enemy team.

        Args:
            enemy_team: Enemy Team to analyze

        Returns:
            List of weakness dicts with exploit strategies
        """
        weaknesses = []
        analysis = self.analyze_enemy_team(enemy_team)

        # Weakness 1: No healing/sustain
        if analysis['healers'] == 0:
            weaknesses.append({
                'weakness': 'No Healing/Sustain',
                'description': 'Team cannot recover from damage over time',
                'exploit': 'Use sustained DPS or high burst damage to overwhelm',
                'priority': 'HIGH',
                'confidence': 95
            })

        # Weakness 2: Tank-heavy frontline
        if analysis['front_position'] >= 3:
            weaknesses.append({
                'weakness': 'Tank-Heavy Frontline',
                'description': f'{analysis["front_position"]} cookies in front position',
                'exploit': 'Use defense shred, ambush cookies, or percentage-based damage',
                'priority': 'HIGH',
                'confidence': 90
            })

        # Weakness 3: Exposed backline
        if analysis['rear_position'] >= 3 and analysis['front_position'] <= 1:
            weaknesses.append({
                'weakness': 'Exposed Backline',
                'description': f'{analysis["rear_position"]} rear cookies with weak frontline',
                'exploit': 'Use ambush assassins to eliminate squishy backline targets',
                'priority': 'HIGH',
                'confidence': 92
            })

        # Weakness 4: No crowd control immunity
        if not analysis['immunity'] and analysis['crowd_control'] == 0:
            weaknesses.append({
                'weakness': 'No CC Immunity',
                'description': 'Team vulnerable to stun/freeze/silence lockdown',
                'exploit': 'Use crowd control heavy team to prevent skill usage',
                'priority': 'MEDIUM',
                'confidence': 75
            })

        # Weakness 5: No debuff cleanse
        if not analysis['cleanse']:
            weaknesses.append({
                'weakness': 'No Debuff Cleanse',
                'description': 'Cannot remove negative status effects',
                'exploit': 'Stack debuffs and damage-over-time effects',
                'priority': 'MEDIUM',
                'confidence': 70
            })

        # Weakness 6: Healing-heavy composition (2+ healers)
        if analysis['healers'] >= 2:
            weaknesses.append({
                'weakness': 'Healing-Heavy Team',
                'description': f'{analysis["healers"]} support/healing cookies',
                'exploit': 'Use anti-heal cookies or burst damage to eliminate healers first',
                'priority': 'HIGH',
                'confidence': 88
            })

        # Weakness 7: Shadow Milk without proper counter
        if analysis['has_shadow_milk'] and not analysis['taunt']:
            weaknesses.append({
                'weakness': 'Shadow Milk Without Taunt Defense',
                'description': 'Shadow Milk can freely assassinate backline',
                'exploit': 'Counter with taunt tanks or Shadow Milk mirror match',
                'priority': 'CRITICAL',
                'confidence': 95
            })

        # Weakness 8: Burst damage team with low sustain
        if analysis['burst_damage'] and analysis['healers'] <= 1:
            weaknesses.append({
                'weakness': 'Burst-Heavy Low-Sustain Team',
                'description': 'High damage but cannot sustain through long fights',
                'exploit': 'Use high HP tanks and shields to survive burst, then attrition',
                'priority': 'HIGH',
                'confidence': 85
            })

        # Weakness 9: No anti-heal against healing teams
        if analysis['healers'] >= 1 and analysis['anti_heal'] == 0:
            weaknesses.append({
                'weakness': 'No Anti-Heal',
                'description': 'Cannot counter enemy healing',
                'exploit': 'If using healing team, stack sustain to outlast',
                'priority': 'LOW',
                'confidence': 60
            })

        return weaknesses

    def generate_counter_strategies(self, enemy_team: Team) -> Dict:
        """
        Generate comprehensive counter strategies based on enemy composition using ability data.

        Args:
            enemy_team: Enemy Team to counter

        Returns:
            dict: Counter strategies with cookie suggestions
        """
        analysis = self.analyze_enemy_team(enemy_team)
        weaknesses = self.identify_weaknesses(enemy_team)

        counter_strategy = {
            'recommended_cookies': [],
            'avoid_cookies': [],
            'strategy_description': '',
            'priority_targets': [],
            'team_archetype': '',
            'confidence': 0
        }

        # Build dynamic counter cookie lists using ability data
        burst_damage_cookies = [c.name for c in self.all_cookies if c.skill_type == 'Damage' and c.rarity in ['Beast', 'Ancient', 'Legendary']]
        anti_heal_cookies = [c.name for c in self.all_cookies if c.anti_heal]
        defense_shred_cookies = [c.name for c in self.all_cookies if c.anti_tank]
        ambush_cookies = [c.name for c in self.all_cookies if c.role == 'Ambush' or c.target_type == 'Backline']
        immunity_cookies = [c.name for c in self.all_cookies if c.grants_immunity and c.grants_immunity != 'None']
        cc_cookies = [c.name for c in self.all_cookies if c.crowd_control and c.crowd_control != 'None']
        shield_cookies = [c.name for c in self.all_cookies if c.provides_shield]
        healing_cookies = [c.name for c in self.all_cookies if c.provides_healing]

        # Strategy 1: Counter no healing
        if analysis['healers'] == 0:
            counter_strategy['recommended_cookies'].extend(burst_damage_cookies[:5])  # Top 5 burst damage
            counter_strategy['avoid_cookies'].extend(anti_heal_cookies)
            counter_strategy['strategy_description'] = 'High burst damage to exploit lack of sustain'
            counter_strategy['team_archetype'] = 'Burst Damage'
            counter_strategy['confidence'] = 90

        # Strategy 2: Counter healing-heavy
        elif analysis['healers'] >= 2:
            counter_strategy['recommended_cookies'].extend(anti_heal_cookies)
            counter_strategy['recommended_cookies'].extend(ambush_cookies[:3])
            counter_strategy['priority_targets'] = analysis['healer_list']
            counter_strategy['strategy_description'] = 'Eliminate healers with ambush cookies and use anti-heal'
            counter_strategy['team_archetype'] = 'Anti-Heal Assassin'
            counter_strategy['confidence'] = 88

        # Strategy 3: Counter tank-heavy
        if analysis['front_position'] >= 3:
            counter_strategy['recommended_cookies'].extend(defense_shred_cookies)
            counter_strategy['strategy_description'] = 'Defense shred and sustained damage against tanks'
            counter_strategy['team_archetype'] = 'Defense Shred'
            counter_strategy['confidence'] = 85

        # Strategy 4: Counter exposed backline
        if analysis['rear_position'] >= 3 and analysis['front_position'] <= 1:
            counter_strategy['recommended_cookies'].extend(ambush_cookies)
            counter_strategy['priority_targets'] = analysis['healer_list'] + analysis['dps_list']
            counter_strategy['strategy_description'] = 'Ambush assassins to eliminate exposed backline'
            counter_strategy['team_archetype'] = 'Dive/Assassin'
            counter_strategy['confidence'] = 92

        # Strategy 5: Counter Shadow Milk
        if analysis['has_shadow_milk']:
            counter_strategy['recommended_cookies'].extend(TAUNT_TANKS)
            counter_strategy['recommended_cookies'].append('Shadow Milk Cookie')  # Mirror match
            counter_strategy['recommended_cookies'].append('Black Pearl Cookie')  # Burst before lockdown
            counter_strategy['avoid_cookies'].append('Single-carry DPS teams')
            counter_strategy['strategy_description'] = 'Taunt tanks to redirect Shadow Milk or mirror match'
            counter_strategy['team_archetype'] = 'Anti-Shadow Milk'
            counter_strategy['confidence'] = 90

        # Strategy 6: Counter CC-heavy
        if analysis['crowd_control'] >= 2:
            counter_strategy['recommended_cookies'].extend(immunity_cookies)
            counter_strategy['strategy_description'] = f'Immunity to counter {", ".join(analysis["cc_types"])} crowd control'
            counter_strategy['team_archetype'] = 'Immunity/Cleanse'
            counter_strategy['confidence'] = 80

        # Strategy 7: Counter burst damage - recommend shields + healing
        if analysis['burst_damage'] and analysis['healers'] <= 1:
            counter_strategy['recommended_cookies'].extend(shield_cookies[:3])
            counter_strategy['recommended_cookies'].extend(healing_cookies[:2])
            counter_strategy['recommended_cookies'].extend(HIGH_HP_TANKS[:2])
            counter_strategy['strategy_description'] = 'High HP tanks, shields, and healing to survive burst, then attrition'
            counter_strategy['team_archetype'] = 'Tank/Sustain'
            counter_strategy['confidence'] = 85

        # Strategy 8: Counter no immunity - recommend CC lockdown
        if not analysis['immunity']:
            counter_strategy['recommended_cookies'].extend(cc_cookies[:3])
            counter_strategy['strategy_description'] = 'Heavy crowd control to lock down enemy team'
            counter_strategy['team_archetype'] = 'CC Lockdown'
            counter_strategy['confidence'] = 82

        # Strategy 9: Counter no cleanse - recommend debuff stacking
        if not analysis['cleanse']:
            debuff_cookies = [c.name for c in self.all_cookies if 'Debuff' in str(c.key_mechanic) or 'DoT' in str(c.key_mechanic)]
            if debuff_cookies:
                counter_strategy['recommended_cookies'].extend(debuff_cookies[:3])
                counter_strategy['strategy_description'] = 'Stack debuffs and damage-over-time effects'

        # Remove duplicates
        counter_strategy['recommended_cookies'] = list(set(counter_strategy['recommended_cookies']))
        counter_strategy['avoid_cookies'] = list(set(counter_strategy['avoid_cookies']))

        return counter_strategy

    def recommend_counter_treasures(self, enemy_team: Team, counter_team: Team, strategy: Dict) -> List[Tuple]:
        """
        Recommend treasures specifically for countering enemy team.

        Args:
            enemy_team: Enemy team to counter
            counter_team: Your counter team
            strategy: Counter strategy dict from generate_counter_strategies

        Returns:
            List of (Treasure, score, reason) tuples
        """
        from team_optimizer import Treasure

        analysis = self.analyze_enemy_team(enemy_team)
        treasure_scores = []

        for treasure in self.all_treasures:
            score = 0.0
            reasons = []

            # Base tier score
            tier_base = {'S+': 10.0, 'S': 8.0, 'A': 6.0, 'B': 4.0, 'C': 2.0}
            score += tier_base.get(treasure.tier_ranking, 2.0)

            # Strategy-based treasure recommendations

            # 1. Counter healing-heavy teams with anti-heal or burst damage
            if analysis['healers'] >= 2:
                if treasure.atk_boost_max > 0 or treasure.crit_boost_max > 0:
                    score += 4.0
                    reasons.append("Burst damage to overwhelm healing")
                if treasure.enemy_debuff:
                    score += 3.0
                    reasons.append("Debuffs to reduce enemy effectiveness")

            # 2. Counter tank-heavy teams with sustained damage and CDR
            if analysis['tanks'] >= 2:
                if treasure.cooldown_reduction_max > 0:
                    score += 4.0
                    reasons.append("CDR for sustained pressure vs tanks")
                if treasure.atk_boost_max > 0:
                    score += 2.0
                    reasons.append("ATK boost for tank-busting")

            # 3. Counter exposed backline with offensive treasures
            if analysis['rear_position'] >= 3 and analysis['front_position'] <= 1:
                if treasure.atk_boost_max > 0 or treasure.crit_boost_max > 0:
                    score += 5.0
                    reasons.append("Offensive stats to punish weak frontline")
                if treasure.cooldown_reduction_max > 0:
                    score += 3.0
                    reasons.append("Faster skills to burst backline")

            # 4. Counter Shadow Milk with defensive treasures
            if analysis['has_shadow_milk']:
                if treasure.hp_shield_max > 0:
                    score += 4.0
                    reasons.append("Shield to survive Shadow Milk burst")
                if treasure.dmg_resist_max > 0:
                    score += 3.0
                    reasons.append("DMG resist vs Shadow Milk")
                if treasure.debuff_cleanse:
                    score += 3.0
                    reasons.append("Cleanse Shadow Milk debuffs")

            # 5. Counter CC-heavy teams with sustain
            if analysis['crowd_control'] >= 2:
                if treasure.hp_shield_max > 0 or treasure.heal_max > 0:
                    score += 4.0
                    reasons.append(f"Sustain to survive {', '.join(analysis['cc_types'])} CC")
                if treasure.debuff_cleanse:
                    score += 5.0
                    reasons.append("Cleanse crowd control effects")

            # 6. Counter burst damage teams with defense
            if analysis['burst_damage']:
                if treasure.hp_shield_max > 0:
                    score += 5.0
                    reasons.append("Shield critical vs burst damage")
                if treasure.dmg_resist_max > 0:
                    score += 4.0
                    reasons.append("DMG resist to survive initial burst")
                if treasure.heal_max > 0:
                    score += 3.0
                    reasons.append("Healing to recover from burst")
                if treasure.revive:
                    score += 4.0
                    reasons.append("Revival as backup vs burst")

            # 7. Exploit no immunity with offensive treasures
            if not analysis['immunity']:
                if treasure.enemy_debuff:
                    score += 4.0
                    reasons.append("Debuffs (enemy has no immunity)")
                if treasure.cooldown_reduction_max > 0:
                    score += 2.0
                    reasons.append("CDR to spam CC")

            # 8. Exploit no cleanse with debuff treasures
            if not analysis['cleanse']:
                if treasure.enemy_debuff:
                    score += 3.0
                    reasons.append("Enemy can't cleanse debuffs")

            # Universal treasures always score well
            if 'Universal' in treasure.recommended_archetypes:
                score += 3.0
                if not reasons:
                    reasons.append("Universal treasure (works with any strategy)")

            # Archetype matching bonus
            team_archetypes = set()
            counter_role_dist = counter_team.get_role_distribution()
            if any(role in counter_role_dist for role in ['Magic', 'Ranged', 'Bomber', 'Ambush']):
                team_archetypes.add('DPS')
            if any(role in counter_role_dist for role in ['Defense', 'Charge']):
                team_archetypes.add('Tank')
            if any(role in counter_role_dist for role in ['Healing', 'Support']):
                team_archetypes.add('Sustain')

            matching_archetypes = set(treasure.recommended_archetypes) & team_archetypes
            if matching_archetypes:
                score += len(matching_archetypes) * 1.5

            # Compile final recommendation
            reason = reasons[0] if reasons else "Standard treasure"
            treasure_scores.append((treasure, score, reason))

        # Sort by score and return top 3
        treasure_scores.sort(key=lambda x: x[1], reverse=True)
        return treasure_scores[:3]

    def find_counter_teams(
        self,
        enemy_team: Team,
        n: int = 5,
        method: str = 'greedy',
        required_cookies: Optional[List[str]] = None
    ) -> List[Tuple[Team, Dict]]:
        """
        Generate counter-teams optimized against enemy composition.

        Args:
            enemy_team: Enemy Team to counter
            n: Number of counter-teams to return
            method: Optimization method ('random', 'greedy', 'genetic')
            required_cookies: Optional list of cookie names that must be included

        Returns:
            List of (Team, counter_info) tuples with counter analysis
        """
        # Get counter strategy
        counter_strategy = self.generate_counter_strategies(enemy_team)
        weaknesses = self.identify_weaknesses(enemy_team)

        # Filter cookies to prioritize counter picks
        recommended_names = counter_strategy['recommended_cookies']
        counter_cookies = [c for c in self.all_cookies if c.name in recommended_names]

        # If we don't have enough counter cookies, add high-tier cookies
        if len(counter_cookies) < 20:
            high_tier = [c for c in self.all_cookies
                        if c.rarity in ['Beast', 'Ancient', 'Legendary']
                        and c not in counter_cookies]
            counter_cookies.extend(high_tier[:20 - len(counter_cookies)])

        # Generate teams using counter cookies
        if method == 'greedy':
            # Greedy approach: start with best counter cookies
            teams = []
            for _ in range(n * 3):  # Generate more than needed
                team_cookies = []

                # Add required cookies first
                if required_cookies:
                    for name in required_cookies:
                        cookie = next((c for c in self.all_cookies if c.name == name), None)
                        if cookie:
                            team_cookies.append(cookie)

                # Fill remaining slots with counter cookies
                available = [c for c in counter_cookies if c not in team_cookies]
                while len(team_cookies) < 5 and available:
                    team_cookies.append(available.pop(0))

                # If still not enough, add any high-tier cookies
                if len(team_cookies) < 5:
                    remaining = [c for c in self.all_cookies if c not in team_cookies]
                    remaining.sort(key=lambda c: self.optimizer.rarity_weights.get(c.rarity, 0), reverse=True)
                    team_cookies.extend(remaining[:5 - len(team_cookies)])

                if len(team_cookies) == 5:
                    teams.append(Team(team_cookies))

        else:
            # Use optimizer's methods but with filtered cookie pool
            original_cookies = self.optimizer.all_cookies
            self.optimizer.all_cookies = counter_cookies if counter_cookies else original_cookies

            teams = self.optimizer.find_best_teams(
                n=n * 3,
                method=method,
                required_cookies=required_cookies
            )

            self.optimizer.all_cookies = original_cookies

        # Score teams based on counter effectiveness
        scored_teams = []
        for team in teams:
            counter_score = self._calculate_counter_score(team, enemy_team, counter_strategy)

            # Get treasure recommendations for this counter team
            recommended_treasures = self.recommend_counter_treasures(enemy_team, team, counter_strategy)

            counter_info = {
                'counter_score': counter_score,
                'team_score': team.composition_score,
                'combined_score': (counter_score * 0.6) + (team.composition_score * 0.4),
                'strategy': counter_strategy['strategy_description'],
                'weaknesses_exploited': weaknesses,
                'priority_targets': counter_strategy['priority_targets'],
                'recommended_treasures': [
                    {
                        'name': t[0].name,
                        'tier': t[0].tier_ranking,
                        'score': round(t[1], 2),
                        'reason': t[2],
                        'effects': {
                            'atk_boost': t[0].atk_boost_max,
                            'crit_boost': t[0].crit_boost_max,
                            'cooldown_reduction': t[0].cooldown_reduction_max,
                            'dmg_resist': t[0].dmg_resist_max,
                            'hp_shield': t[0].hp_shield_max,
                            'heal': t[0].heal_max
                        }
                    }
                    for t in recommended_treasures
                ]
            }
            scored_teams.append((team, counter_info))

        # Sort by combined score
        scored_teams.sort(key=lambda x: x[1]['combined_score'], reverse=True)

        return scored_teams[:n]

    def _calculate_counter_score(
        self,
        counter_team: Team,
        enemy_team: Team,
        strategy: Dict
    ) -> float:
        """
        Calculate how well a team counters the enemy using ability data (0-100 score).

        Args:
            counter_team: Your counter team
            enemy_team: Enemy team to counter
            strategy: Counter strategy dict

        Returns:
            float: Counter effectiveness score (0-100)
        """
        score = 0.0
        max_score = 100.0

        # Check for recommended counter cookies (40 points max)
        recommended_count = sum(
            1 for cookie in counter_team.cookies
            if cookie.name in strategy['recommended_cookies']
        )
        score += (recommended_count / 5) * 40

        # Check if team has essential counter elements using ability data (30 points max)
        analysis = self.analyze_enemy_team(enemy_team)

        # Anti-heal if enemy has healers (10 points) - use ability data
        if analysis['healers'] >= 2:
            has_anti_heal = any(c.anti_heal for c in counter_team.cookies)
            if has_anti_heal:
                score += 10

        # Ambush or backline targeting if enemy has exposed backline (10 points)
        if analysis['rear_position'] >= 3:
            has_ambush = any(c.role == 'Ambush' or c.target_type == 'Backline' for c in counter_team.cookies)
            if has_ambush:
                score += 10

        # Defense shred/anti-tank if enemy is tank-heavy (10 points) - use ability data
        if analysis['tanks'] >= 2:
            has_def_shred = any(c.anti_tank for c in counter_team.cookies)
            if has_def_shred:
                score += 10

        # Crowd control if enemy lacks immunity (10 points) - use ability data
        if not analysis['immunity']:
            has_cc = any(c.crowd_control and c.crowd_control != 'None' for c in counter_team.cookies)
            if has_cc:
                score += 5

        # Immunity if enemy has CC (5 points) - use ability data
        if analysis['crowd_control'] >= 2:
            has_immunity = any(c.grants_immunity and c.grants_immunity != 'None' for c in counter_team.cookies)
            if has_immunity:
                score += 5

        # Team balance (15 points max)
        role_dist = counter_team.get_role_distribution()
        has_tank = any(role in role_dist for role in ['Defense', 'Charge'])
        has_healer = any(role in role_dist for role in ['Healing', 'Support'])
        has_dps = any(role in role_dist for role in ['Magic', 'Ranged', 'Bomber', 'Ambush'])

        if has_tank:
            score += 5
        if has_healer:
            score += 5
        if has_dps:
            score += 5

        # Synergy bonus (15 points max)
        if hasattr(counter_team, 'synergy_score'):
            score += (counter_team.synergy_score / 100) * 15

        return min(score, max_score)

    def explain_counter(self, counter_team: Team, enemy_team: Team) -> str:
        """
        Generate human-readable explanation of why counter-team works.

        Args:
            counter_team: Your counter team
            enemy_team: Enemy team being countered

        Returns:
            str: Detailed explanation
        """
        weaknesses = self.identify_weaknesses(enemy_team)
        strategy = self.generate_counter_strategies(enemy_team)

        explanation = f"Counter-Team Analysis\n"
        explanation += f"{'='*60}\n\n"

        # Enemy weaknesses
        explanation += f"Enemy Weaknesses Identified ({len(weaknesses)}):\n"
        for i, weakness in enumerate(weaknesses, 1):
            explanation += f"{i}. {weakness['weakness']} ({weakness['priority']} priority)\n"
            explanation += f"   → {weakness['description']}\n"
            explanation += f"   → Exploit: {weakness['exploit']}\n\n"

        # Counter strategy
        explanation += f"Counter Strategy: {strategy['team_archetype']}\n"
        explanation += f"{strategy['strategy_description']}\n\n"

        # Recommended cookies in team
        counter_cookies_used = [
            c.name for c in counter_team.cookies
            if c.name in strategy['recommended_cookies']
        ]

        if counter_cookies_used:
            explanation += f"Counter Cookies Used:\n"
            for cookie_name in counter_cookies_used:
                explanation += f"  ✓ {cookie_name}\n"
            explanation += "\n"

        # Priority targets
        if strategy['priority_targets']:
            explanation += f"Priority Targets to Eliminate:\n"
            for target in strategy['priority_targets']:
                explanation += f"  🎯 {target}\n"

        return explanation


def main():
    """Example usage of counter-team generator."""
    from team_optimizer import TeamOptimizer

    # Load cookies
    optimizer = TeamOptimizer('crk-cookies.csv')

    # Create example enemy team (healing-heavy)
    enemy_cookies = []
    for name in ['Pure Vanilla Cookie', 'Cream Ferret Cookie', 'Hollyberry Cookie',
                 'Frost Queen Cookie', 'Parfait Cookie']:
        cookie = next((c for c in optimizer.all_cookies if c.name == name), None)
        if cookie:
            enemy_cookies.append(cookie)

    if len(enemy_cookies) >= 5:
        enemy_team = Team(enemy_cookies)

        print(f"\n{'='*60}")
        print(f"Enemy Team: {', '.join([c.name for c in enemy_team.cookies])}")
        print(f"{'='*60}\n")

        # Generate counter-teams
        generator = CounterTeamGenerator(optimizer)

        # Analyze enemy
        weaknesses = generator.identify_weaknesses(enemy_team)
        print(f"Weaknesses Found: {len(weaknesses)}\n")
        for weakness in weaknesses:
            print(f"⚠️  {weakness['weakness']} ({weakness['confidence']}% confidence)")
            print(f"    {weakness['description']}")
            print(f"    Exploit: {weakness['exploit']}\n")

        # Generate counter-teams
        print(f"\n{'='*60}")
        print("Top 3 Counter-Teams:")
        print(f"{'='*60}\n")

        counter_teams = generator.find_counter_teams(enemy_team, n=3, method='greedy')

        for i, (team, info) in enumerate(counter_teams, 1):
            print(f"Counter Team #{i} (Counter Score: {info['counter_score']:.1f}/100)")
            print(f"Team: {', '.join([c.name for c in team.cookies])}")
            print(f"Strategy: {info['strategy']}")
            print(f"Combined Score: {info['combined_score']:.1f}\n")


if __name__ == '__main__':
    main()
