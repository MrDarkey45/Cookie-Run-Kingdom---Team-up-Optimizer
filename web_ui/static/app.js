// Cookie Run: Kingdom Team Optimizer - Frontend JavaScript (Updated)

let allCookies = [];
let selectedCookies = [];
let cookieStats = {};  // Stores cookie stats with detailed topping info
let currentEditingCookie = null;
let currentToppings = [];

// Topping types available in the game
const TOPPING_TYPES = [
    'Solid Almond',
    'Searing Raspberry',
    'Swift Chocolate',
    'Bouncy Caramel',
    'Healthy Peanut'
];

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadCookies();
    loadStats();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    document.getElementById('optimizeBtn').addEventListener('click', optimizeTeams);
    document.getElementById('cookieSearch').addEventListener('input', filterCookies);
    document.getElementById('method').addEventListener('change', updateMethodHelp);
    document.getElementById('addStatsBtn').addEventListener('click', openCookieStatsModal);
    document.getElementById('modalCookieSearch').addEventListener('input', handleModalSearch);
}

// Load all available cookies
async function loadCookies() {
    try {
        const response = await fetch('/api/cookies');
        allCookies = await response.json();
        displayCookieList(allCookies);
    } catch (error) {
        console.error('Error loading cookies:', error);
    }
}

// Display cookie list in the scrollable container
function displayCookieList(cookies) {
    const cookieList = document.getElementById('cookieList');
    cookieList.innerHTML = '';

    cookies.forEach(cookie => {
        const cookieItem = document.createElement('div');
        cookieItem.className = 'cookie-item';

        // Get element display
        const elementDisplay = cookie.element && cookie.element !== 'N/A' ?
            `• ${cookie.element}` : '';

        cookieItem.innerHTML = `
            <div class="cookie-info">
                <div class="cookie-rarity-badge" style="background-color: ${cookie.color}"></div>
                <div>
                    <div class="cookie-name">${cookie.name}</div>
                    <div class="cookie-meta">${cookie.role} • ${cookie.position} ${elementDisplay}</div>
                </div>
            </div>
            <button class="btn-add" onclick="toggleCookie('${cookie.name.replace(/'/g, "\\'")}')">+</button>
        `;

        cookieList.appendChild(cookieItem);
    });
}

// Filter cookies based on search
function filterCookies(event) {
    const searchTerm = event.target.value.toLowerCase();
    const filtered = allCookies.filter(cookie =>
        cookie.name.toLowerCase().includes(searchTerm) ||
        cookie.role.toLowerCase().includes(searchTerm) ||
        cookie.position.toLowerCase().includes(searchTerm) ||
        (cookie.element && cookie.element.toLowerCase().includes(searchTerm))
    );
    displayCookieList(filtered);
}

// Toggle cookie selection for required cookies
function toggleCookie(cookieName) {
    const cookie = allCookies.find(c => c.name === cookieName);
    if (!cookie) return;

    const index = selectedCookies.findIndex(c => c.name === cookieName);

    if (index > -1) {
        selectedCookies.splice(index, 1);
    } else {
        if (selectedCookies.length >= 5) {
            alert('Maximum 5 cookies can be required!');
            return;
        }
        selectedCookies.push(cookie);
    }

    updateSelectedCookies();
}

// Update selected cookies display
function updateSelectedCookies() {
    const container = document.getElementById('selectedCookies');

    if (selectedCookies.length === 0) {
        container.innerHTML = '<p class="no-selection">No cookies selected - will optimize all combinations</p>';
        return;
    }

    container.innerHTML = selectedCookies.map(cookie => `
        <div class="selected-cookie-tag" style="border-left: 4px solid ${cookie.color}">
            <span>${cookie.name}</span>
            <span class="remove-cookie" onclick="removeCookie('${cookie.name.replace(/'/g, "\\'")}')">×</span>
        </div>
    `).join('');
}

// Remove cookie from selection
function removeCookie(cookieName) {
    selectedCookies = selectedCookies.filter(c => c.name !== cookieName);
    updateSelectedCookies();
}

// Update method help text
function updateMethodHelp() {
    const method = document.getElementById('method').value;
    const helpTexts = {
        random: 'Fast exploration, diverse results',
        greedy: 'Power-focused, consistent results',
        genetic: 'Best quality, recommended ⭐',
        exhaustive: 'Guaranteed optimal (requires 3+ cookies)'
    };

    console.log('Method selected:', method, '-', helpTexts[method]);
}

