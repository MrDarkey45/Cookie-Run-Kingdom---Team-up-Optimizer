"""
Synergy Calculator Module for Cookie Run: Kingdom

This module calculates synergy scores between cookies and teams based on:
- Role compatibility (Tank+Healer, DPS+Support, etc.)
- Position synergy (Front/Middle/Rear balance)
- Elemental matching (same element bonuses)
- Type-based synergies (3+ Beast/Ancient/etc.)

Synergy Score (0-100):
    Role Synergy: 0-30 points
    Position Synergy: 0-20 points
    Elemental Synergy: 0-25 points
    Type-Based Synergy: 0-15 points
    Buff/Debuff Coverage: 0-10 points
"""

from typing import List, Dict, Tuple, Optional
from collections import Counter
from team_optimizer import Cookie, Team


# Role Synergy Matrix - How well roles work together (0.0 to 1.0)
ROLE_SYNERGY_MATRIX = {
    # Tanks (Defense, Charge) synergize with Healers and Support
    'Defense': {
        'Healing': 1.0,   # Tanks + Healers = perfect combo
        'Support': 0.9,   # Tanks + Support = great
        'Magic': 0.7,     # Tanks + DPS = decent
        'Ranged': 0.7,
        'Bomber': 0.7,
        'Ambush': 0.6,
        'Charge': 0.5,    # Double tank = okay
        'Defense': 0.4    # Triple tank = not ideal
    },
    'Charge': {
        'Healing': 1.0,
        'Support': 0.9,
        'Magic': 0.7,
        'Ranged': 0.7,
        'Bomber': 0.7,
        'Ambush': 0.6,
        'Defense': 0.5,
        'Charge': 0.4
    },
    # Healers synergize with everyone
    'Healing': {
        'Defense': 1.0,
        'Charge': 1.0,
        'Magic': 0.9,
        'Ranged': 0.9,
        'Bomber': 0.9,
        'Ambush': 0.9,
        'Support': 0.8,
        'Healing': 0.3    # Multiple healers = overkill
    },
    # Support synergizes with DPS and Tanks
    'Support': {
        'Defense': 0.9,
        'Charge': 0.9,
        'Magic': 0.9,
        'Ranged': 0.9,
        'Bomber': 0.9,
        'Ambush': 0.8,
        'Healing': 0.8,
        'Support': 0.5
    },
    # DPS roles (Magic, Ranged, Bomber, Ambush)
    'Magic': {
        'Healing': 0.9,
        'Support': 0.9,
        'Defense': 0.7,
        'Charge': 0.7,
        'Ranged': 0.7,
        'Bomber': 0.7,
        'Ambush': 0.7,
        'Magic': 0.6
    },
    'Ranged': {
        'Healing': 0.9,
        'Support': 0.9,
        'Defense': 0.7,
        'Charge': 0.7,
        'Magic': 0.7,
        'Bomber': 0.7,
        'Ambush': 0.7,
        'Ranged': 0.6
    },
    'Bomber': {
        'Healing': 0.9,
        'Support': 0.9,
        'Defense': 0.7,
        'Charge': 0.7,
        'Magic': 0.7,
        'Ranged': 0.7,
        'Ambush': 0.7,
        'Bomber': 0.6
    },
    'Ambush': {
        'Healing': 0.9,
        'Support': 0.8,
        'Defense': 0.6,
        'Charge': 0.6,
        'Magic': 0.7,
        'Ranged': 0.7,
        'Bomber': 0.7,
        'Ambush': 0.6
    }
}

# Elemental synergy bonus multiplier (same element teams get bonus)
ELEMENT_BONUS_MULTIPLIER = 1.15  # 15% bonus per matching element

# Type synergy thresholds
TYPE_SYNERGY_THRESHOLD = 3  # Need 3+ of same type for bonus


