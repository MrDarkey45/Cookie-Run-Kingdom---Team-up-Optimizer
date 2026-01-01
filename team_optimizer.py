"""
Team Optimization Module for Cookie Run: Kingdom

This module provides classes and functions to build and optimize 5-cookie teams
based on role diversity, position coverage, and power scoring (rarity-based or
with optional level/skill stats).

Supports two modes:
- Basic Mode: Rarity-only scoring for recommended meta teams
- Advanced Mode: Personalized scoring with cookie levels, skill levels, and toppings
"""

import pandas as pd
import random
import json
from typing import List, Dict, Optional, Tuple
from collections import Counter
from cookie_analysis import load_data


# Rarity to power weight mapping (linear scale)
RARITY_WEIGHTS = {
    'Beast': 7.0,
    'Ancient (Ascended)': 6.5,
    'Ancient': 6.0,
    'Legendary': 5.0,
    'Dragon': 5.0,
    'Super Epic': 4.0,
    'Epic': 3.0,
    'Special': 2.0,
    'Rare': 1.0,
    'Common': 0.5
}


class Treasure:
    """Represents a treasure with buffs and effects for the team."""

    def __init__(
        self,
        name: str,
        rarity: str,
        activation_type: str,
        tier_ranking: str,
        effect_category: str,
        primary_effect: str,
        atk_boost_max: float = 0.0,
        crit_boost_max: float = 0.0,
        cooldown_reduction_max: float = 0.0,
        dmg_resist_max: float = 0.0,
        hp_shield_max: float = 0.0,
        heal_max: float = 0.0,
        revive: bool = False,
        debuff_cleanse: bool = False,
        enemy_debuff: bool = False,
        summon_boost: bool = False,
        recommended_archetypes: Optional[str] = None,
        cooldown_seconds: float = 0.0,
        special_condition: Optional[str] = None
    ):
        """
        Initialize a Treasure.

        Args:
            name: Treasure name
            rarity: Common, Rare, Epic, Special
            activation_type: Passive or Active
            tier_ranking: S+, S, A, B, C
            effect_category: Offensive, Defensive, Utility, Hybrid
            primary_effect: Main effect description
            atk_boost_max: Max ATK% boost (0-100)
            crit_boost_max: Max CRIT% boost (0-100)
            cooldown_reduction_max: Max cooldown reduction% (0-100)
            dmg_resist_max: Max DMG Resist% (0-100)
            hp_shield_max: Max HP Shield% (0-100)
            heal_max: Max Heal% (0-100)
            revive: Whether treasure can revive fallen cookies
            debuff_cleanse: Whether treasure cleanses debuffs
            enemy_debuff: Whether treasure applies debuffs to enemies
            summon_boost: Whether treasure boosts summoned creatures
            recommended_archetypes: Pipe-separated archetypes (e.g., "DPS|Burst|Tank")
            cooldown_seconds: Cooldown for active treasures
            special_condition: Special activation conditions or notes
        """
        self.name = name
        self.rarity = rarity
        self.activation_type = activation_type
        self.tier_ranking = tier_ranking
        self.effect_category = effect_category
        self.primary_effect = primary_effect

        # Stat bonuses (at max level)
        self.atk_boost_max = atk_boost_max
        self.crit_boost_max = crit_boost_max
        self.cooldown_reduction_max = cooldown_reduction_max
        self.dmg_resist_max = dmg_resist_max
        self.hp_shield_max = hp_shield_max
        self.heal_max = heal_max

        # Special abilities
        self.revive = revive
        self.debuff_cleanse = debuff_cleanse
        self.enemy_debuff = enemy_debuff
        self.summon_boost = summon_boost

        # Metadata
        self.recommended_archetypes = recommended_archetypes.split('|') if recommended_archetypes else []
        self.cooldown_seconds = cooldown_seconds
        self.special_condition = special_condition if special_condition != 'None' else None

    def get_power_score(self) -> float:
        """
        Calculate treasure power score based on effects.

        Returns:
            float: Power score (0-10, where 10 is maximum utility)
        """
        # Tier-based base score
        tier_scores = {'S+': 10.0, 'S': 8.5, 'A': 7.0, 'B': 5.5, 'C': 4.0}
        base_score = tier_scores.get(self.tier_ranking, 5.0)

        # Bonus for universal archetypes
        if 'Universal' in self.recommended_archetypes:
            base_score += 1.0

        return min(base_score, 10.0)

    def __repr__(self) -> str:
        return f"Treasure({self.name}, {self.tier_ranking}, {self.effect_category})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Treasure):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        """Hash based on treasure name for set operations."""
        return hash(self.name)

    def to_dict(self) -> Dict:
        """Export treasure as dictionary for JSON serialization."""
        return {
            'name': self.name,
            'rarity': self.rarity,
            'activation_type': self.activation_type,
            'tier_ranking': self.tier_ranking,
            'effect_category': self.effect_category,
            'primary_effect': self.primary_effect,
            'atk_boost': self.atk_boost_max,
            'crit_boost': self.crit_boost_max,
            'cooldown_reduction': self.cooldown_reduction_max,
            'power_score': self.get_power_score(),
            'recommended_archetypes': self.recommended_archetypes
        }


class Cookie:
    """Represents a single cookie with game attributes and optional progression stats."""

    def __init__(
        self,
        name: str,
        rarity: str,
        role: str,
        position: str,
        element: Optional[str] = None,
        cookie_level: Optional[int] = None,
        skill_level: Optional[int] = None,
        topping_quality: Optional[float] = None,
        # Ability attributes
        skill_name: Optional[str] = None,
        skill_type: Optional[str] = None,
        crowd_control: Optional[str] = None,
        grants_immunity: Optional[str] = None,
        provides_healing: bool = False,
        provides_shield: bool = False,
        anti_heal: bool = False,
        anti_tank: bool = False,
        dispel: bool = False,
        target_type: Optional[str] = None,
        key_mechanic: Optional[str] = None,
        # Guild Battle-specific attributes
        water_element: bool = False,
        aoe_damage: bool = False,
        def_shred: bool = False,
        indirect_damage: bool = False,
        attack_speed_buff: bool = False,
        shield_provider: bool = False,
        debuff_heavy: bool = False,
        # Synergy system attributes
        synergy_groups: Optional[List[str]] = None,
        special_combos: Optional[List[str]] = None
    ):
        """
        Initialize a Cookie instance.

        Args:
            name: Cookie name
            rarity: Cookie rarity tier (Common, Rare, Epic, etc.)
            role: Cookie role (Charge, Defense, Magic, Healing, etc.)
            position: Cookie position (Front, Middle, Rear)
            element: Optional cookie element (Fire, Water, Light, etc.)
            cookie_level: Optional cookie level (1-90) for advanced mode
            skill_level: Optional skill level (1-90) for advanced mode
            topping_quality: Optional topping quality rating (0-5) for advanced mode
            skill_name: Optional skill name
            skill_type: Optional skill type (Damage, Healing, Buff, etc.)
            crowd_control: Optional CC type (Stun, Freeze, Silence, None)
            grants_immunity: Optional immunity type (All_Debuffs, Stun, None)
            provides_healing: Has healing abilities
            provides_shield: Has shield abilities
            anti_heal: Has healing reduction
            anti_tank: Has HP-based or True damage
            dispel: Can remove debuffs/buffs
            target_type: Targeting (AoE, Single_Target, etc.)
            key_mechanic: Brief ability description
            water_element: Cookie has water-element attacks (for Guild Battle)
            aoe_damage: Cookie excels at AOE damage (for Guild Battle)
            def_shred: Cookie provides DEF reduction debuffs (for Guild Battle)
            indirect_damage: Cookie deals indirect damage like poison/burn (for Guild Battle)
            attack_speed_buff: Cookie provides ATK SPD buffs (for Guild Battle)
            shield_provider: Cookie provides shields to allies (for Guild Battle)
            debuff_heavy: Cookie relies heavily on debuffs (for Guild Battle)
            synergy_groups: List of synergy groups cookie belongs to (Beast, Dragon, Ancient, Citrus Squad, etc.)
            special_combos: List of special combo teams cookie can participate in
        """
        self.name = name
        self.rarity = rarity
        self.role = role
        self.position = position
        self.element = element if element and element != 'N/A' else None
        self.cookie_level = cookie_level
        self.skill_level = skill_level
        self.topping_quality = topping_quality

        # Ability attributes
        self.skill_name = skill_name
        self.skill_type = skill_type
        self.crowd_control = crowd_control if crowd_control != 'None' else None
        self.grants_immunity = grants_immunity if grants_immunity != 'None' else None
        self.provides_healing = provides_healing
        self.provides_shield = provides_shield
        self.anti_heal = anti_heal
        self.anti_tank = anti_tank
        self.dispel = dispel
        self.target_type = target_type
        self.key_mechanic = key_mechanic

        # Guild Battle-specific attributes
        self.water_element = water_element
        self.aoe_damage = aoe_damage
        self.def_shred = def_shred
        self.indirect_damage = indirect_damage
        self.attack_speed_buff = attack_speed_buff
        self.shield_provider = shield_provider
        self.debuff_heavy = debuff_heavy

        # Synergy system attributes
        self.synergy_groups = synergy_groups if synergy_groups else []
        self.special_combos = special_combos if special_combos else []

    def get_power_score(self) -> float:
        """
        Calculate and return the power score for this cookie.

        Returns:
            float: Power score (0-7 scale)
        """
        # Check if any advanced stats are provided
        if any([self.cookie_level, self.skill_level, self.topping_quality]):
            return self._calculate_advanced_score()
        else:
            # Basic mode: rarity-only
            return RARITY_WEIGHTS.get(self.rarity, 1.0)

    def _calculate_advanced_score(self) -> float:
        """
        Calculate advanced power score based on level, skill, and toppings.

        Formula:
        Power = (Rarity × 40%) + (Skill/60 × 35% × 7) + (Level/70 × 15% × 7) + (Topping/5 × 10% × 7)

        Returns:
            float: Advanced power score (0-7 scale)
        """
        # Base rarity weight (40%)
        rarity_score = RARITY_WEIGHTS.get(self.rarity, 1.0) * 0.40

        # Skill level component (35%) - most impactful
        skill_score = 0.0
        if self.skill_level is not None:
            skill_score = (self.skill_level / 60.0) * 0.35 * 7.0

        # Cookie level component (15%)
        level_score = 0.0
        if self.cookie_level is not None:
            level_score = (self.cookie_level / 70.0) * 0.15 * 7.0

        # Topping quality component (10%)
        topping_score = 0.0
        if self.topping_quality is not None:
            topping_score = (self.topping_quality / 5.0) * 0.10 * 7.0

        return rarity_score + skill_score + level_score + topping_score

    def __repr__(self) -> str:
        """String representation of the cookie."""
        power = self.get_power_score()
        level_info = ""
        if self.cookie_level or self.skill_level:
            level_info = f" [Lv{self.cookie_level or '?'}/Skill{self.skill_level or '?'}]"
        return f"{self.name} ({self.rarity}, {self.role}, {self.position}){level_info} - Power: {power:.2f}"

    def __eq__(self, other) -> bool:
        """Equality check based on cookie name to prevent duplicates."""
        if isinstance(other, Cookie):
            return self.name == other.name
        return False

    def __hash__(self) -> int:
        """Hash based on cookie name for set operations."""
        return hash(self.name)

    def to_dict(self) -> Dict:
        """Export cookie data as dictionary for JSON serialization."""
        return {
            'name': self.name,
            'rarity': self.rarity,
            'role': self.role,
            'position': self.position,
            'element': self.element,
            'cookie_level': self.cookie_level,
            'skill_level': self.skill_level,
            'topping_quality': self.topping_quality,
            'power_score': round(self.get_power_score(), 2),
            'synergy_groups': self.synergy_groups,
            'special_combos': self.special_combos
        }


class Team:
    """Represents a team of 5 cookies with up to 3 treasures, validation, and scoring."""

    def __init__(self, cookies: List[Cookie], treasures: Optional[List[Treasure]] = None, include_synergy: bool = True, strict_validation: bool = True):
        """
        Initialize a Team instance.

        Args:
            cookies: List of exactly 5 unique Cookie objects (or 1-5 if strict_validation=False)
            treasures: Optional list of up to 3 unique Treasure objects
            include_synergy: Whether to include synergy bonus in score (default: True)
            strict_validation: If True, enforce exactly 5 cookies. If False, allow 1-5 cookies (default: True)

        Raises:
            ValueError: If team doesn't have exactly 5 unique cookies (when strict) or more than 3 treasures
        """
        self.cookies = cookies
        self.treasures = treasures if treasures else []
        self.include_synergy = include_synergy
        self.strict_validation = strict_validation
        self.validate()
        self.synergy_score = 0.0
        self.synergy_breakdown = {}
        self.treasure_bonus = 0.0
        self.composition_score = self.calculate_score()

    def validate(self) -> bool:
        """
        Validate team composition including treasures.

        Returns:
            bool: True if valid

        Raises:
            ValueError: If validation fails
        """
        if self.strict_validation:
            if len(self.cookies) != 5:
                raise ValueError(f"Team must have exactly 5 cookies, got {len(self.cookies)}")
        else:
            if len(self.cookies) < 1 or len(self.cookies) > 5:
                raise ValueError(f"Team must have 1-5 cookies, got {len(self.cookies)}")

        if len(set(self.cookies)) != len(self.cookies):
            raise ValueError("Team cannot have duplicate cookies")

        if len(self.treasures) > 3:
            raise ValueError(f"Team can have maximum 3 treasures, got {len(self.treasures)}")

        if len(self.treasures) != len(set(self.treasures)):
            raise ValueError("Team cannot have duplicate treasures")

        return True

    def get_cookie_signature(self) -> frozenset:
        """
        Get a unique signature for this team based on cookie names.
        Used to identify duplicate teams regardless of order.

        Returns:
            frozenset: Immutable set of cookie names
        """
        return frozenset(cookie.name for cookie in self.cookies)

    def __eq__(self, other) -> bool:
        """Check if two teams have the same cookies (regardless of order)."""
        if isinstance(other, Team):
            return self.get_cookie_signature() == other.get_cookie_signature()
        return False

    def __hash__(self) -> int:
        """Hash based on cookie signature for set operations."""
        return hash(self.get_cookie_signature())

    def calculate_score(self) -> float:
        """
        Calculate overall team composition score.

        Score components:
        - Role Diversity: 0-30 points
        - Position Coverage: 0-25 points
        - Power Score: 0-35 points
        - Bonus Modifiers: 0-10 points
        - Synergy Bonus: 0-20 points (if enabled)
        - Treasure Bonus: 0-15 points (if treasures equipped)

        Returns:
            float: Total team score (~100-135 max with synergy and treasures)
        """
        role_score = self._calculate_role_diversity_score()
        position_score = self._calculate_position_coverage_score()
        power_score = self._calculate_power_score()
        bonus_score = self._calculate_bonus_modifiers()

        base_score = role_score + position_score + power_score + bonus_score

        # Calculate treasure bonus if treasures equipped
        treasure_bonus = self._calculate_treasure_bonus()
        self.treasure_bonus = treasure_bonus

        # Calculate synergy bonus if enabled
        if self.include_synergy:
            synergy_bonus = self._calculate_synergy_bonus()
            return base_score + treasure_bonus + synergy_bonus

        return base_score + treasure_bonus

    def _calculate_synergy_bonus(self) -> float:
        """
        Calculate synergy bonus score (0-20 points).

        Uses the synergy calculator to add bonus points based on team synergies.
        The synergy score (0-100) is scaled to 0-20 bonus points.

        Returns:
            float: Synergy bonus points (0-20)
        """
        try:
            # Lazy import to avoid circular dependency
            from synergy_calculator import SynergyCalculator

            calculator = SynergyCalculator()
            self.synergy_breakdown = calculator.calculate_team_synergy(self)
            self.synergy_score = self.synergy_breakdown['total_score']

            # Scale synergy score (0-100) to bonus points (0-20)
            return (self.synergy_score / 100.0) * 20.0

        except ImportError:
            # Synergy calculator not available, return 0
            return 0.0

    def _calculate_role_diversity_score(self) -> float:
        """Calculate role diversity score (0-30 points)."""
        unique_roles = len(set(cookie.role for cookie in self.cookies))

        role_scores = {
            5: 30,
            4: 24,
            3: 15,
            2: 8,
            1: 0
        }

        return role_scores.get(unique_roles, 0)

    def _calculate_position_coverage_score(self) -> float:
        """Calculate position coverage score (0-25 points)."""
        unique_positions = len(set(cookie.position for cookie in self.cookies))

        position_scores = {
            3: 25,  # All positions covered
            2: 15,
            1: 5
        }

        return position_scores.get(unique_positions, 0)

    def _calculate_power_score(self) -> float:
        """Calculate total power score (0-35 points)."""
        return sum(cookie.get_power_score() for cookie in self.cookies)

    def _calculate_bonus_modifiers(self) -> float:
        """Calculate bonus modifiers (0-10 points)."""
        bonus = 0.0

        # +3 for having a tank (Defense or Charge in Front)
        if self.has_tank():
            bonus += 3.0

        # +3 for having a healer (Healing or Support)
        if self.has_healer():
            bonus += 3.0

        # +2 for having damage dealers
        damage_roles = {'Magic', 'Ranged', 'Bomber', 'Ambush'}
        if any(cookie.role in damage_roles for cookie in self.cookies):
            bonus += 2.0

        return bonus

    def _calculate_treasure_bonus(self) -> float:
        """
        Calculate treasure bonus score (0-15 points).

        Treasures provide bonus points based on:
        - Treasure power scores (tier-based)
        - Stat bonuses (ATK, CRIT, cooldown reduction)
        - Special effects (revival, shields, healing)

        Returns:
            float: Treasure bonus points (0-15)
        """
        if not self.treasures or len(self.treasures) == 0:
            return 0.0

        bonus = 0.0

        # Base power score from treasures (0-10 points)
        # Average treasure power scaled to 0-10 range
        avg_treasure_power = sum(t.get_power_score() for t in self.treasures) / len(self.treasures)
        bonus += min(avg_treasure_power, 10.0)

        # Stat bonuses (0-3 points)
        total_atk_boost = sum(t.atk_boost_max for t in self.treasures)
        total_crit_boost = sum(t.crit_boost_max for t in self.treasures)
        total_cdr = sum(t.cooldown_reduction_max for t in self.treasures)

        # ATK boost contribution (up to 1 point)
        if total_atk_boost > 0:
            bonus += min(total_atk_boost / 100.0, 1.0)

        # CRIT boost contribution (up to 1 point)
        if total_crit_boost > 0:
            bonus += min(total_crit_boost / 30.0, 1.0)

        # Cooldown reduction contribution (up to 1 point)
        if total_cdr > 0:
            bonus += min(total_cdr / 40.0, 1.0)

        # Special effects bonus (0-2 points)
        special_bonus = 0.0

        # Revival treasure bonus
        if any(t.revive for t in self.treasures):
            special_bonus += 0.5

        # Debuff cleanse bonus
        if any(t.debuff_cleanse for t in self.treasures):
            special_bonus += 0.3

        # Enemy debuff bonus
        if any(t.enemy_debuff for t in self.treasures):
            special_bonus += 0.4

        # Shield/healing bonus
        total_shields = sum(t.hp_shield_max for t in self.treasures)
        total_heals = sum(t.heal_max for t in self.treasures)
        if total_shields > 0 or total_heals > 0:
            special_bonus += 0.5

        # Summon boost bonus
        if any(t.summon_boost for t in self.treasures):
            # Check if team has summoners
            has_summoner = any(
                c.skill_type == 'Summon' if hasattr(c, 'skill_type') and c.skill_type else False
                for c in self.cookies
            )
            if has_summoner:
                special_bonus += 0.8  # Big bonus if team has summoners
            else:
                special_bonus -= 0.3  # Small penalty if no summoners

        bonus += min(special_bonus, 2.0)

        return min(bonus, 15.0)

    def get_role_distribution(self) -> Dict[str, int]:
        """Get count of each role in the team."""
        return dict(Counter(cookie.role for cookie in self.cookies))

    def get_position_distribution(self) -> Dict[str, int]:
        """Get count of each position in the team."""
        return dict(Counter(cookie.position for cookie in self.cookies))

    @property
    def element_synergy_score(self) -> float:
        """
        Calculate bonus for element matching (0-15 points).
        Rewards teams with focused elemental damage.
        """
        element_counts = {}
        for cookie in self.cookies:
            if cookie.element:
                element_counts[cookie.element] = element_counts.get(cookie.element, 0) + 1

        if not element_counts:
            return 0.0

        max_same_element = max(element_counts.values())

        if max_same_element >= 3:
            return 15.0  # 3+ same element = strong elemental focus
        elif max_same_element == 2:
            return 7.0   # 2 same element = moderate focus
        else:
            return 0.0   # Diverse elements = no bonus

    @property
    def group_synergy_score(self) -> float:
        """
        Calculate bonus for synergy group matching (0-20 points).
        Rewards teams from the same group (Beast, Dragon, Ancient, etc.)
        """
        group_counts = {}
        for cookie in self.cookies:
            if cookie.synergy_groups:
                for group in cookie.synergy_groups:
                    group_counts[group] = group_counts.get(group, 0) + 1

        total_bonus = 0.0
        for group, count in group_counts.items():
            if count >= 3:
                total_bonus += 12.0  # 3+ from same group = strong synergy
            elif count == 2:
                total_bonus += 5.0   # 2 from same group = moderate synergy

        return min(20.0, total_bonus)  # Cap at 20 points

    @property
    def special_combo_score(self) -> float:
        """
        Detect special combo activation (0-25 points).
        Recognizes named team combos like Citrus Party, Silver Knighthood, etc.
        """
        combo_bonuses = {
            'Citrus Party': {
                'required': {'Lemon Cookie'},
                'optional': {'Orange Cookie', 'Lime Cookie', 'Grapefruit Cookie'},
                'min_members': 2,
                'bonus': 20.0
            },
            'The Protector of the Golden City': {
                'required': {'Golden Cheese Cookie'},
                'optional': {'Burnt Cheese Cookie', 'Smoked Cheese Cookie'},
                'min_members': 2,
                'bonus': 15.0
            },
            'Silver Knighthood': {
                'required': {'Mercurial Knight Cookie', 'Silverbell Cookie'},
                'bonus': 25.0
            },
            'Team Drizzle': {
                'required': {'Choco Drizzle Cookie', 'Green Tea Mousse Cookie', 'Pudding à la Mode Cookie'},
                'bonus': 25.0
            },
            'The Deceitful Trio': {
                'required': {'Shadow Milk Cookie', 'Black Sapphire Cookie', 'Candy Apple Cookie'},
                'bonus': 25.0
            }
        }

        cookie_names = {c.name for c in self.cookies}
        max_bonus = 0.0

        for combo_name, combo_data in combo_bonuses.items():
            required = combo_data['required']

            # Check if all required cookies are present
            if required.issubset(cookie_names):
                # Check for minimum members requirement (for combos with optional members)
                if 'min_members' in combo_data:
                    optional = combo_data.get('optional', set())
                    all_members = required | optional
                    present_members = cookie_names & all_members
                    if len(present_members) >= combo_data['min_members']:
                        max_bonus = max(max_bonus, combo_data['bonus'])
                else:
                    # All required present, activate bonus
                    max_bonus = max(max_bonus, combo_data['bonus'])

        return max_bonus

    @property
    def total_synergy_score(self) -> float:
        """
        Total synergy score from elements, groups, and special combos (0-60 points max).
        - Element synergy: 0-15
        - Group synergy: 0-20
        - Special combos: 0-25
        """
        return (
            self.element_synergy_score +
            self.group_synergy_score +
            self.special_combo_score
        )

    def has_tank(self) -> bool:
        """Check if team has a tank (Defense or Charge in Front)."""
        return any(
            cookie.position == 'Front' and cookie.role in {'Defense', 'Charge'}
            for cookie in self.cookies
        )

    def has_healer(self) -> bool:
        """Check if team has a healer (Healing or Support)."""
        return any(cookie.role in {'Healing', 'Support'} for cookie in self.cookies)

    def __repr__(self) -> str:
        """String representation of the team."""
        lines = [f"\n{'='*60}"]
        lines.append(f"Team Score: {self.composition_score:.1f}/100")
        lines.append(f"{'='*60}")

        for i, cookie in enumerate(self.cookies, 1):
            lines.append(f"{i}. {cookie}")

        lines.append(f"\nRole Distribution: {self.get_role_distribution()}")
        lines.append(f"Position Coverage: {self.get_position_distribution()}")

        tank = "✓" if self.has_tank() else "✗"
        healer = "✓" if self.has_healer() else "✗"
        lines.append(f"Has Tank: {tank} | Has Healer: {healer}")
        lines.append(f"{'='*60}")

        return "\n".join(lines)

    def to_dict(self) -> Dict:
        """Export team data as dictionary for JSON serialization."""
        result = {
            'score': round(self.composition_score, 2),
            'cookies': [cookie.to_dict() for cookie in self.cookies],
            'role_distribution': self.get_role_distribution(),
            'position_distribution': self.get_position_distribution(),
            'has_tank': self.has_tank(),
            'has_healer': self.has_healer()
        }

        # Include treasure data if available
        if self.treasures and len(self.treasures) > 0:
            result['treasures'] = [treasure.to_dict() for treasure in self.treasures]
            result['treasure_bonus'] = round(self.treasure_bonus, 2)

        # Include synergy data if available
        if self.include_synergy and self.synergy_breakdown:
            result['synergy'] = {
                'total_score': round(self.synergy_score, 2),
                'breakdown': {
                    'role_synergy': round(self.synergy_breakdown.get('role_synergy', 0), 2),
                    'position_synergy': round(self.synergy_breakdown.get('position_synergy', 0), 2),
                    'element_synergy': round(self.synergy_breakdown.get('element_synergy', 0), 2),
                    'type_synergy': round(self.synergy_breakdown.get('type_synergy', 0), 2),
                    'coverage_synergy': round(self.synergy_breakdown.get('coverage_synergy', 0), 2)
                }
            }

        # Always include new synergy scores
        result['advanced_synergy'] = {
            'total_synergy': round(self.total_synergy_score, 2),
            'element_synergy': round(self.element_synergy_score, 2),
            'group_synergy': round(self.group_synergy_score, 2),
            'special_combo': round(self.special_combo_score, 2)
        }

        return result


class TeamOptimizer:
    """Main class for generating and ranking team compositions."""

    def __init__(self, csv_filepath: str, treasures_filepath: str = 'crk_treasures.csv'):
        """
        Initialize TeamOptimizer with cookie and treasure data.

        Args:
            csv_filepath: Path to the cookie CSV file
            treasures_filepath: Path to the treasures CSV file (default: 'crk_treasures.csv')
        """
        # Store the base directory for loading auxiliary files
        import os
        self.base_dir = os.path.dirname(os.path.abspath(csv_filepath))

        self.cookies_df = load_data(csv_filepath)
        if self.cookies_df is None:
            raise ValueError(f"Failed to load data from {csv_filepath}")

        self.rarity_weights = RARITY_WEIGHTS
        self.all_cookies = self.load_cookies()
        self.all_treasures = self.load_treasures(treasures_filepath)

        print(f"Loaded {len(self.all_cookies)} cookies for team optimization")
        print(f"Loaded {len(self.all_treasures)} treasures")

    def _load_synergy_data(self) -> Dict:
        """
        Load synergy data from JSON file.

        Returns:
            Dict: Synergy data with elements, synergy_groups, and special_combos
        """
        try:
            import os
            synergy_path = os.path.join(self.base_dir, 'cookie_synergy_data.json')
            with open(synergy_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: cookie_synergy_data.json not found. Cookies will have no synergy data.")
            return {'elements': {}, 'synergy_groups': {}, 'special_combos': {}}
        except json.JSONDecodeError as e:
            print(f"Error parsing synergy data: {e}")
            return {'elements': {}, 'synergy_groups': {}, 'special_combos': {}}

    def load_cookies(self) -> List[Cookie]:
        """
        Convert DataFrame to Cookie objects with ability data merged.

        Returns:
            List[Cookie]: List of all available cookies
        """
        cookies = []

        # Load synergy data
        synergy_data = self._load_synergy_data()

        # Load ability data from separate CSV
        try:
            import os
            abilities_path = os.path.join(self.base_dir, 'cookie_abilities.csv')
            abilities_df = pd.read_csv(abilities_path)

            # Merge ability data with main cookie data on cookie_name
            merged_df = self.cookies_df.merge(
                abilities_df,
                on='cookie_name',
                how='left'
            )
        except FileNotFoundError:
            # If ability file doesn't exist, use main data only
            print("Warning: cookie_abilities.csv not found. Loading cookies without ability data.")
            merged_df = self.cookies_df

        for _, row in merged_df.iterrows():
            # Skip cookies with missing critical data
            if pd.isna(row['cookie_name']) or pd.isna(row['cookie_rarity']):
                continue

            # Extract element from CSV first, then override with synergy data if available
            element = None
            if 'cookie_element' in row and not pd.isna(row['cookie_element']) and row['cookie_element'] != 'N/A':
                element = row['cookie_element']

            # Override with synergy data if available
            cookie_name = row['cookie_name']
            if cookie_name in synergy_data.get('elements', {}):
                element = synergy_data['elements'][cookie_name]

            # Get synergy groups and special combos
            synergy_groups = synergy_data.get('synergy_groups', {}).get(cookie_name, [])
            special_combos = synergy_data.get('special_combos', {}).get(cookie_name, [])

            # Extract ability attributes if available
            skill_name = row.get('skill_name') if 'skill_name' in row and not pd.isna(row.get('skill_name')) else None
            skill_type = row.get('skill_type') if 'skill_type' in row and not pd.isna(row.get('skill_type')) else None
            crowd_control = row.get('crowd_control') if 'crowd_control' in row and not pd.isna(row.get('crowd_control')) else None
            grants_immunity = row.get('grants_immunity') if 'grants_immunity' in row and not pd.isna(row.get('grants_immunity')) else None
            target_type = row.get('target_type') if 'target_type' in row and not pd.isna(row.get('target_type')) else None
            key_mechanic = row.get('key_mechanic') if 'key_mechanic' in row and not pd.isna(row.get('key_mechanic')) else None

            # Convert boolean strings to actual booleans
            provides_healing = False
            if 'provides_healing' in row and not pd.isna(row.get('provides_healing')):
                provides_healing = str(row['provides_healing']).lower() == 'true'

            provides_shield = False
            if 'provides_shield' in row and not pd.isna(row.get('provides_shield')):
                provides_shield = str(row['provides_shield']).lower() == 'true'

            anti_heal = False
            if 'anti_heal' in row and not pd.isna(row.get('anti_heal')):
                anti_heal = str(row['anti_heal']).lower() == 'true'

            anti_tank = False
            if 'anti_tank' in row and not pd.isna(row.get('anti_tank')):
                anti_tank = str(row['anti_tank']).lower() == 'true'

            dispel = False
            if 'dispel' in row and not pd.isna(row.get('dispel')):
                dispel = str(row['dispel']).lower() == 'true'

            # Auto-detect Guild Battle attributes
            water_element = element and 'water' in element.lower() if element else False
            aoe_damage = target_type == 'AoE' if target_type else False
            def_shred = row['cookie_name'] in [
                'Dark Choco Cookie', 'Candy Apple Cookie', 'Black Lemonade Cookie',
                'Eclair Cookie', 'Affogato Cookie'
            ]
            indirect_damage = anti_heal or ('poison' in key_mechanic.lower() if key_mechanic else False) or ('burn' in key_mechanic.lower() if key_mechanic else False)
            attack_speed_buff = row['cookie_name'] in [
                'Mint Choco Cookie', 'Star Coral Cookie', 'Cotton Cookie',
                'Financier Cookie'
            ]
            shield_provider = provides_shield
            debuff_heavy = row['cookie_name'] in [
                'Black Raisin Cookie', 'Captain Caviar Cookie', 'Linzer Cookie',
                'Affogato Cookie', 'Eclair Cookie'
            ]

            cookie = Cookie(
                name=row['cookie_name'],
                rarity=row['cookie_rarity'],
                role=row['cookie_role'] if not pd.isna(row['cookie_role']) else 'Unknown',
                position=row['cookie_position'] if not pd.isna(row['cookie_position']) else 'Middle',
                element=element,
                skill_name=skill_name,
                skill_type=skill_type,
                crowd_control=crowd_control,
                grants_immunity=grants_immunity,
                provides_healing=provides_healing,
                provides_shield=provides_shield,
                anti_heal=anti_heal,
                anti_tank=anti_tank,
                dispel=dispel,
                target_type=target_type,
                key_mechanic=key_mechanic,
                water_element=water_element,
                aoe_damage=aoe_damage,
                def_shred=def_shred,
                indirect_damage=indirect_damage,
                attack_speed_buff=attack_speed_buff,
                shield_provider=shield_provider,
                debuff_heavy=debuff_heavy,
                synergy_groups=synergy_groups,
                special_combos=special_combos
            )
            cookies.append(cookie)

        return cookies

    def load_treasures(self, treasures_filepath: str) -> List[Treasure]:
        """
        Load treasures from CSV file.

        Args:
            treasures_filepath: Path to treasures CSV file

        Returns:
            List[Treasure]: List of all available treasures
        """
        treasures = []

        try:
            import os
            # If path is not absolute, make it relative to base_dir
            if not os.path.isabs(treasures_filepath):
                treasures_filepath = os.path.join(self.base_dir, treasures_filepath)
            treasures_df = pd.read_csv(treasures_filepath)

            for _, row in treasures_df.iterrows():
                # Skip treasures with missing critical data
                if pd.isna(row.get('treasure_name')):
                    continue

                # Convert boolean strings to actual booleans
                revive = str(row.get('revive', 'False')).lower() == 'true'
                debuff_cleanse = str(row.get('debuff_cleanse', 'False')).lower() == 'true'
                enemy_debuff = str(row.get('enemy_debuff', 'False')).lower() == 'true'
                summon_boost = str(row.get('summon_boost', 'False')).lower() == 'true'

                treasure = Treasure(
                    name=row['treasure_name'],
                    rarity=row.get('rarity', 'Common'),
                    activation_type=row.get('activation_type', 'Passive'),
                    tier_ranking=row.get('tier_ranking', 'C'),
                    effect_category=row.get('effect_category', 'Offensive'),
                    primary_effect=row.get('primary_effect', ''),
                    atk_boost_max=float(row.get('atk_boost_max', 0.0)),
                    crit_boost_max=float(row.get('crit_boost_max', 0.0)),
                    cooldown_reduction_max=float(row.get('cooldown_reduction_max', 0.0)),
                    dmg_resist_max=float(row.get('dmg_resist_max', 0.0)),
                    hp_shield_max=float(row.get('hp_shield_max', 0.0)),
                    heal_max=float(row.get('heal_max', 0.0)),
                    revive=revive,
                    debuff_cleanse=debuff_cleanse,
                    enemy_debuff=enemy_debuff,
                    summon_boost=summon_boost,
                    recommended_archetypes=row.get('recommended_archetypes', ''),
                    cooldown_seconds=float(row.get('cooldown_seconds', 0.0)),
                    special_condition=row.get('special_condition', 'None')
                )
                treasures.append(treasure)

        except FileNotFoundError:
            print(f"Warning: {treasures_filepath} not found. No treasures loaded.")
        except Exception as e:
            print(f"Error loading treasures: {e}")

        return treasures

    def update_cookie_stats(self, cookie_stats: Dict[str, Dict[str, float]]):
        """
        Update cookie progression stats (levels, skills, toppings).

        Args:
            cookie_stats: Dictionary mapping cookie names to their stats
                         Format: {
                             "Cookie Name": {
                                 "cookie_level": 70,
                                 "skill_level": 60,
                                 "topping_quality": 5.0
                             }
                         }
        """
        for cookie in self.all_cookies:
            if cookie.name in cookie_stats:
                stats = cookie_stats[cookie.name]
                cookie.cookie_level = stats.get('cookie_level')
                cookie.skill_level = stats.get('skill_level')
                cookie.topping_quality = stats.get('topping_quality')

    def generate_random_teams(self, n: int = 100, required_cookies: Optional[List[str]] = None) -> List[Team]:
        """
        Generate N random valid teams.

        Args:
            n: Number of teams to generate
            required_cookies: Optional list of cookie names that MUST be in every team

        Returns:
            List[Team]: List of generated teams
        """
        teams = []

        # Get required cookie objects
        required = []
        if required_cookies:
            required = [c for c in self.all_cookies if c.name in required_cookies]
            if len(required) != len(required_cookies):
                missing = set(required_cookies) - {c.name for c in required}
                raise ValueError(f"Required cookies not found: {missing}")

        # Get available cookies for random selection (exclude required ones)
        available = [c for c in self.all_cookies if c.name not in (required_cookies or [])]

        # Calculate how many more cookies needed
        slots_to_fill = 5 - len(required)

        if slots_to_fill < 0:
            raise ValueError(f"Too many required cookies: {len(required)}. Maximum is 5.")
        if slots_to_fill > len(available):
            raise ValueError(f"Not enough cookies to fill team. Need {slots_to_fill}, have {len(available)}.")

        for _ in range(n):
            # Start with required cookies
            selected_cookies = required.copy()

            # Fill remaining slots with random selection
            if slots_to_fill > 0:
                selected_cookies.extend(random.sample(available, slots_to_fill))

            try:
                team = Team(selected_cookies)
                teams.append(team)
            except ValueError:
                # Skip invalid teams (shouldn't happen with random.sample)
                continue

        return teams

    def find_best_teams(
        self,
        n: int = 10,
        method: str = 'random',
        num_candidates: int = 1000,
        required_cookies: Optional[List[str]] = None
    ) -> List[Team]:
        """
        Find the top N best teams.

        Args:
            n: Number of top teams to return
            method: Generation method ('random', 'greedy', 'genetic', 'synergy', or 'exhaustive')
            num_candidates: Number of candidate teams to generate (for random/greedy/genetic/synergy methods)
            required_cookies: Optional list of cookie names that MUST be in the team

        Returns:
            List[Team]: Top N teams sorted by score (highest first)
        """
        if method == 'random':
            teams = self.generate_random_teams(num_candidates, required_cookies=required_cookies)
        elif method == 'greedy':
            teams = self._generate_greedy_teams(n * 10, required_cookies=required_cookies)
        elif method == 'genetic':
            teams = self._generate_genetic_teams(num_candidates, required_cookies=required_cookies)
        elif method == 'synergy':
            teams = self._generate_synergy_teams(num_candidates, required_cookies=required_cookies)
        elif method == 'exhaustive':
            teams = self._generate_exhaustive_teams(required_cookies=required_cookies)
        else:
            raise ValueError(f"Unknown method: {method}. Use 'random', 'greedy', 'genetic', 'synergy', or 'exhaustive'")

        # Remove duplicate teams (same cookies, different order)
        unique_teams = list(set(teams))

        # Sort by score descending and return top N
        # For synergy method, prioritize total_synergy_score, then composition_score
        if method == 'synergy':
            unique_teams.sort(key=lambda t: (t.total_synergy_score, t.composition_score), reverse=True)
        else:
            unique_teams.sort(key=lambda t: t.composition_score, reverse=True)
        return unique_teams[:n]

    def _generate_greedy_teams(self, n: int, required_cookies: Optional[List[str]] = None) -> List[Team]:
        """
        Generate teams using greedy approach (start with highest-rarity cookies).

        Args:
            n: Number of teams to generate
            required_cookies: Optional list of cookie names that MUST be in every team

        Returns:
            List[Team]: Generated teams
        """
        # Get required cookie objects
        required = []
        if required_cookies:
            required = [c for c in self.all_cookies if c.name in required_cookies]

        # Sort cookies by power score descending
        sorted_cookies = sorted(self.all_cookies, key=lambda c: c.get_power_score(), reverse=True)

        # Remove required cookies from sorted list to avoid duplicates
        available_sorted = [c for c in sorted_cookies if c not in required]

        teams = []
        slots_to_fill = 5 - len(required)

        for _ in range(n):
            # Start with required cookies
            team_cookies = required.copy()

            if slots_to_fill > 0:
                # Pick one high-power cookie from top 10
                if len(available_sorted) >= 10:
                    team_cookies.append(random.choice(available_sorted[:10]))
                else:
                    team_cookies.append(random.choice(available_sorted[:max(1, len(available_sorted))]))

                # Fill remaining slots with random selection from top 50%
                remaining = [c for c in available_sorted if c not in team_cookies][:len(available_sorted)//2]
                needed = min(slots_to_fill - 1, len(remaining))
                if needed > 0:
                    team_cookies.extend(random.sample(remaining, needed))

            if len(team_cookies) == 5:
                try:
                    teams.append(Team(team_cookies))
                except ValueError:
                    continue

        return teams

    def _generate_genetic_teams(
        self,
        generations: int = 100,
        population_size: int = 50,
        required_cookies: Optional[List[str]] = None
    ) -> List[Team]:
        """
        Generate teams using genetic algorithm (evolutionary approach).

        Args:
            generations: Number of generations to evolve (default: 100)
            population_size: Size of population per generation (default: 50)
            required_cookies: Optional list of cookie names that MUST be in every team

        Returns:
            List[Team]: All teams from final generation
        """
        # Initialize population with random teams
        population = self.generate_random_teams(population_size, required_cookies=required_cookies)

        for generation in range(generations):
            # Sort by fitness (team score)
            population.sort(key=lambda t: t.composition_score, reverse=True)

            # Keep top 20% as elites
            elite_count = max(2, population_size // 5)
            elites = population[:elite_count]

            # Create next generation
            next_generation = elites.copy()

            # Breed new teams from elites
            while len(next_generation) < population_size:
                # Select two random parents from elites
                parent1, parent2 = random.sample(elites, 2)

                # Crossover: combine cookies from both parents
                child_cookies = self._crossover_teams(
                    parent1, parent2, required_cookies=required_cookies
                )

                # Mutation: randomly replace a cookie (10% chance)
                if random.random() < 0.1:
                    child_cookies = self._mutate_team(child_cookies, required_cookies=required_cookies)

                try:
                    child_team = Team(child_cookies)
                    next_generation.append(child_team)
                except ValueError:
                    # Invalid team, skip
                    continue

            population = next_generation

        return population

    def _crossover_teams(
        self,
        team1: Team,
        team2: Team,
        required_cookies: Optional[List[str]] = None
    ) -> List[Cookie]:
        """
        Crossover operation: combine cookies from two parent teams.

        Args:
            team1: First parent team
            team2: Second parent team
            required_cookies: Cookies that must be in the result

        Returns:
            List[Cookie]: Child cookie combination
        """
        # Get required cookies
        required = []
        if required_cookies:
            required = [c for c in team1.cookies if c.name in required_cookies]

        # Combine cookies from both parents
        all_parent_cookies = list(set(team1.cookies + team2.cookies))

        # Remove required cookies from selection pool
        available = [c for c in all_parent_cookies if c not in required]

        # Calculate slots to fill
        slots_to_fill = 5 - len(required)

        # Randomly select from combined parent cookies
        if len(available) >= slots_to_fill:
            selected = random.sample(available, slots_to_fill)
        else:
            # Not enough cookies from parents, add random ones
            selected = available.copy()
            remaining_slots = slots_to_fill - len(selected)
            extra_cookies = [c for c in self.all_cookies if c not in selected and c not in required]
            selected.extend(random.sample(extra_cookies, remaining_slots))

        return required + selected

    def _mutate_team(
        self,
        cookies: List[Cookie],
        required_cookies: Optional[List[str]] = None
    ) -> List[Cookie]:
        """
        Mutation operation: randomly replace one cookie (not required ones).

        Args:
            cookies: Current cookie list
            required_cookies: Cookies that cannot be mutated

        Returns:
            List[Cookie]: Mutated cookie list
        """
        # Identify which cookies can be mutated
        mutable_cookies = [c for c in cookies if not required_cookies or c.name not in required_cookies]

        if not mutable_cookies:
            return cookies  # All cookies are required, can't mutate

        # Pick a random cookie to replace
        to_replace = random.choice(mutable_cookies)

        # Find a replacement cookie not already in team
        available = [c for c in self.all_cookies if c not in cookies]

        if not available:
            return cookies  # No alternatives available

        replacement = random.choice(available)

        # Create new list with replacement
        new_cookies = [replacement if c == to_replace else c for c in cookies]

        return new_cookies

    def _generate_exhaustive_teams(self, required_cookies: Optional[List[str]] = None) -> List[Team]:
        """
        Generate ALL possible team combinations (exhaustive search).

        WARNING: This can be VERY slow! Only use with small cookie pools or required cookies.
        With 177 cookies and no requirements: C(177,5) = 138,313,260 combinations!

        Args:
            required_cookies: Optional list of cookie names that MUST be in every team

        Returns:
            List[Team]: All valid teams
        """
        from itertools import combinations

        # Get required cookies
        required = []
        if required_cookies:
            required = [c for c in self.all_cookies if c.name in required_cookies]

        # Get available cookies for combinations
        available = [c for c in self.all_cookies if c not in required]

        # Calculate slots to fill
        slots_to_fill = 5 - len(required)

        # Estimate total combinations
        from math import comb
        total_combos = comb(len(available), slots_to_fill)

        if total_combos > 1_000_000:
            print(f"⚠️  WARNING: Exhaustive search will generate {total_combos:,} teams!")
            print(f"   This may take a VERY long time and use significant memory.")
            response = input("   Continue? (yes/no): ")
            if response.lower() != 'yes':
                print("   Exhaustive search cancelled.")
                return []

        print(f"Generating {total_combos:,} team combinations...")

        teams = []
        for combo in combinations(available, slots_to_fill):
            team_cookies = required + list(combo)
            try:
                team = Team(team_cookies)
                teams.append(team)
            except ValueError:
                continue

        print(f"✅ Generated {len(teams):,} valid teams")
        return teams

    def _generate_synergy_teams(
        self,
        n: int = 100,
        required_cookies: Optional[List[str]] = None
    ) -> List[Team]:
        """
        Generate teams optimized for synergy bonuses.

        This method prioritizes:
        1. Special combos (Citrus Party, Silver Knighthood, etc.)
        2. Synergy groups (Beast, Dragon, Ancient, Kingdom affiliations)
        3. Element matching (focused elemental damage)

        Args:
            n: Number of teams to generate
            required_cookies: Optional list of cookie names that MUST be in every team

        Returns:
            List[Team]: Teams optimized for synergy
        """
        teams = []
        used_combinations = set()

        # Get required cookies
        required = []
        if required_cookies:
            required = [c for c in self.all_cookies if c.name in required_cookies]

        # Strategy 1: Build teams around special combos
        special_combo_teams = self._build_special_combo_teams(required, n // 3)
        teams.extend(special_combo_teams)

        # Track used combinations
        for team in teams:
            combo_key = tuple(sorted([c.name for c in team.cookies]))
            used_combinations.add(combo_key)

        # Strategy 2: Build teams around synergy groups
        group_teams = self._build_synergy_group_teams(required, n // 3, used_combinations)
        teams.extend(group_teams)

        # Update used combinations
        for team in teams:
            combo_key = tuple(sorted([c.name for c in team.cookies]))
            used_combinations.add(combo_key)

        # Strategy 3: Build teams around element matching
        element_teams = self._build_element_teams(required, n // 3, used_combinations)
        teams.extend(element_teams)

        # Fill remaining slots with high-synergy random teams
        attempts = 0
        max_attempts = n * 10
        while len(teams) < n and attempts < max_attempts:
            team_cookies = required.copy()
            available = [c for c in self.all_cookies if c not in team_cookies]

            # Weighted selection favoring cookies with more synergy attributes
            weights = [
                1 + len(c.synergy_groups) * 2 + len(c.special_combos) * 3
                for c in available
            ]

            slots_to_fill = 5 - len(required)
            if len(available) >= slots_to_fill:
                selected = random.choices(available, weights=weights, k=slots_to_fill)
                team_cookies.extend(selected)

                # Check for duplicates
                combo_key = tuple(sorted([c.name for c in team_cookies]))
                if combo_key not in used_combinations:
                    try:
                        team = Team(team_cookies)
                        teams.append(team)
                        used_combinations.add(combo_key)
                    except ValueError:
                        pass

            attempts += 1

        return teams

    def _build_special_combo_teams(
        self,
        required: List[Cookie],
        target_count: int,
        used_combinations: Optional[set] = None
    ) -> List[Team]:
        """Build teams around special combos like Citrus Party, Team Drizzle, etc."""
        if used_combinations is None:
            used_combinations = set()

        teams = []

        # Define special combo requirements
        special_combos = {
            'Citrus Party': ['Lemon Cookie', 'Orange Cookie', 'Lime Cookie', 'Grapefruit Cookie'],
            'The Protector of the Golden City': ['Golden Cheese Cookie', 'Burnt Cheese Cookie', 'Smoked Cheese Cookie'],
            'Silver Knighthood': ['Mercurial Knight Cookie', 'Silverbell Cookie'],
            'Team Drizzle': ['Choco Drizzle Cookie', 'Green Tea Mousse Cookie', 'Pudding à la Mode Cookie'],
            'The Deceitful Trio': ['Shadow Milk Cookie', 'Black Sapphire Cookie', 'Candy Apple Cookie']
        }

        for combo_name, combo_members in special_combos.items():
            # Get available combo member cookies
            combo_cookies = [c for c in self.all_cookies if c.name in combo_members]

            if not combo_cookies:
                continue

            # Try to build teams with this combo
            attempts = 0
            while len(teams) < target_count and attempts < target_count * 3:
                team_cookies = required.copy()

                # Add combo members (at least 2-3)
                min_members = min(3, len(combo_cookies))
                combo_sample = random.sample(combo_cookies, min(min_members, len(combo_cookies)))
                team_cookies.extend([c for c in combo_sample if c not in team_cookies])

                # Fill remaining slots
                slots_remaining = 5 - len(team_cookies)
                if slots_remaining > 0:
                    available = [c for c in self.all_cookies if c not in team_cookies]
                    if len(available) >= slots_remaining:
                        team_cookies.extend(random.sample(available, slots_remaining))

                if len(team_cookies) == 5:
                    combo_key = tuple(sorted([c.name for c in team_cookies]))
                    if combo_key not in used_combinations:
                        try:
                            team = Team(team_cookies)
                            teams.append(team)
                            used_combinations.add(combo_key)
                        except ValueError:
                            pass

                attempts += 1

        return teams

    def _build_synergy_group_teams(
        self,
        required: List[Cookie],
        target_count: int,
        used_combinations: Optional[set] = None
    ) -> List[Team]:
        """Build teams around synergy groups (Beast, Dragon, Ancient, Kingdoms, etc.)."""
        if used_combinations is None:
            used_combinations = set()

        teams = []

        # Get all unique synergy groups
        all_groups = set()
        for cookie in self.all_cookies:
            all_groups.update(cookie.synergy_groups)

        for group in all_groups:
            # Get cookies in this group
            group_cookies = [c for c in self.all_cookies if group in c.synergy_groups]

            if len(group_cookies) < 2:
                continue

            # Try to build teams with 3+ from this group
            attempts = 0
            while len(teams) < target_count and attempts < target_count * 2:
                team_cookies = required.copy()

                # Add 3+ cookies from this group
                min_group_members = min(3, len(group_cookies))
                group_sample = random.sample(
                    [c for c in group_cookies if c not in team_cookies],
                    min(min_group_members, len([c for c in group_cookies if c not in team_cookies]))
                )
                team_cookies.extend(group_sample)

                # Fill remaining slots
                slots_remaining = 5 - len(team_cookies)
                if slots_remaining > 0:
                    available = [c for c in self.all_cookies if c not in team_cookies]
                    if len(available) >= slots_remaining:
                        team_cookies.extend(random.sample(available, slots_remaining))

                if len(team_cookies) == 5:
                    combo_key = tuple(sorted([c.name for c in team_cookies]))
                    if combo_key not in used_combinations:
                        try:
                            team = Team(team_cookies)
                            teams.append(team)
                            used_combinations.add(combo_key)
                        except ValueError:
                            pass

                attempts += 1

        return teams

    def _build_element_teams(
        self,
        required: List[Cookie],
        target_count: int,
        used_combinations: Optional[set] = None
    ) -> List[Team]:
        """Build teams with focused elemental damage (3+ same element)."""
        if used_combinations is None:
            used_combinations = set()

        teams = []

        # Get all unique elements
        all_elements = set(c.element for c in self.all_cookies if c.element)

        for element in all_elements:
            # Get cookies with this element
            element_cookies = [c for c in self.all_cookies if c.element == element]

            if len(element_cookies) < 3:
                continue

            # Try to build teams with 3+ of this element
            attempts = 0
            while len(teams) < target_count and attempts < target_count * 2:
                team_cookies = required.copy()

                # Add 3+ cookies with this element
                element_sample = random.sample(
                    [c for c in element_cookies if c not in team_cookies],
                    min(3, len([c for c in element_cookies if c not in team_cookies]))
                )
                team_cookies.extend(element_sample)

                # Fill remaining slots
                slots_remaining = 5 - len(team_cookies)
                if slots_remaining > 0:
                    available = [c for c in self.all_cookies if c not in team_cookies]
                    if len(available) >= slots_remaining:
                        team_cookies.extend(random.sample(available, slots_remaining))

                if len(team_cookies) == 5:
                    combo_key = tuple(sorted([c.name for c in team_cookies]))
                    if combo_key not in used_combinations:
                        try:
                            team = Team(team_cookies)
                            teams.append(team)
                            used_combinations.add(combo_key)
                        except ValueError:
                            pass

                attempts += 1

        return teams

    def filter_by_role(self, role: str) -> List[Cookie]:
        """Get all cookies with a specific role."""
        return [c for c in self.all_cookies if c.role == role]

    def filter_by_position(self, position: str) -> List[Cookie]:
        """Get all cookies at a specific position."""
        return [c for c in self.all_cookies if c.position == position]

    def recommend_treasures(self, team: Team, top_n: int = 3) -> List[Tuple[Treasure, float, str]]:
        """
        Recommend treasures for a team based on team composition and treasure synergies.

        Args:
            team: Team to recommend treasures for
            top_n: Number of treasure recommendations to return (default: 3)

        Returns:
            List of (Treasure, score, reason) tuples sorted by score
        """
        treasure_scores = []

        for treasure in self.all_treasures:
            score = 0.0
            reasons = []

            # Base score from tier ranking
            tier_base = {'S+': 10.0, 'S': 8.0, 'A': 6.0, 'B': 4.0, 'C': 2.0}
            score += tier_base.get(treasure.tier_ranking, 2.0)

            # Check archetype compatibility
            role_dist = team.get_role_distribution()
            team_archetypes = set()

            # Determine team archetypes
            if any(role in role_dist for role in ['Magic', 'Ranged', 'Bomber', 'Ambush']):
                team_archetypes.add('DPS')
            if any(role in role_dist for role in ['Defense', 'Charge']):
                team_archetypes.add('Tank')
            if any(role in role_dist for role in ['Healing', 'Support']):
                team_archetypes.add('Sustain')

            # Check for summoners
            if any(c.skill_type == 'Summon' if hasattr(c, 'skill_type') and c.skill_type else False for c in team.cookies):
                team_archetypes.add('Summoner')

            # Universal treasures get bonus for any team
            if 'Universal' in treasure.recommended_archetypes:
                score += 5.0
                reasons.append("Universal treasure (works with any team)")

            # Archetype matching bonus
            matching_archetypes = set(treasure.recommended_archetypes) & team_archetypes
            if matching_archetypes:
                score += len(matching_archetypes) * 2.0
                reasons.append(f"Matches team archetypes: {', '.join(matching_archetypes)}")

            # Summoner synergy (critical for summoner teams)
            if treasure.summon_boost:
                if 'Summoner' in team_archetypes:
                    score += 8.0  # Huge bonus for summoner teams
                    reasons.append("ESSENTIAL for summoner team")
                else:
                    score -= 5.0  # Penalty if no summoners

            # Revival synergy for squishy teams
            if treasure.revive:
                rear_count = sum(1 for c in team.cookies if c.position == 'Rear')
                if rear_count >= 3:
                    score += 4.0
                    reasons.append("Revival protects vulnerable backline")

            # Healing/Shield synergy
            has_healer = any(c.provides_healing if hasattr(c, 'provides_healing') else False for c in team.cookies)
            if treasure.hp_shield_max > 0 or treasure.heal_max > 0:
                if has_healer:
                    score += 3.0
                    reasons.append("Stacks with team's existing sustain")

            # Offensive synergy
            if treasure.atk_boost_max > 0 or treasure.crit_boost_max > 0:
                if 'DPS' in team_archetypes:
                    score += 3.0
                    reasons.append("Amplifies team damage output")

            # Cooldown reduction (universally valuable)
            if treasure.cooldown_reduction_max > 0:
                score += 4.0
                reasons.append("Faster skill rotation for all cookies")

            # Compile final recommendation
            reason = reasons[0] if reasons else "Standard treasure"
            treasure_scores.append((treasure, score, reason))

        # Sort by score and return top N
        treasure_scores.sort(key=lambda x: x[1], reverse=True)
        return treasure_scores[:top_n]

    def export_teams(self, teams: List[Team], filepath: str, format: str = 'json'):
        """
        Export teams to a file.

        Args:
            teams: List of teams to export
            filepath: Output file path
            format: Export format ('json' or 'csv')
        """
        if format == 'json':
            data = {
                'teams': [team.to_dict() for team in teams],
                'total_teams': len(teams)
            }

            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"Exported {len(teams)} teams to {filepath}")

        elif format == 'csv':
            # Flatten team data for CSV
            rows = []
            for i, team in enumerate(teams, 1):
                row = {
                    'team_number': i,
                    'score': team.composition_score,
                    'has_tank': team.has_tank(),
                    'has_healer': team.has_healer()
                }
                # Add cookie names
                for j, cookie in enumerate(team.cookies, 1):
                    row[f'cookie_{j}'] = cookie.name
                    row[f'cookie_{j}_role'] = cookie.role
                    row[f'cookie_{j}_power'] = cookie.get_power_score()

                rows.append(row)

            df = pd.DataFrame(rows)
            df.to_csv(filepath, index=False)
            print(f"Exported {len(teams)} teams to {filepath}")

        else:
            raise ValueError(f"Unknown format: {format}. Use 'json' or 'csv'")


def main():
    """Main function for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Cookie Run: Kingdom Team Optimizer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 1000 random teams
  python team_optimizer.py --method random --generate 1000 --top 5

  # Use genetic algorithm (100 generations)
  python team_optimizer.py --method genetic --generate 100 --top 10

  # Build team around specific cookie
  python team_optimizer.py --require "Shadow Milk Cookie" --top 5

  # Build team around multiple cookies
  python team_optimizer.py --require "Pure Vanilla Cookie,Dark Cacao Cookie" --top 5

  # Exhaustive search with required cookies (fast with 3+ required)
  python team_optimizer.py --method exhaustive --require "Shadow Milk Cookie,Pure Vanilla Cookie,Dark Cacao Cookie"
        """
    )
    parser.add_argument('--csv', default='crk-cookies.csv', help='Path to cookie CSV file')
    parser.add_argument('--generate', type=int, default=1000, help='Number of candidate teams/generations to generate')
    parser.add_argument('--top', type=int, default=10, help='Number of top teams to show')
    parser.add_argument('--method', choices=['random', 'greedy', 'genetic', 'exhaustive'], default='random',
                        help='Team generation method')
    parser.add_argument('--require', help='Comma-separated list of cookie names that MUST be in every team')
    parser.add_argument('--export', help='Export results to file (JSON or CSV)')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Export format')

    args = parser.parse_args()

    print("="*70)
    print("Cookie Run: Kingdom Team Optimizer")
    print("="*70)

    # Initialize optimizer
    optimizer = TeamOptimizer(args.csv)

    # Parse required cookies
    required_cookies = None
    if args.require:
        required_cookies = [name.strip() for name in args.require.split(',')]
        print(f"\n🔒 Required cookies: {', '.join(required_cookies)}")

    # Find best teams
    if args.method == 'genetic':
        print(f"\n🧬 Evolving teams using genetic algorithm ({args.generate} generations)...")
    elif args.method == 'exhaustive':
        print(f"\n🔍 Performing exhaustive search...")
    else:
        print(f"\n⚡ Generating {args.generate} candidate teams using '{args.method}' method...")

    best_teams = optimizer.find_best_teams(
        n=args.top,
        method=args.method,
        num_candidates=args.generate,
        required_cookies=required_cookies
    )

    # Display results
    if best_teams:
        print(f"\n🏆 Top {len(best_teams)} Teams:")
        for i, team in enumerate(best_teams, 1):
            print(f"\n--- Team #{i} ---")
            print(team)

        # Export if requested
        if args.export:
            optimizer.export_teams(best_teams, args.export, format=args.format)

        print("\n✅ Team optimization complete!")
    else:
        print("\n⚠️  No teams generated.")


if __name__ == "__main__":
    main()