// ==============================================
// COOKIE STATS MODAL FUNCTIONS
// ==============================================

function openCookieStatsModal() {
    document.getElementById('cookieStatsModal').style.display = 'flex';
    document.getElementById('modalCookieSearch').value = '';
    document.getElementById('cookieSearchResults').innerHTML = '';
    document.getElementById('cookieStatsForm').style.display = 'none';
    currentEditingCookie = null;
    currentToppings = [];
}

function closeCookieStatsModal() {
    document.getElementById('cookieStatsModal').style.display = 'none';
    resetStatsForm();
}

function resetStatsForm() {
    document.getElementById('cookieLevel').value = 90;
    document.getElementById('skillLevel').value = 90;
    document.getElementById('toppingsContainer').innerHTML = '';
    currentToppings = [];
    currentEditingCookie = null;
}

// Handle modal search with autocomplete
function handleModalSearch(event) {
    const searchTerm = event.target.value.toLowerCase();
    const resultsContainer = document.getElementById('cookieSearchResults');

    if (searchTerm.length === 0) {
        resultsContainer.innerHTML = '';
        resultsContainer.style.display = 'none';
        return;
    }

    const filtered = allCookies.filter(cookie =>
        cookie.name.toLowerCase().includes(searchTerm) ||
        cookie.role.toLowerCase().includes(searchTerm) ||
        cookie.rarity.toLowerCase().includes(searchTerm)
    ).slice(0, 10); // Limit to 10 results

    if (filtered.length === 0) {
        resultsContainer.innerHTML = '<div class="cookie-search-result-item">No cookies found</div>';
        resultsContainer.style.display = 'block';
        return;
    }

    resultsContainer.innerHTML = filtered.map(cookie => {
        const elementDisplay = cookie.element && cookie.element !== 'N/A' ?
            ` • ${cookie.element}` : '';
        return `
            <div class="cookie-search-result-item" onclick="selectCookieForStats('${cookie.name.replace(/'/g, "\\'")}')">
                <div class="cookie-name">${cookie.name}</div>
                <div class="cookie-meta" style="font-size: 0.85rem; opacity: 0.7;">
                    ${cookie.rarity} • ${cookie.role}${elementDisplay}
                </div>
            </div>
        `;
    }).join('');

    resultsContainer.style.display = 'block';
}

// Select a cookie from search results to add stats
function selectCookieForStats(cookieName) {
    const cookie = allCookies.find(c => c.name === cookieName);
    if (!cookie) return;

    currentEditingCookie = cookie;

    // Hide search results
    document.getElementById('cookieSearchResults').innerHTML = '';
    document.getElementById('cookieSearchResults').style.display = 'none';
    document.getElementById('modalCookieSearch').value = '';

    // Show form
    document.getElementById('cookieStatsForm').style.display = 'block';
    document.getElementById('selectedCookieName').textContent = cookie.name;

    const elementDisplay = cookie.element && cookie.element !== 'N/A' ?
        ` • ${cookie.element}` : '';
    document.getElementById('selectedCookieInfo').textContent =
        `${cookie.rarity} • ${cookie.role} • ${cookie.position}${elementDisplay}`;

    // Load existing stats if available
    if (cookieStats[cookie.name]) {
        const stats = cookieStats[cookie.name];
        document.getElementById('cookieLevel').value = stats.cookie_level || 90;
        document.getElementById('skillLevel').value = stats.skill_level || 90;
        currentToppings = stats.toppings || [];
    } else {
        document.getElementById('cookieLevel').value = 90;
        document.getElementById('skillLevel').value = 90;
        currentToppings = [];
    }

    renderToppings();
}

// Add a topping slot
function addToppingSlot() {
    if (currentToppings.length >= 5) {
        alert('Maximum 5 toppings allowed!');
        return;
    }

    currentToppings.push({
        type: TOPPING_TYPES[0],
        level: 12
    });

    renderToppings();
}

// Remove a topping slot
function removeToppingSlot(index) {
    currentToppings.splice(index, 1);
    renderToppings();
}

// Update topping data
function updateTopping(index, field, value) {
    if (currentToppings[index]) {
        currentToppings[index][field] = field === 'level' ? parseInt(value) : value;
    }
}

