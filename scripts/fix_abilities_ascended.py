#!/usr/bin/env python3
"""Fix cookie_abilities.csv to use correct Ascended cookie names."""

import pandas as pd

# Load the abilities CSV
df = pd.read_csv('cookie_abilities.csv')

print(f"Total abilities before fix: {len(df)}")

# Map of Awakened skill names to Ascended cookie names
awakened_skills = {
    'Awakened Light of Unwavering Resolution': 'Pure Vanilla Cookie (Ascended)',
    'Awakened Grand Entrance': 'Hollyberry Cookie (Ascended)',
    'Awakened Grapejam Chocoblade': 'Dark Cacao Cookie (Ascended)',
    'Awakened Radiant Glory': 'Golden Cheese Cookie (Ascended)',
    'Awakened Final Verdict': 'White Lily Cookie (Ascended)'
}

print("\nUpdating Awakened skill cookie names:")
for skill_name, new_cookie_name in awakened_skills.items():
    mask = df['skill_name'] == skill_name
    old_name = df.loc[mask, 'cookie_name'].values[0] if mask.any() else 'NOT FOUND'
    df.loc[mask, 'cookie_name'] = new_cookie_name
    print(f"  {old_name} -> {new_cookie_name}")

# Check for duplicates
duplicates = df[df.duplicated(subset=['cookie_name'], keep=False)]
if len(duplicates) > 0:
    print(f"\n⚠️ WARNING: Found {len(duplicates)} duplicate cookie names:")
    print(duplicates[['cookie_name', 'skill_name']].to_string())
else:
    print(f"\n✓ No duplicate cookie names found!")

# Verify the fix
print("\n=== Verification ===")
for base_name in ['Pure Vanilla Cookie', 'Hollyberry Cookie', 'Dark Cacao Cookie',
                   'Golden Cheese Cookie', 'White Lily Cookie']:
    base_count = len(df[df['cookie_name'] == base_name])
    ascended_name = f"{base_name} (Ascended)"
    ascended_count = len(df[df['cookie_name'] == ascended_name])
    print(f"{base_name}: {base_count} | {ascended_name}: {ascended_count}")

# Save the fixed CSV
df.to_csv('cookie_abilities.csv', index=False)
print(f"\n✓ Saved fixed CSV to cookie_abilities.csv")
print(f"Total abilities after fix: {len(df)}")
