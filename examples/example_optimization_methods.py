"""
Example: Comparing Different Optimization Methods

This script demonstrates the various team optimization algorithms available
and shows how to build teams around specific cookies.
"""

from team_optimizer import TeamOptimizer
import time


def compare_optimization_methods():
    """Compare different optimization algorithms."""
    print("="*70)
    print("COMPARING OPTIMIZATION METHODS")
    print("="*70)

    optimizer = TeamOptimizer('crk-cookies.csv')

    methods = {
        'random': {'num_candidates': 1000, 'description': 'Random sampling'},
        'greedy': {'num_candidates': 1000, 'description': 'Greedy selection (high-power cookies first)'},
        'genetic': {'num_candidates': 100, 'description': 'Genetic algorithm (100 generations)'}
    }

    results = {}

    for method_name, config in methods.items():
        print(f"\n{'='*70}")
        print(f"🔬 Method: {config['description']}")
        print(f"{'='*70}")

        start_time = time.time()

        best_teams = optimizer.find_best_teams(
            n=5,
            method=method_name,
            num_candidates=config['num_candidates']
        )

        elapsed = time.time() - start_time

        if best_teams:
            best_score = best_teams[0].composition_score
            avg_score = sum(t.composition_score for t in best_teams) / len(best_teams)

            results[method_name] = {
                'best_score': best_score,
                'avg_score': avg_score,
                'time': elapsed
            }

            print(f"\n📊 Results:")
            print(f"   Best Team Score: {best_score:.1f}/100")
            print(f"   Avg Top 5 Score: {avg_score:.1f}/100")
            print(f"   Time Taken: {elapsed:.2f}s")

            print(f"\n🏆 Best Team:")
            print(best_teams[0])

    # Summary comparison
    print("\n" + "="*70)
    print("📈 SUMMARY COMPARISON")
    print("="*70)
    print(f"{'Method':<15} {'Best Score':<12} {'Avg Score':<12} {'Time (s)':<10}")
    print("-"*70)

    for method, data in results.items():
        print(f"{method.capitalize():<15} {data['best_score']:<12.1f} {data['avg_score']:<12.1f} {data['time']:<10.2f}")

    # Determine winner
    best_method = max(results.items(), key=lambda x: x[1]['best_score'])
    fastest_method = min(results.items(), key=lambda x: x[1]['time'])

    print("\n" + "="*70)
    print(f"🏅 Best Score: {best_method[0].capitalize()} ({best_method[1]['best_score']:.1f}/100)")
    print(f"⚡ Fastest: {fastest_method[0].capitalize()} ({fastest_method[1]['time']:.2f}s)")
    print("="*70)


def build_around_cookie_example():
    """Demonstrate building teams around a specific cookie."""
    print("\n" + "="*70)
    print("BUILDING TEAMS AROUND SPECIFIC COOKIES")
    print("="*70)

    optimizer = TeamOptimizer('crk-cookies.csv')

    # Example 1: Build around one cookie
    print("\n🎯 Example 1: Build the best team around 'Shadow Milk Cookie'")
    print("-"*70)

    best_teams = optimizer.find_best_teams(
        n=3,
        method='genetic',
        num_candidates=50,
        required_cookies=['Shadow Milk Cookie']
    )

    if best_teams:
        print(f"\n🏆 Best Team (Score: {best_teams[0].composition_score:.1f}/100):")
        for i, cookie in enumerate(best_teams[0].cookies, 1):
            marker = "🔒" if cookie.name == 'Shadow Milk Cookie' else "  "
            print(f"   {marker} {i}. {cookie}")

    # Example 2: Build around multiple cookies
    print("\n" + "="*70)
    print("🎯 Example 2: Build team around 'Pure Vanilla Cookie' + 'Dark Cacao Cookie'")
    print("-"*70)

    best_teams = optimizer.find_best_teams(
        n=3,
        method='greedy',
        num_candidates=500,
        required_cookies=['Pure Vanilla Cookie', 'Dark Cacao Cookie']
    )

    if best_teams:
        print(f"\n🏆 Best Team (Score: {best_teams[0].composition_score:.1f}/100):")
        required_names = {'Pure Vanilla Cookie', 'Dark Cacao Cookie'}
        for i, cookie in enumerate(best_teams[0].cookies, 1):
            marker = "🔒" if cookie.name in required_names else "  "
            print(f"   {marker} {i}. {cookie}")

    # Example 3: Fill around 3 cookies
    print("\n" + "="*70)
    print("🎯 Example 3: I have these 3 cookies maxed - who should I pair them with?")
    print("   - Mystic Flour Cookie (Beast, Healer)")
    print("   - Burning Spice Cookie (Beast, Tank)")
    print("   - Shadow Milk Cookie (Beast, DPS)")
    print("-"*70)

    best_teams = optimizer.find_best_teams(
        n=1,
        method='genetic',
        num_candidates=100,
        required_cookies=['Mystic Flour Cookie', 'Burning Spice Cookie', 'Shadow Milk Cookie']
    )

    if best_teams:
        print(f"\n🏆 Recommended Team (Score: {best_teams[0].composition_score:.1f}/100):")
        required_names = {'Mystic Flour Cookie', 'Burning Spice Cookie', 'Shadow Milk Cookie'}

        for i, cookie in enumerate(best_teams[0].cookies, 1):
            if cookie.name in required_names:
                print(f"   🔒 {i}. {cookie} (Your cookie)")
            else:
                print(f"   ➕ {i}. {cookie} (RECOMMENDED)")

        print("\n💡 The algorithm filled the remaining 2 slots with cookies that:")
        print("   - Maximize role diversity")
        print("   - Cover all positions (Front/Middle/Rear)")
        print("   - Complement your existing team composition")


