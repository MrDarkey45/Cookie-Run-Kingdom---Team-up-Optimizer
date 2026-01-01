"""
Flask Web Application for Cookie Run: Kingdom Team Optimizer

A beautiful web interface for visualizing and generating optimal cookie teams.
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add parent directory to path to import team_optimizer
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from team_optimizer import TeamOptimizer, Cookie, Team
from counter_team_generator import CounterTeamGenerator
from guild_battle_optimizer import GuildBattleOptimizer
from cookie_images import get_cookie_image_url

app = Flask(__name__)

# Initialize optimizer (CSV is in parent directory)
csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'crk-cookies.csv')
optimizer = TeamOptimizer(csv_path)

# Initialize counter-team generator
counter_generator = CounterTeamGenerator(optimizer)
guild_optimizer = GuildBattleOptimizer(optimizer)

# Rarity color mapping for UI
RARITY_COLORS = {
    'Beast': '#ff0066',
    'Ancient (Ascended)': '#ffd700',
    'Ancient': '#ffaa00',
    'Legendary': '#9966ff',
    'Dragon': '#ff6600',
    'Super Epic': '#ff1493',
    'Epic': '#9370db',
    'Special': '#4169e1',
    'Rare': '#32cd32',
    'Common': '#808080'
}

# Rarity hierarchy for filtering
RARITY_ORDER = [
    'Common',
    'Rare',
    'Special',
    'Epic',
    'Super Epic',
    'Legendary',
    'Dragon',
    'Ancient',
    'Ancient (Ascended)',
    'Beast'
]

def filter_cookies_by_max_rarity(cookies, max_rarity):
    """Filter cookies to only include those at or below max_rarity."""
    if not max_rarity:
        return cookies

    try:
        max_index = RARITY_ORDER.index(max_rarity)
        return [c for c in cookies if RARITY_ORDER.index(c.rarity) <= max_index]
    except ValueError:
        # If rarity not in list, return all cookies
        return cookies


@app.route('/')
def index():
    """Render the main page (new v2 UI)."""
    return render_template('index_v2.html')

@app.route('/v1')
def index_v1():
    """Render the old v1 UI (fallback)."""
    return render_template('index.html')


@app.route('/api/cookies')
def get_cookies():
    """Get list of all available cookies."""
    cookies_data = []
    for cookie in optimizer.all_cookies:
        cookies_data.append({
            'name': cookie.name,
            'rarity': cookie.rarity,
            'role': cookie.role,
            'position': cookie.position,
            'element': cookie.element if hasattr(cookie, 'element') else None,
            'synergyGroups': cookie.synergy_groups if hasattr(cookie, 'synergy_groups') else [],
            'specialCombos': cookie.special_combos if hasattr(cookie, 'special_combos') else [],
            'power': round(cookie.get_power_score(), 2),
            'color': RARITY_COLORS.get(cookie.rarity, '#808080'),
            'image_url': get_cookie_image_url(cookie.name)
        })

    # Sort by power descending
    cookies_data.sort(key=lambda x: x['power'], reverse=True)

    return jsonify(cookies_data)


@app.route('/api/treasures')
def get_treasures():
    """Get list of all available treasures."""
    treasures_data = []
    for treasure in optimizer.all_treasures:
        treasures_data.append({
            'name': treasure.name,
            'rarity': treasure.rarity,
            'activation_type': treasure.activation_type,
            'tier_ranking': treasure.tier_ranking,
            'effect_category': treasure.effect_category,
            'primary_effect': treasure.primary_effect,
            'atk_boost': treasure.atk_boost_max,
            'crit_boost': treasure.crit_boost_max,
            'cooldown_reduction': treasure.cooldown_reduction_max,
            'dmg_resist': treasure.dmg_resist_max,
            'hp_shield': treasure.hp_shield_max,
            'heal': treasure.heal_max,
            'revive': treasure.revive,
            'debuff_cleanse': treasure.debuff_cleanse,
            'enemy_debuff': treasure.enemy_debuff,
            'summon_boost': treasure.summon_boost,
            'recommended_archetypes': treasure.recommended_archetypes,
            'cooldown_seconds': treasure.cooldown_seconds,
            'special_condition': treasure.special_condition,
            'power_score': round(treasure.get_power_score(), 2)
        })

    # Sort by tier ranking (S+ → S → A → B → C)
    tier_order = {'S+': 0, 'S': 1, 'A': 2, 'B': 3, 'C': 4}
    treasures_data.sort(key=lambda x: tier_order.get(x['tier_ranking'], 99))

    return jsonify(treasures_data)


@app.route('/api/optimize', methods=['POST'])
def optimize_teams():
    """Generate optimized teams based on user parameters."""
    data = request.json

    method = data.get('method', 'random')
    num_candidates = data.get('numCandidates', 1000)
    top_n = data.get('topN', 5)
    required_cookies = data.get('requiredCookies', [])
    cookie_stats = data.get('cookieStats', {})
    max_rarity = data.get('maxRarity', '')

    # Validate inputs
    if num_candidates > 10000:
        return jsonify({'error': 'Maximum 10,000 candidates allowed'}), 400

    if top_n > 50:
        return jsonify({'error': 'Maximum 50 teams allowed'}), 400

    try:
        # Update cookie stats if provided
        if cookie_stats:
            optimizer.update_cookie_stats(cookie_stats)

        # Apply max rarity filter if specified
        original_cookies = optimizer.all_cookies
        if max_rarity:
            optimizer.all_cookies = filter_cookies_by_max_rarity(original_cookies, max_rarity)

        # Generate teams
        teams = optimizer.find_best_teams(
            n=top_n,
            method=method,
            num_candidates=num_candidates,
            required_cookies=required_cookies if required_cookies else None
        )

        # Restore original cookies list
        if max_rarity:
            optimizer.all_cookies = original_cookies

        # Convert to JSON-friendly format
        teams_data = []
        for i, team in enumerate(teams, 1):
            team_dict = {
                'rank': i,
                'score': round(team.composition_score, 1),
                'cookies': [],
                'roleDistribution': team.get_role_distribution(),
                'positionDistribution': team.get_position_distribution(),
                'hasTank': team.has_tank(),
                'hasHealer': team.has_healer(),
                # Add advanced synergy data
                'advancedSynergy': {
                    'totalSynergy': round(team.total_synergy_score, 2),
                    'elementSynergy': round(team.element_synergy_score, 2),
                    'groupSynergy': round(team.group_synergy_score, 2),
                    'specialCombo': round(team.special_combo_score, 2)
                }
            }

            for cookie in team.cookies:
                team_dict['cookies'].append({
                    'name': cookie.name,
                    'rarity': cookie.rarity,
                    'role': cookie.role,
                    'position': cookie.position,
                    'element': cookie.element if hasattr(cookie, 'element') else None,
                    'synergyGroups': cookie.synergy_groups if hasattr(cookie, 'synergy_groups') else [],
                    'specialCombos': cookie.special_combos if hasattr(cookie, 'special_combos') else [],
                    'power': round(cookie.get_power_score(), 2),
                    'color': RARITY_COLORS.get(cookie.rarity, '#808080'),
                    'image_url': get_cookie_image_url(cookie.name),
                    'isRequired': cookie.name in (required_cookies or [])
                })

            teams_data.append(team_dict)

        return jsonify({
            'success': True,
            'teams': teams_data,
            'totalGenerated': num_candidates if method != 'exhaustive' else 'All combinations'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/cookie/<cookie_name>')
def get_cookie_details(cookie_name):
    """Get detailed information about a specific cookie."""
    cookie = next((c for c in optimizer.all_cookies if c.name == cookie_name), None)

    if not cookie:
        return jsonify({'error': 'Cookie not found'}), 404

    return jsonify({
        'name': cookie.name,
        'rarity': cookie.rarity,
        'role': cookie.role,
        'position': cookie.position,
        'power': round(cookie.get_power_score(), 2),
        'color': RARITY_COLORS.get(cookie.rarity, '#808080')
    })


@app.route('/api/stats')
def get_stats():
    """Get overall statistics about the cookie collection."""
    from collections import Counter

    rarity_counts = Counter(c.rarity for c in optimizer.all_cookies)
    role_counts = Counter(c.role for c in optimizer.all_cookies)
    position_counts = Counter(c.position for c in optimizer.all_cookies)

    return jsonify({
        'totalCookies': len(optimizer.all_cookies),
        'rarityDistribution': dict(rarity_counts),
        'roleDistribution': dict(role_counts),
        'positionDistribution': dict(position_counts),
        'averagePower': round(sum(c.get_power_score() for c in optimizer.all_cookies) / len(optimizer.all_cookies), 2)
    })


@app.route('/api/counter-teams', methods=['POST'])
def generate_counter_teams():
    """Generate counter-teams against an enemy team composition."""
    try:
        data = request.json
        enemy_cookie_names = data.get('enemyTeam', [])
        num_counter_teams = data.get('numCounterTeams', 5)
        method = data.get('method', 'random')
        required_cookies = data.get('requiredCookies', [])
        max_rarity = data.get('maxRarity', '')

        # Validate enemy team
        if not enemy_cookie_names or len(enemy_cookie_names) < 1 or len(enemy_cookie_names) > 5:
            return jsonify({'error': 'Enemy team must have 1-5 cookies'}), 400

        # Build enemy team
        enemy_cookies = []
        for name in enemy_cookie_names:
            cookie = next((c for c in optimizer.all_cookies if c.name == name), None)
            if not cookie:
                return jsonify({'error': f'Cookie not found: {name}'}), 404
            enemy_cookies.append(cookie)

        enemy_team = Team(enemy_cookies, strict_validation=False)

        # Analyze enemy team
        analysis = counter_generator.analyze_enemy_team(enemy_team)
        weaknesses = counter_generator.identify_weaknesses(enemy_team)
        counter_strategy = counter_generator.generate_counter_strategies(enemy_team)

        # Apply max rarity filter if specified
        original_cookies = counter_generator.all_cookies
        if max_rarity:
            counter_generator.all_cookies = filter_cookies_by_max_rarity(original_cookies, max_rarity)

        # Generate counter-teams
        counter_teams = counter_generator.find_counter_teams(
            enemy_team,
            n=num_counter_teams,
            method=method,
            required_cookies=required_cookies if required_cookies else None
        )

        # Restore original cookies list
        if max_rarity:
            counter_generator.all_cookies = original_cookies

        # Format response
        counter_teams_data = []
        for team, counter_info in counter_teams:
            team_cookies = []
            for cookie in team.cookies:
                team_cookies.append({
                    'name': cookie.name,
                    'rarity': cookie.rarity,
                    'role': cookie.role,
                    'position': cookie.position,
                    'power': round(cookie.get_power_score(), 2),
                    'color': RARITY_COLORS.get(cookie.rarity, '#808080'),
                    'image_url': get_cookie_image_url(cookie.name),
                    'element': cookie.element if hasattr(cookie, 'element') and cookie.element else 'N/A'
                })

            # Get synergy breakdown if available (legacy system)
            synergy_data = {}
            if hasattr(team, 'synergy_breakdown') and team.synergy_breakdown:
                synergy_data = {
                    'total_score': round(team.synergy_score, 1),
                    'breakdown': {
                        'role_synergy': round(team.synergy_breakdown['role_synergy'], 1),
                        'position_synergy': round(team.synergy_breakdown['position_synergy'], 1),
                        'element_synergy': round(team.synergy_breakdown['element_synergy'], 1),
                        'type_synergy': round(team.synergy_breakdown['type_synergy'], 1),
                        'coverage_synergy': round(team.synergy_breakdown['coverage_synergy'], 1)
                    }
                }

            # Get advanced synergy data (new system)
            advanced_synergy = {
                'totalSynergy': round(team.total_synergy_score, 2),
                'elementSynergy': round(team.element_synergy_score, 2),
                'groupSynergy': round(team.group_synergy_score, 2),
                'specialCombo': round(team.special_combo_score, 2)
            }

            counter_teams_data.append({
                'cookies': team_cookies,
                'score': round(team.composition_score, 2),
                'counterScore': round(counter_info['counter_score'], 1),
                'combinedScore': round(counter_info['combined_score'], 1),
                'strategy': counter_info['strategy'],
                'priorityTargets': counter_info['priority_targets'],
                'weaknessesExploited': len(counter_info['weaknesses_exploited']),
                'roleDistribution': team.get_role_distribution(),
                'positionDistribution': team.get_position_distribution(),
                'synergy': synergy_data,
                'advancedSynergy': advanced_synergy,
                'recommendedTreasures': counter_info.get('recommended_treasures', [])
            })

        # Format weaknesses
        weaknesses_data = [{
            'weakness': w['weakness'],
            'description': w['description'],
            'exploit': w['exploit'],
            'priority': w['priority'],
            'confidence': w['confidence']
        } for w in weaknesses]

        return jsonify({
            'success': True,
            'enemyAnalysis': {
                'healers': analysis['healers'],
                'tanks': analysis['tanks'],
                'dpsCount': analysis['dps_count'],
                'frontPosition': analysis['front_position'],
                'middlePosition': analysis['middle_position'],
                'rearPosition': analysis['rear_position'],
                'hasShadowMilk': analysis['has_shadow_milk'],
                'beastCookies': analysis['beast_cookies']
            },
            'weaknesses': weaknesses_data,
            'counterStrategy': {
                'recommendedCookies': counter_strategy['recommended_cookies'],
                'avoidCookies': counter_strategy['avoid_cookies'],
                'description': counter_strategy['strategy_description'],
                'teamArchetype': counter_strategy['team_archetype'],
                'confidence': counter_strategy['confidence']
            },
            'counterTeams': counter_teams_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/guild-battle', methods=['POST'])
def generate_guild_battle_teams():
    """API endpoint for Guild Battle team generation."""
    try:
        data = request.get_json()
        boss_name = data.get('boss')
        required_cookie_names = data.get('requiredCookies', [])
        num_teams = data.get('numTeams', 5)
        prioritize_s_tier = data.get('prioritizeSTier', True)

        # Validate boss
        if not boss_name:
            return jsonify({'error': 'Boss name is required'}), 400

        # Get boss info
        boss_info = guild_optimizer.get_boss_info(boss_name)
        if not boss_info:
            return jsonify({'error': f'Unknown boss: {boss_name}'}), 400

        # Generate teams
        teams_data = guild_optimizer.generate_guild_battle_team(
            boss_name=boss_name,
            required_cookies=required_cookie_names,
            num_teams=num_teams,
            prioritize_s_tier=prioritize_s_tier
        )

        # Format response
        guild_teams = []
        for team_info in teams_data:
            team = team_info['team']

            team_cookies = []
            for cookie in team.cookies:
                team_cookies.append({
                    'name': cookie.name,
                    'rarity': cookie.rarity,
                    'role': cookie.role,
                    'position': cookie.position,
                    'power': round(cookie.get_power_score(), 2),
                    'color': RARITY_COLORS.get(cookie.rarity, '#808080'),
                    'image_url': get_cookie_image_url(cookie.name),
                    'element': cookie.element if hasattr(cookie, 'element') and cookie.element else 'N/A'
                })

            guild_teams.append({
                'cookies': team_cookies,
                'score': round(team_info['score'], 2),
                'strategy': team_info['strategy'],
                'roleDistribution': team.get_role_distribution(),
                'positionDistribution': team.get_position_distribution(),
                'advancedSynergy': {
                    'totalSynergy': round(team.total_synergy_score, 2),
                    'elementSynergy': round(team.element_synergy_score, 2),
                    'groupSynergy': round(team.group_synergy_score, 2),
                    'specialCombo': round(team.special_combo_score, 2)
                }
            })

        return jsonify({
            'success': True,
            'boss': boss_name,
            'bossInfo': {
                'description': boss_info['description'],
                'mechanics': boss_info['mechanics'],
                'strategy': boss_info['strategy'],
                'sTierCookies': boss_info['s_tier_cookies'],
                'aTierCookies': boss_info['a_tier_cookies']
            },
            'teams': guild_teams
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)

    print("="*70)
    print("🍪 Cookie Run: Kingdom Team Optimizer Web UI")
    print("="*70)
    print("\n🌐 Server starting at: http://127.0.0.1:5000")
    print("📊 Open your browser and navigate to the URL above")
    print("\nPress Ctrl+C to stop the server")
    print("="*70 + "\n")

    app.run(debug=True, host='127.0.0.1', port=5000)