class SynergyCalculator:
    """Calculate synergy scores between cookies and teams."""

    def __init__(self):
        """Initialize the synergy calculator."""
        self.role_matrix = ROLE_SYNERGY_MATRIX
        self.element_multiplier = ELEMENT_BONUS_MULTIPLIER
        self.type_threshold = TYPE_SYNERGY_THRESHOLD

    def calculate_cookie_synergy(self, cookie1: Cookie, cookie2: Cookie) -> float:
        """
        Calculate synergy score between two individual cookies.

        Args:
            cookie1: First cookie
            cookie2: Second cookie

        Returns:
            float: Synergy score (0-10, where 10 is perfect synergy)
        """
        synergy_score = 0.0

        # Role synergy (0-5 points)
        role1 = cookie1.role
        role2 = cookie2.role

        if role1 in self.role_matrix and role2 in self.role_matrix[role1]:
            role_synergy = self.role_matrix[role1][role2] * 5.0
            synergy_score += role_synergy

        # Position synergy (0-2 points)
        # Different positions = better coverage
        if cookie1.position != cookie2.position:
            synergy_score += 2.0
        else:
            synergy_score += 0.5  # Same position = some synergy

        # Elemental synergy (0-3 points)
        if cookie1.rarity != 'N/A' and cookie2.rarity != 'N/A':
            element1 = getattr(cookie1, 'element', 'N/A')
            element2 = getattr(cookie2, 'element', 'N/A')

            if element1 != 'N/A' and element2 != 'N/A' and element1 == element2:
                synergy_score += 3.0  # Same element bonus
            elif element1 != 'N/A' and element2 != 'N/A':
                synergy_score += 0.5  # Different elements = slight bonus

        return min(synergy_score, 10.0)  # Cap at 10

    def calculate_team_synergy(self, team: Team) -> Dict[str, float]:
        """
        Calculate comprehensive team synergy score.

        Args:
            team: Team instance to analyze

        Returns:
            dict: Dictionary with synergy breakdown
                - total_score: Overall synergy (0-100)
                - role_synergy: Role compatibility (0-30)
                - position_synergy: Position coverage (0-20)
                - element_synergy: Elemental matching (0-25)
                - type_synergy: Type-based bonus (0-15)
                - coverage_synergy: Buff/debuff coverage (0-10)
        """
        synergy_breakdown = {
            'role_synergy': 0.0,
            'position_synergy': 0.0,
            'element_synergy': 0.0,
            'type_synergy': 0.0,
            'coverage_synergy': 0.0,
            'total_score': 0.0
        }

        if not team or len(team.cookies) != 5:
            return synergy_breakdown

        # 1. ROLE SYNERGY (0-30 points)
        # Calculate average pairwise role synergy
        role_pairs = []
        for i in range(len(team.cookies)):
            for j in range(i + 1, len(team.cookies)):
                cookie1 = team.cookies[i]
                cookie2 = team.cookies[j]

                role1 = cookie1.role
                role2 = cookie2.role

                if role1 in self.role_matrix and role2 in self.role_matrix[role1]:
                    role_pairs.append(self.role_matrix[role1][role2])

        if role_pairs:
            avg_role_synergy = sum(role_pairs) / len(role_pairs)
            synergy_breakdown['role_synergy'] = avg_role_synergy * 30.0

        # 2. POSITION SYNERGY (0-20 points)
        position_dist = team.get_position_distribution()
        position_coverage = len(position_dist)

        if position_coverage == 3:
            synergy_breakdown['position_synergy'] = 20.0  # All 3 positions
        elif position_coverage == 2:
            synergy_breakdown['position_synergy'] = 12.0  # 2 positions
        else:
            synergy_breakdown['position_synergy'] = 5.0   # Only 1 position

        # Bonus for balanced distribution (2-2-1 or 2-1-2 is ideal)
        position_counts = list(position_dist.values())
        if sorted(position_counts) == [1, 2, 2]:
            synergy_breakdown['position_synergy'] += 5.0

        # 3. ELEMENTAL SYNERGY (0-25 points)
        # Count cookies with elements and calculate element matching
        element_counts = Counter()
        total_with_elements = 0

        for cookie in team.cookies:
            element = getattr(cookie, 'element', 'N/A')
            if element and element != 'N/A':
                element_counts[element] += 1
                total_with_elements += 1

        if total_with_elements > 0:
            # Calculate element matching score
            max_element_count = max(element_counts.values()) if element_counts else 0

            if max_element_count >= 5:
                synergy_breakdown['element_synergy'] = 25.0  # All same element!
            elif max_element_count == 4:
                synergy_breakdown['element_synergy'] = 20.0  # 4 matching
            elif max_element_count == 3:
                synergy_breakdown['element_synergy'] = 15.0  # 3 matching
            elif max_element_count == 2:
                synergy_breakdown['element_synergy'] = 8.0   # 2 matching
            else:
                synergy_breakdown['element_synergy'] = 3.0   # All different

        # 4. TYPE-BASED SYNERGY (0-15 points)
        # Count cookies by rarity type
        rarity_counts = Counter()
        for cookie in team.cookies:
            rarity_counts[cookie.rarity] += 1

        # Check for type synergies (3+ of same high-tier type)
        high_tier_types = ['Beast', 'Ancient', 'Ancient (Ascended)', 'Legendary', 'Dragon']

        for rarity, count in rarity_counts.items():
            if rarity in high_tier_types and count >= self.type_threshold:
                if count == 5:
                    synergy_breakdown['type_synergy'] = 15.0  # All same type!
                elif count == 4:
                    synergy_breakdown['type_synergy'] = 12.0
                elif count == 3:
                    synergy_breakdown['type_synergy'] = 8.0
                break

        # 5. COVERAGE SYNERGY (0-10 points)
        # Check for essential role coverage
        role_dist = team.get_role_distribution()

        coverage_score = 0.0

        # Has tank
        if any(role in role_dist for role in ['Defense', 'Charge']):
            coverage_score += 3.0

        # Has healer
        if any(role in role_dist for role in ['Healing', 'Support']):
            coverage_score += 3.0

        # Has DPS
        if any(role in role_dist for role in ['Magic', 'Ranged', 'Bomber', 'Ambush']):
            coverage_score += 2.0

        # Role diversity bonus
        if len(role_dist) >= 4:
            coverage_score += 2.0

        synergy_breakdown['coverage_synergy'] = coverage_score

        # Calculate total synergy score
        synergy_breakdown['total_score'] = (
            synergy_breakdown['role_synergy'] +
            synergy_breakdown['position_synergy'] +
            synergy_breakdown['element_synergy'] +
            synergy_breakdown['type_synergy'] +
            synergy_breakdown['coverage_synergy']
        )

        return synergy_breakdown

    def get_synergy_suggestions(
        self,
        selected_cookies: List[Cookie],
        all_cookies: List[Cookie],
        top_n: int = 5
    ) -> List[Tuple[Cookie, float, str]]:
        """
        Suggest cookies that have good synergy with selected cookies.

        Args:
            selected_cookies: List of already selected cookies
            all_cookies: List of all available cookies
            top_n: Number of suggestions to return

        Returns:
            List of (Cookie, synergy_score, reason) tuples
        """
        if not selected_cookies:
            return []

        suggestions = []

        for cookie in all_cookies:
            # Skip if already selected
            if cookie.name in [c.name for c in selected_cookies]:
                continue

            # Calculate average synergy with selected cookies
            synergy_scores = []
            reasons = []

            for selected in selected_cookies:
                score = self.calculate_cookie_synergy(selected, cookie)
                synergy_scores.append(score)

                # Generate reason
                reason_parts = []

                # Check element matching
                selected_element = getattr(selected, 'element', 'N/A')
                cookie_element = getattr(cookie, 'element', 'N/A')
                if selected_element != 'N/A' and cookie_element != 'N/A':
                    if selected_element == cookie_element:
                        reason_parts.append(f"Same element ({cookie_element})")

                # Check role synergy
                role1 = selected.role
                role2 = cookie.role
                if role1 in self.role_matrix and role2 in self.role_matrix[role1]:
                    synergy_value = self.role_matrix[role1][role2]
                    if synergy_value >= 0.9:
                        reason_parts.append(f"{role2} complements {role1}")

                if reason_parts:
                    reasons.append(", ".join(reason_parts))

            if synergy_scores:
                avg_synergy = sum(synergy_scores) / len(synergy_scores)
                reason = reasons[0] if reasons else "Good team fit"
                suggestions.append((cookie, avg_synergy, reason))

        # Sort by synergy score and return top N
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return suggestions[:top_n]

    def explain_synergy(self, team: Team) -> str:
        """
        Generate human-readable explanation of team synergy.

        Args:
            team: Team to explain

        Returns:
            str: Explanation text
        """
        breakdown = self.calculate_team_synergy(team)

        explanation = f"Team Synergy Analysis (Total: {breakdown['total_score']:.1f}/100)\n\n"

        # Role synergy
        explanation += f"⚔️  Role Synergy: {breakdown['role_synergy']:.1f}/30\n"
        if breakdown['role_synergy'] >= 24:
            explanation += "   Excellent role compatibility!\n"
        elif breakdown['role_synergy'] >= 18:
            explanation += "   Good role balance.\n"
        else:
            explanation += "   Could improve role diversity.\n"

        # Position synergy
        explanation += f"\n📍 Position Synergy: {breakdown['position_synergy']:.1f}/20\n"
        position_dist = team.get_position_distribution()
        explanation += f"   Coverage: {', '.join([f'{k}: {v}' for k, v in position_dist.items()])}\n"

        # Element synergy
        explanation += f"\n✨ Element Synergy: {breakdown['element_synergy']:.1f}/25\n"
        element_counts = Counter()
        for cookie in team.cookies:
            element = getattr(cookie, 'element', 'N/A')
            if element and element != 'N/A':
                element_counts[element] += 1

        if element_counts:
            explanation += f"   Elements: {', '.join([f'{k}: {v}' for k, v in element_counts.items()])}\n"
        else:
            explanation += "   No elemental data available.\n"

        # Type synergy
        explanation += f"\n🌟 Type Synergy: {breakdown['type_synergy']:.1f}/15\n"
        rarity_counts = Counter([c.rarity for c in team.cookies])
        top_rarity = rarity_counts.most_common(1)[0]
        explanation += f"   Dominant type: {top_rarity[0]} ({top_rarity[1]} cookies)\n"

        # Coverage
        explanation += f"\n🛡️  Coverage: {breakdown['coverage_synergy']:.1f}/10\n"
        explanation += f"   Tank: {'✓' if team.has_tank() else '✗'} | "
        explanation += f"Healer: {'✓' if team.has_healer() else '✗'}\n"

        return explanation


def main():
    """Example usage of synergy calculator."""
    from team_optimizer import TeamOptimizer

    # Load cookies
    optimizer = TeamOptimizer('crk-cookies.csv')

    # Find a good team
    teams = optimizer.find_best_teams(n=1, method='genetic', num_candidates=50)

    if teams:
        team = teams[0]

        # Calculate synergy
        calculator = SynergyCalculator()
        synergy = calculator.calculate_team_synergy(team)

        print(f"\n{'='*60}")
        print(f"Team: {', '.join([c.name for c in team.cookies])}")
        print(f"{'='*60}")
        print(calculator.explain_synergy(team))

        # Show synergy suggestions
        print(f"\n{'='*60}")
        print("Top 5 cookies that would synergize well:")
        print(f"{'='*60}")

        suggestions = calculator.get_synergy_suggestions(
            team.cookies,
            optimizer.all_cookies,
            top_n=5
        )

        for i, (cookie, score, reason) in enumerate(suggestions, 1):
            print(f"{i}. {cookie.name} (Score: {score:.1f}/10) - {reason}")


if __name__ == '__main__':
    main()
