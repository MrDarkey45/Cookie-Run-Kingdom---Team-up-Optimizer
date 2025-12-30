#!/usr/bin/env python3
"""Test treasure scoring system."""

from team_optimizer import TeamOptimizer, Team

# Load optimizer with treasures
optimizer = TeamOptimizer('crk-cookies.csv')

# Create a test team
test_cookies = []
for name in ['Shadow Milk Cookie', 'Black Pearl Cookie', 'Frost Queen Cookie',
             'Pure Vanilla Cookie', 'Dark Cacao Cookie']:
    cookie = next((c for c in optimizer.all_cookies if c.name == name), None)
    if cookie:
        test_cookies.append(cookie)

if len(test_cookies) == 5:
    # Test 1: Team without treasures
    team_no_treasures = Team(test_cookies, treasures=[])
    print("="*70)
    print("Test 1: Team WITHOUT Treasures")
    print("="*70)
    print(f"Team Score: {team_no_treasures.composition_score:.2f}")
    print(f"Treasure Bonus: {team_no_treasures.treasure_bonus:.2f}")
    print()

    # Test 2: Team with S+ tier treasures (the holy trinity)
    s_plus_treasures = []
    for name in ['Old Pilgrim\'s Scroll', 'Squishy Jelly Watch', 'Dream Conductor\'s Whistle']:
        treasure = next((t for t in optimizer.all_treasures if t.name == name), None)
        if treasure:
            s_plus_treasures.append(treasure)
            print(f"Added treasure: {treasure.name} (Tier: {treasure.tier_ranking})")

    if len(s_plus_treasures) == 3:
        team_with_treasures = Team(test_cookies, treasures=s_plus_treasures)
        print()
        print("="*70)
        print("Test 2: Team WITH S+ Tier Treasures")
        print("="*70)
        print(f"Team Score: {team_with_treasures.composition_score:.2f}")
        print(f"Treasure Bonus: {team_with_treasures.treasure_bonus:.2f}")
        print()
        print("Treasure Effects:")
        for treasure in s_plus_treasures:
            print(f"  • {treasure.name}:")
            print(f"    - ATK Boost: {treasure.atk_boost_max}%")
            print(f"    - CRIT Boost: {treasure.crit_boost_max}%")
            print(f"    - Cooldown Reduction: {treasure.cooldown_reduction_max}%")
        print()
        print(f"Score Improvement: +{team_with_treasures.composition_score - team_no_treasures.composition_score:.2f} points")
        print()

    # Test 3: Team with revival treasure
    revival_treasure = next((t for t in optimizer.all_treasures if t.name == 'Sugar Swan\'s Shining Feather'), None)
    if revival_treasure:
        team_with_revival = Team(test_cookies, treasures=[revival_treasure])
        print("="*70)
        print("Test 3: Team WITH Revival Treasure")
        print("="*70)
        print(f"Treasure: {revival_treasure.name} (Tier: {revival_treasure.tier_ranking})")
        print(f"Revival Effect: {revival_treasure.revive}")
        print(f"Team Score: {team_with_revival.composition_score:.2f}")
        print(f"Treasure Bonus: {team_with_revival.treasure_bonus:.2f}")
        print()

    # Test 4: Export to dict to verify treasure data is included
    team_dict = team_with_treasures.to_dict()
    if 'treasures' in team_dict:
        print("="*70)
        print("Test 4: Treasure Data Export")
        print("="*70)
        print("✓ Treasures successfully exported to team dict")
        print(f"Number of treasures: {len(team_dict['treasures'])}")
        print(f"Treasure bonus in export: {team_dict['treasure_bonus']}")
        print()
        for i, treasure_data in enumerate(team_dict['treasures'], 1):
            print(f"{i}. {treasure_data['name']} (Tier: {treasure_data['tier_ranking']})")
    else:
        print("✗ Treasures NOT found in export!")

print()
print("="*70)
print("✓ All treasure scoring tests complete!")
print("="*70)