// Render toppings UI
function renderToppings() {
    const container = document.getElementById('toppingsContainer');

    if (currentToppings.length === 0) {
        container.innerHTML = '<p style="opacity: 0.5; font-style: italic; text-align: center;">No toppings added yet</p>';
    } else {
        container.innerHTML = currentToppings.map((topping, index) => `
            <div class="topping-slot">
                <select onchange="updateTopping(${index}, 'type', this.value)">
                    ${TOPPING_TYPES.map(type => `
                        <option value="${type}" ${topping.type === type ? 'selected' : ''}>${type}</option>
                    `).join('')}
                </select>
                <input type="number"
                       value="${topping.level}"
                       min="0"
                       max="12"
                       onchange="updateTopping(${index}, 'level', this.value)"
                       placeholder="Level">
                <button class="btn-remove-topping" onclick="removeToppingSlot(${index})">✕</button>
            </div>
        `).join('');
    }

    // Update add button state
    const addButton = document.querySelector('.btn-add-topping');
    if (addButton) {
        addButton.disabled = currentToppings.length >= 5;
    }
}

// Save cookie stats
function saveCookieStats() {
    if (!currentEditingCookie) return;

    const cookieLevel = parseInt(document.getElementById('cookieLevel').value);
    const skillLevel = parseInt(document.getElementById('skillLevel').value);

    // Calculate average topping quality (0-5 scale) from detailed toppings
    let toppingQuality = 0;
    if (currentToppings.length > 0) {
        const avgLevel = currentToppings.reduce((sum, t) => sum + t.level, 0) / currentToppings.length;
        toppingQuality = (avgLevel / 12) * 5; // Convert 0-12 to 0-5 scale
    }

    cookieStats[currentEditingCookie.name] = {
        cookie_level: cookieLevel,
        skill_level: skillLevel,
        topping_quality: toppingQuality,
        toppings: [...currentToppings] // Store detailed topping info
    };

    updateStatsSummary();
    closeCookieStatsModal();
}

// Cancel stats editing
function cancelCookieStats() {
    closeCookieStatsModal();
}

// Update stats summary display
function updateStatsSummary() {
    const summary = document.getElementById('addedStatsSummary');
    const count = Object.keys(cookieStats).length;

    if (count === 0) {
        summary.innerHTML = '<p style="opacity: 0.5; font-style: italic; text-align: center;">No cookie stats added yet</p>';
        return;
    }

    summary.innerHTML = Object.entries(cookieStats).map(([name, stats]) => `
        <div class="stats-summary-item">
            <div class="stats-summary-info">
                <div class="stats-summary-name">${name}</div>
                <div class="stats-summary-details">
                    Lv${stats.cookie_level} • Skill ${stats.skill_level} • ${stats.toppings.length} Toppings
                </div>
            </div>
            <button class="btn-edit-stats" onclick="editCookieStats('${name.replace(/'/g, "\\'")}')">Edit</button>
            <button class="btn-delete-stats" onclick="deleteCookieStats('${name.replace(/'/g, "\\'")}')">Delete</button>
        </div>
    `).join('');
}

// Edit existing cookie stats
function editCookieStats(cookieName) {
    selectCookieForStats(cookieName);
    openCookieStatsModal();
}

// Delete cookie stats
function deleteCookieStats(cookieName) {
    if (confirm(`Delete stats for ${cookieName}?`)) {
        delete cookieStats[cookieName];
        updateStatsSummary();
    }
}

// ==============================================
// TEAM OPTIMIZATION
// ==============================================

async function optimizeTeams() {
    const method = document.getElementById('method').value;
    const numCandidates = parseInt(document.getElementById('numCandidates').value);
    const topN = parseInt(document.getElementById('topN').value);

    // Validation
    if (method === 'exhaustive' && selectedCookies.length < 3) {
        alert('Exhaustive search requires at least 3 required cookies to be practical!');
        return;
    }

    // Show loading
    document.getElementById('loadingIndicator').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';

    try {
        const response = await fetch('/api/optimize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                method: method,
                numCandidates: numCandidates,
                topN: topN,
                requiredCookies: selectedCookies.map(c => c.name),
                cookieStats: cookieStats  // Include detailed cookie stats
            })
        });

        const data = await response.json();

        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        displayResults(data);
    } catch (error) {
        console.error('Error optimizing teams:', error);
        alert('Failed to optimize teams. Please try again.');
    } finally {
        document.getElementById('loadingIndicator').style.display = 'none';
    }
}

