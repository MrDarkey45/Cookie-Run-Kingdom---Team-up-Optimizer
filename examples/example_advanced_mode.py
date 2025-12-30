"""
Example: Using Team Optimizer in Advanced Mode

This script demonstrates how to use the team optimizer with custom
cookie levels, skill levels, and topping quality for personalized
team recommendations based on your actual cookie collection.
"""

from team_optimizer import Cookie, Team, TeamOptimizer


def example_basic_vs_advanced():
    """Compare basic rarity-only vs advanced scoring with levels/skills."""

    print("="*70)
    print("EXAMPLE: Basic vs Advanced Mode Comparison")
    print("="*70)

    # Same cookie, different modes
    cookie_name = "Shadow Milk Cookie"
    rarity = "Beast"
    role = "Magic"
    position = "Middle"

    # Basic mode - rarity only
    basic_cookie = Cookie(cookie_name, rarity, role, position)
    print(f"\n📊 Basic Mode (Rarity Only):")
    print(f"   {basic_cookie}")

    # Advanced mode - with progression stats
    advanced_cookie = Cookie(
        cookie_name, rarity, role, position,
        cookie_level=70,      # Max level
        skill_level=60,       # Max skill
        topping_quality=5.0   # Perfect toppings
    )
    print(f"\n📈 Advanced Mode (Maxed Out):")
    print(f"   {advanced_cookie}")

    # Advanced mode - moderate investment
    moderate_cookie = Cookie(
        cookie_name, rarity, role, position,
        cookie_level=50,      # Mid level
        skill_level=40,       # Mid skill
        topping_quality=3.0   # Good toppings
    )
    print(f"\n📊 Advanced Mode (Moderate Investment):")
    print(f"   {moderate_cookie}")

    # Advanced mode - new cookie
    new_cookie = Cookie(
        cookie_name, rarity, role, position,
        cookie_level=20,      # Low level
        skill_level=10,       # Low skill
        topping_quality=1.0   # Basic toppings
    )
    print(f"\n📉 Advanced Mode (New Cookie):")
    print(f"   {new_cookie}")

    print("\n" + "="*70)
    print("💡 Notice how skill level has the biggest impact on power score!")
    print("="*70)


def example_custom_team():
    """Create a custom team with your actual cookie stats."""

    print("\n" + "="*70)
    print("EXAMPLE: Custom Team with Real Cookie Stats")
    print("="*70)

    # Create your actual cookies with their real stats
    my_cookies = [
        Cookie("Pure Vanilla Cookie", "Ancient", "Healing", "Rear",
               cookie_level=70, skill_level=60, topping_quality=4.5),

        Cookie("Dark Cacao Cookie", "Ancient", "Charge", "Front",
               cookie_level=68, skill_level=58, topping_quality=4.0),

        Cookie("Financier Cookie", "Epic", "Defense", "Front",
               cookie_level=60, skill_level=50, topping_quality=3.5),

        Cookie("Shadow Milk Cookie", "Beast", "Magic", "Middle",
               cookie_level=55, skill_level=45, topping_quality=3.0),

        Cookie("Oyster Cookie", "Super Epic", "Support", "Rear",
               cookie_level=50, skill_level=40, topping_quality=2.5)
    ]

    # Create team
    my_team = Team(my_cookies)
    print(f"\n🎮 Your Custom Team:")
    print(my_team)

    print("\n" + "="*70)
    print("💡 This team reflects YOUR actual cookie investment!")
    print("   Higher skill levels = better score, even for Epic cookies")
    print("="*70)


