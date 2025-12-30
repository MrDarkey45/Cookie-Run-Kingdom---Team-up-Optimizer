#!/usr/bin/env python3
"""Fix Ascended cookies by renaming them to avoid duplicates."""

import pandas as pd

# Read the CSV
df = pd.read_csv('crk-cookies.csv')

print(f"Total cookies before fix: {len(df)}")
print(f"\nCookies with 'Ascended' rarity:")

# Find Ascended cookies
ascended_mask = df['cookie_rarity'].str.contains('Ascended', na=False)
ascended_cookies = df[ascended_mask]

print(f"Found {len(ascended_cookies)} Ascended cookies:")
for idx, row in ascended_cookies.iterrows():
    print(f"  - {row['cookie_name']} ({row['cookie_rarity']})")

# Rename Ascended cookies by appending (Ascended) to their names
df.loc[ascended_mask, 'cookie_name'] = df.loc[ascended_mask, 'cookie_name'] + ' (Ascended)'

# Also simplify the rarity from "Ancient (Ascended)" to just "Ancient (Ascended)"
# Keep it as is for now to maintain the distinction

print(f"\nAfter renaming:")
ascended_cookies_renamed = df[ascended_mask]
for idx, row in ascended_cookies_renamed.iterrows():
    print(f"  - {row['cookie_name']} ({row['cookie_rarity']})")

# Check for duplicates
duplicates = df[df.duplicated(subset=['cookie_name'], keep=False)]
if len(duplicates) > 0:
    print(f"\n⚠️ WARNING: Still found {len(duplicates)} duplicate cookie names:")
    print(duplicates[['cookie_name', 'cookie_rarity']].to_string())
else:
    print(f"\n✓ No duplicate cookie names found!")

# Save the fixed CSV
df.to_csv('crk-cookies.csv', index=False, encoding='utf-8-sig')
print(f"\n✓ Saved fixed CSV to crk-cookies.csv")
print(f"Total cookies after fix: {len(df)}")
