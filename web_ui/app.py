"""
Flask Web Application for Cookie Run: Kingdom Team Optimizer

A beautiful web interface for visualizing and generating optimal cookie teams.
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add parent directory to path to import team_optimizer
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from team_optimizer import TeamOptimizer, Cookie

app = Flask(__name__)

# Initialize optimizer (CSV is in parent directory)
csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'crk-cookies.csv')
optimizer = TeamOptimizer(csv_path)

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


@app.route('/')
def index():
    """Render the main page."""
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
            'power': round(cookie.get_power_score(), 2),
            'color': RARITY_COLORS.get(cookie.rarity, '#808080')
        })

    # Sort by power descending
    cookies_data.sort(key=lambda x: x['power'], reverse=True)

    return jsonify(cookies_data)


@app.route('/api/optimize', methods=['POST'])
def optimize_teams():
    """Generate optimized teams based on user parameters."""
    data = request.json

    method = data.get('method', 'random')
    num_candidates = data.get('numCandidates', 1000)
    top_n = data.get('topN', 5)
    required_cookies = data.get('requiredCookies', [])
    cookie_stats = data.get('cookieStats', {})  # New: cookie stats

    # Validate inputs
    if num_candidates > 10000:
        return jsonify({'error': 'Maximum 10,000 candidates allowed'}), 400

    if top_n > 50:
        return jsonify({'error': 'Maximum 50 teams allowed'}), 400

    try:
        # Update cookie stats if provided
        if cookie_stats:
            optimizer.update_cookie_stats(cookie_stats)

        # Generate teams
        teams = optimizer.find_best_teams(
            n=top_n,
            method=method,
            num_candidates=num_candidates,
            required_cookies=required_cookies if required_cookies else None
        )

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
                'hasHealer': team.has_healer()
            }

            for cookie in team.cookies:
                team_dict['cookies'].append({
                    'name': cookie.name,
                    'rarity': cookie.rarity,
                    'role': cookie.role,
                    'position': cookie.position,
                    'power': round(cookie.get_power_score(), 2),
                    'color': RARITY_COLORS.get(cookie.rarity, '#808080'),
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
