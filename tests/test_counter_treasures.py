#!/usr/bin/env python3
"""Test counter-team treasure recommendations."""

from team_optimizer import TeamOptimizer, Team
from counter_team_generator import CounterTeamGenerator

# Load optimizer with treasures
optimizer = TeamOptimizer('crk-cookies.csv')

# Create enemy team (healing-heavy with Shadow Milk)
enemy_cookies = []
for name in ['Pure Vanilla Cookie', 'Shadow Milk Cookie', 'Cream Ferret Cookie',
             'Hollyberry Cookie', 'Parfait Cookie']:
    cookie = next((c for c in optimizer.all_cookies if c.name == name), None)
    if cookie:
        enemy_cookies.append(cookie)

if len(enemy_cookies) == 5:
    enemy_team = Team(enemy_cookies)

    print("="*80)
    print("COUNTER-TEAM TREASURE RECOMMENDATION TEST")
    print("="*80)
    print()
    print(f"Enemy Team: {', '.join([c.name for c in enemy_team.cookies])}")
    print()

    # Generate counter-teams
    generator = CounterTeamGenerator(optimizer)
    counter_teams = generator.find_counter_teams(enemy_team, n=2, method='greedy')

    for i, (team, counter_info) in enumerate(counter_teams, 1):
        print("="*80)
        print(f"Counter-Team #{i}")
        print("="*80)
        print(f"Counter Score: {counter_info['counter_score']:.1f}/100")
        print(f"Team Score: {counter_info['team_score']:.1f}")
        print(f"Combined Score: {counter_info['combined_score']:.1f}/100")
        print(f"\nStrategy: {counter_info['strategy']}")
        print(f"\nTeam Composition:")
        for cookie in team.cookies:
            print(f"  • {cookie.name} ({cookie.role}, {cookie.position})")

        print(f"\n🎁 Recommended Treasures:")
        for treasure in counter_info['recommended_treasures']:
            print(f"\n  {treasure['name']} (Tier: {treasure['tier']}, Score: {treasure['score']})")
            print(f"  Reason: {treasure['reason']}")
            print(f"  Effects:")
            effects = treasure['effects']
            if effects['atk_boost'] > 0:
                print(f"    - ATK Boost: +{effects['atk_boost']}%")
            if effects['crit_boost'] > 0:
                print(f"    - CRIT Boost: +{effects['crit_boost']}%")
            if effects['cooldown_reduction'] > 0:
                print(f"    - Cooldown Reduction: -{effects['cooldown_reduction']}%")
            if effects['dmg_resist'] > 0:
                print(f"    - DMG Resist: +{effects['dmg_resist']}%")
            if effects['hp_shield'] > 0:
                print(f"    - HP Shield: +{effects['hp_shield']}%")
            if effects['heal'] > 0:
                print(f"    - Healing: +{effects['heal']}%")

        print()

    print("="*80)
    print("✓ Counter-team treasure recommendation test complete!")
    print("="*80)
