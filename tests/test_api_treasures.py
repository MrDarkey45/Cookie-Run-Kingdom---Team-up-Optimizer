#!/usr/bin/env python3
"""Test the treasures API endpoint."""

import sys
import os
sys.path.insert(0, 'web_ui')

from app import app

# Create a test client
client = app.test_client()

print("="*80)
print("Testing /api/treasures endpoint")
print("="*80)
print()

# Test GET /api/treasures
response = client.get('/api/treasures')

if response.status_code == 200:
    treasures = response.get_json()
    print(f"✓ API endpoint working! Retrieved {len(treasures)} treasures")
    print()
    print("Top 5 Treasures by Tier:")
    print()
    for i, treasure in enumerate(treasures[:5], 1):
        print(f"{i}. {treasure['name']}")
        print(f"   Tier: {treasure['tier_ranking']} | Rarity: {treasure['rarity']} | Type: {treasure['activation_type']}")
        print(f"   Effect: {treasure['primary_effect']}")
        print(f"   Power Score: {treasure['power_score']}")

        # Show key stats
        stats = []
        if treasure['atk_boost'] > 0:
            stats.append(f"ATK +{treasure['atk_boost']}%")
        if treasure['crit_boost'] > 0:
            stats.append(f"CRIT +{treasure['crit_boost']}%")
        if treasure['cooldown_reduction'] > 0:
            stats.append(f"CDR -{treasure['cooldown_reduction']}%")
        if treasure['hp_shield'] > 0:
            stats.append(f"Shield +{treasure['hp_shield']}%")
        if treasure['heal'] > 0:
            stats.append(f"Heal +{treasure['heal']}%")

        if stats:
            print(f"   Stats: {', '.join(stats)}")

        # Show special effects
        special = []
        if treasure['revive']:
            special.append("Revival")
        if treasure['debuff_cleanse']:
            special.append("Cleanse")
        if treasure['enemy_debuff']:
            special.append("Enemy Debuff")
        if treasure['summon_boost']:
            special.append("Summon Boost")

        if special:
            print(f"   Special: {', '.join(special)}")

        print()
else:
    print(f"✗ API endpoint failed with status {response.status_code}")

print("="*80)
print("✓ Treasures API test complete!")
print("="*80)