// Display optimization results with synergy breakdown
function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsStats = document.getElementById('resultsStats');
    const teamsList = document.getElementById('teamsList');

    // Update stats
    resultsStats.innerHTML = `
        Generated ${data.totalGenerated} teams •
        Showing top ${data.teams.length} results
    `;

    // Display teams with synergy breakdown
    teamsList.innerHTML = data.teams.map(team => `
        <div class="team-card">
            <div class="team-header">
                <div class="team-rank">#${team.rank}</div>
                <div class="team-score">${team.score}/120</div>
            </div>

            <div class="cookies-grid">
                ${team.cookies.map(cookie => `
                    <div class="cookie-card ${cookie.isRequired ? 'required' : ''}">
                        ${cookie.isRequired ? '<div class="required-badge">REQUIRED</div>' : ''}
                        <div class="cookie-rarity-badge" style="background-color: ${cookie.color}; width: 40px; height: 40px; margin: 0 auto; border-radius: 50%;"></div>
                        <h4>${cookie.name}</h4>
                        <div class="cookie-card-rarity" style="color: ${cookie.color}">${cookie.rarity}</div>
                        <div class="cookie-card-role">${cookie.role} • ${cookie.position}</div>
                        ${cookie.element && cookie.element !== 'null' ? `<div class="cookie-card-role" style="color: var(--accent-color);">✨ ${cookie.element}</div>` : ''}
                        <div class="cookie-card-power">⚡ ${cookie.power}</div>
                    </div>
                `).join('')}
            </div>

            <div class="team-stats">
                <div class="stat-box">
                    <h5>Role Diversity</h5>
                    <div class="stat-value">${Object.keys(team.roleDistribution).length}/5</div>
                </div>
                <div class="stat-box">
                    <h5>Position Coverage</h5>
                    <div class="stat-value">${Object.keys(team.positionDistribution).length}/3</div>
                </div>
                <div class="stat-box">
                    <h5>Has Tank</h5>
                    <div class="stat-value">${team.hasTank ? '<span class="stat-icon">✓</span>' : '<span class="stat-icon">✗</span>'}</div>
                </div>
                <div class="stat-box">
                    <h5>Has Healer</h5>
                    <div class="stat-value">${team.hasHealer ? '<span class="stat-icon">✓</span>' : '<span class="stat-icon">✗</span>'}</div>
                </div>
            </div>

            ${team.synergy ? renderSynergyBreakdown(team.synergy) : ''}
        </div>
    `).join('');

    resultsSection.style.display = 'block';

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Render synergy breakdown chart
function renderSynergyBreakdown(synergy) {
    const breakdown = synergy.breakdown;
    const maxValues = {
        role_synergy: 30,
        position_synergy: 20,
        element_synergy: 25,
        type_synergy: 15,
        coverage_synergy: 10
    };

    const labels = {
        role_synergy: '⚔️ Role Synergy',
        position_synergy: '📍 Position Synergy',
        element_synergy: '✨ Element Synergy',
        type_synergy: '🌟 Type Synergy',
        coverage_synergy: '🛡️ Coverage'
    };

    return `
        <div class="synergy-section">
            <h4>🔗 Team Synergy Analysis (${synergy.total_score}/100)</h4>
            <div class="synergy-bar-chart">
                ${Object.entries(breakdown).map(([key, value]) => {
                    const max = maxValues[key];
                    const percentage = (value / max) * 100;
                    return `
                        <div class="synergy-bar-item">
                            <div class="synergy-bar-label">
                                <span class="synergy-bar-label-text">${labels[key]}</span>
                                <span class="synergy-bar-value">${value.toFixed(1)}/${max}</span>
                            </div>
                            <div class="synergy-bar-track">
                                <div class="synergy-bar-fill" style="width: ${percentage}%"></div>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        </div>
    `;
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();

        const statsContent = document.getElementById('statsContent');
        statsContent.innerHTML = `
            <div class="stat-card">
                <h4>Total Cookies</h4>
                <div class="stat-number">${stats.totalCookies}</div>
            </div>
            <div class="stat-card">
                <h4>Average Power</h4>
                <div class="stat-number">${stats.averagePower}</div>
            </div>
            <div class="stat-card">
                <h4>Unique Roles</h4>
                <div class="stat-number">${Object.keys(stats.roleDistribution).length}</div>
            </div>
            <div class="stat-card">
                <h4>Beast/Ancient Cookies</h4>
                <div class="stat-number">${(stats.rarityDistribution['Beast'] || 0) + (stats.rarityDistribution['Ancient'] || 0)}</div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}