def example_comparison_scenario():
    """Compare two team strategies: high rarity vs high investment."""

    print("\n" + "="*70)
    print("EXAMPLE: High Rarity vs High Investment Strategy")
    print("="*70)

    # Team 1: All Beast/Ancient but low investment
    high_rarity_team = [
        Cookie("Shadow Milk Cookie", "Beast", "Magic", "Middle",
               cookie_level=30, skill_level=20, topping_quality=1.0),
        Cookie("Mystic Flour Cookie", "Beast", "Healing", "Rear",
               cookie_level=30, skill_level=20, topping_quality=1.0),
        Cookie("Pure Vanilla Cookie", "Ancient", "Healing", "Rear",
               cookie_level=30, skill_level=20, topping_quality=1.0),
        Cookie("Dark Cacao Cookie", "Ancient", "Charge", "Front",
               cookie_level=30, skill_level=20, topping_quality=1.0),
        Cookie("Golden Cheese Cookie", "Ancient", "Ranged", "Middle",
               cookie_level=30, skill_level=20, topping_quality=1.0)
    ]

    # Team 2: Epic cookies but maxed investment
    high_investment_team = [
        Cookie("Financier Cookie", "Epic", "Defense", "Front",
               cookie_level=70, skill_level=60, topping_quality=5.0),
        Cookie("Eclair Cookie", "Epic", "Support", "Middle",
               cookie_level=70, skill_level=60, topping_quality=5.0),
        Cookie("Cotton Cookie", "Epic", "Support", "Rear",
               cookie_level=70, skill_level=60, topping_quality=5.0),
        Cookie("Espresso Cookie", "Epic", "Magic", "Middle",
               cookie_level=70, skill_level=60, topping_quality=5.0),
        Cookie("Caramel Arrow Cookie", "Epic", "Ranged", "Front",
               cookie_level=70, skill_level=60, topping_quality=5.0)
    ]

    team1 = Team(high_rarity_team)
    team2 = Team(high_investment_team)

    print("\n🌟 Team 1: High Rarity, Low Investment")
    print(team1)

    print("\n⚡ Team 2: Lower Rarity, High Investment")
    print(team2)

    print("\n" + "="*70)
    if team2.composition_score > team1.composition_score:
        print("✅ WINNER: Team 2 (High Investment)")
        print("   Investment in skill levels beats raw rarity!")
    else:
        print("✅ WINNER: Team 1 (High Rarity)")
        print("   Rarity advantage overcame lower investment")
    print("="*70)


def example_optimizer_with_custom_collection():
    """Example of how to use optimizer with a subset of your collection."""

    print("\n" + "="*70)
    print("EXAMPLE: Optimize Teams from Your Cookie Collection")
    print("="*70)

    # Simulate your cookie collection with actual stats
    my_collection = [
        Cookie("Shadow Milk Cookie", "Beast", "Magic", "Middle",
               cookie_level=70, skill_level=60, topping_quality=5.0),
        Cookie("Pure Vanilla Cookie", "Ancient", "Healing", "Rear",
               cookie_level=68, skill_level=58, topping_quality=4.5),
        Cookie("Dark Cacao Cookie", "Ancient", "Charge", "Front",
               cookie_level=65, skill_level=55, topping_quality=4.0),
        Cookie("Financier Cookie", "Epic", "Defense", "Front",
               cookie_level=60, skill_level=52, topping_quality=4.0),
        Cookie("Cotton Cookie", "Epic", "Support", "Rear",
               cookie_level=62, skill_level=54, topping_quality=4.5),
        Cookie("Espresso Cookie", "Epic", "Magic", "Middle",
               cookie_level=58, skill_level=50, topping_quality=3.5),
        Cookie("Caramel Arrow Cookie", "Epic", "Ranged", "Front",
               cookie_level=55, skill_level=48, topping_quality=3.0),
        Cookie("Wildberry Cookie", "Epic", "Defense", "Front",
               cookie_level=60, skill_level=50, topping_quality=3.5),
    ]

    # Manual team building from your collection
    print("\n🔍 Finding best team from your 8 invested cookies...")

    # Generate all possible 5-cookie combinations from your collection
    from itertools import combinations

    all_possible_teams = []
    for combo in combinations(my_collection, 5):
        try:
            team = Team(list(combo))
            all_possible_teams.append(team)
        except ValueError:
            continue

    # Sort by score
    all_possible_teams.sort(key=lambda t: t.composition_score, reverse=True)

    print(f"\n📊 Generated {len(all_possible_teams)} possible teams from your collection")
    print(f"\n🏆 Your Best Team:")
    print(all_possible_teams[0])

    print("\n" + "="*70)
    print("💡 TIP: This uses YOUR actual cookie stats for realistic recommendations!")
    print("="*70)


if __name__ == "__main__":
    # Run all examples
    example_basic_vs_advanced()
    example_custom_team()
    example_comparison_scenario()
    example_optimizer_with_custom_collection()

    print("\n" + "="*70)
    print("✅ Advanced Mode Examples Complete!")
    print("\n💡 Next Steps:")
    print("   1. Update your cookie stats in a separate CSV/JSON")
    print("   2. Load your collection into the optimizer")
    print("   3. Find optimal teams based on YOUR investment")
    print("="*70)