def exhaustive_search_example():
    """Demonstrate exhaustive search (only practical with required cookies)."""
    print("\n" + "="*70)
    print("EXHAUSTIVE SEARCH (GUARANTEED OPTIMAL)")
    print("="*70)

    optimizer = TeamOptimizer('crk-cookies.csv')

    print("\n⚠️  Exhaustive search without requirements = 138M+ combinations!")
    print("   We'll use 3 required cookies to reduce search space.\n")

    print("🔍 Finding THE BEST team that includes:")
    print("   - Mystic Flour Cookie (Beast, Healer)")
    print("   - Burning Spice Cookie (Beast, Tank)")
    print("   - Shadow Milk Cookie (Beast, DPS)")
    print("\n   This reduces search to C(174, 2) = 15,051 combinations")
    print("-"*70)

    start_time = time.time()

    # This will generate ALL possible 2-cookie combinations to fill the team
    best_teams = optimizer.find_best_teams(
        n=5,
        method='exhaustive',
        required_cookies=['Mystic Flour Cookie', 'Burning Spice Cookie', 'Shadow Milk Cookie']
    )

    elapsed = time.time() - start_time

    if best_teams:
        print(f"\n✅ Exhaustive search complete in {elapsed:.2f}s")
        print(f"\n🏆 Top 5 GUARANTEED OPTIMAL Teams:")

        for rank, team in enumerate(best_teams, 1):
            print(f"\n--- Rank #{rank} (Score: {team.composition_score:.1f}/100) ---")
            required_names = {'Mystic Flour Cookie', 'Burning Spice Cookie', 'Shadow Milk Cookie'}

            for i, cookie in enumerate(team.cookies, 1):
                marker = "🔒" if cookie.name in required_names else "➕"
                print(f"   {marker} {cookie.name} ({cookie.role}, {cookie.position}) - Power: {cookie.get_power_score():.1f}")

        print("\n💡 Exhaustive search guarantees these are the BEST possible teams!")


def practical_use_case():
    """Realistic scenario: User wants to build around their best cookie."""
    print("\n" + "="*70)
    print("PRACTICAL USE CASE: 'I just got Shadow Milk Cookie!'")
    print("="*70)

    optimizer = TeamOptimizer('crk-cookies.csv')

    print("\n📖 Scenario:")
    print("   You just pulled Shadow Milk Cookie (Beast-tier DPS) and want to")
    print("   build the strongest possible team around them.\n")

    print("🎯 Goal: Find top 5 team compositions featuring Shadow Milk Cookie")
    print("-"*70)

    best_teams = optimizer.find_best_teams(
        n=5,
        method='genetic',
        num_candidates=100,
        required_cookies=['Shadow Milk Cookie']
    )

    if best_teams:
        print(f"\n🏆 Top 5 Team Compositions:\n")

        for rank, team in enumerate(best_teams, 1):
            print(f"#{rank} - Score: {team.composition_score:.1f}/100")
            print(f"    Roles: {', '.join(team.get_role_distribution().keys())}")

            # Show non-Shadow Milk cookies
            teammates = [c for c in team.cookies if c.name != 'Shadow Milk Cookie']
            print(f"    Pair with: {', '.join(c.name for c in teammates)}")
            print()

        print("💡 Tips:")
        print("   - All teams include a tank and healer for balance")
        print("   - Role diversity ensures tactical flexibility")
        print("   - Position coverage prevents vulnerability to ambush attacks")


if __name__ == "__main__":
    # Run all examples
    compare_optimization_methods()
    build_around_cookie_example()
    exhaustive_search_example()
    practical_use_case()

    print("\n" + "="*70)
    print("✅ All optimization examples complete!")
    print("\n📚 Summary of Methods:")
    print("   - Random: Fast, good for exploration")
    print("   - Greedy: Fast, focuses on high-power cookies")
    print("   - Genetic: Slower, often finds better solutions")
    print("   - Exhaustive: Guaranteed optimal (only with required cookies)")
    print("\n💡 For build-around scenarios, use genetic with 50-100 generations!")
    print("="*70)
