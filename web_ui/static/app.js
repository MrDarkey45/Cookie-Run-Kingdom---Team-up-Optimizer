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
    document.getElementById('excludeAscended').addEventListener('change', handleExcludeAscendedChange);

    // Counter-team generator listeners
    document.getElementById('generateCounterBtn').addEventListener('click', generateCounterTeams);
    document.getElementById('enemyCookieSearch').addEventListener('input', filterEnemyCookies);
}

// Handle exclude ascended checkbox change
function handleExcludeAscendedChange() {
    // Refresh the cookie list to filter out Ascended cookies
    filterCookies({ target: document.getElementById('cookieSearch') });

    // Remove any Ascended cookies from selected cookies
    const excludeAscended = document.getElementById('excludeAscended').checked;
    if (excludeAscended) {
        selectedCookies = selectedCookies.filter(c => !c.rarity.includes('Ascended'));
        updateSelectedCookies();
    }
}

// Load all available cookies
async function loadCookies() {
    try {
        const response = await fetch('/api/cookies');
        allCookies = await response.json();
        displayCookieList(allCookies);
        displayEnemyCookieList(allCookies); // Also populate enemy cookie list
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

        // Check if cookie has stats
        const hasStats = cookieStats[cookie.name] !== undefined;
        cookieItem.className = hasStats ? 'cookie-item has-stats' : 'cookie-item';

        // Get element display
        const elementDisplay = cookie.element && cookie.element !== 'N/A' ?
            `• ${cookie.element}` : '';

        // Stats badge if stats exist
        const statsBadge = hasStats ? '<div class="stats-badge">⚡ STATS</div>' : '';

        cookieItem.innerHTML = `
            ${statsBadge}
            <div class="cookie-info">
                <div class="cookie-rarity-badge" style="background-color: ${cookie.color}"></div>
                <div>
                    <div class="cookie-name">${cookie.name}</div>
                    <div class="cookie-meta">${cookie.role} • ${cookie.position} ${elementDisplay}</div>
                </div>
            </div>
            <button class="btn-add" onclick="event.stopPropagation(); toggleCookie('${cookie.name.replace(/'/g, "\\'")}')">+</button>
        `;

        // Make entire cookie item clickable
        cookieItem.addEventListener('click', () => toggleCookie(cookie.name));

        cookieList.appendChild(cookieItem);
    });
}

// Filter cookies based on search
function filterCookies(event) {
    const searchTerm = event.target.value.toLowerCase();
    const excludeAscended = document.getElementById('excludeAscended').checked;

    let filtered = allCookies.filter(cookie =>
        cookie.name.toLowerCase().includes(searchTerm) ||
        cookie.role.toLowerCase().includes(searchTerm) ||
        cookie.position.toLowerCase().includes(searchTerm) ||
        (cookie.element && cookie.element.toLowerCase().includes(searchTerm))
    );

    // Filter out Ascended cookies if checkbox is checked
    if (excludeAscended) {
        filtered = filtered.filter(cookie => !cookie.rarity.includes('Ascended'));
    }

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
    const excludeAscended = document.getElementById('excludeAscended').checked;

    if (searchTerm.length === 0) {
        resultsContainer.innerHTML = '';
        resultsContainer.style.display = 'none';
        return;
    }

    let filtered = allCookies.filter(cookie =>
        cookie.name.toLowerCase().includes(searchTerm) ||
        cookie.role.toLowerCase().includes(searchTerm) ||
        cookie.rarity.toLowerCase().includes(searchTerm)
    );

    // Filter out Ascended cookies if checkbox is checked
    if (excludeAscended) {
        filtered = filtered.filter(cookie => !cookie.rarity.includes('Ascended'));
    }

    filtered = filtered.slice(0, 10); // Limit to 10 results

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
    const addToRequired = document.getElementById('addToRequired').checked;

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

    // Add to required cookies if checkbox is checked
    if (addToRequired) {
        const alreadyRequired = selectedCookies.find(c => c.name === currentEditingCookie.name);
        if (!alreadyRequired) {
            if (selectedCookies.length < 5) {
                selectedCookies.push(currentEditingCookie);
                updateSelectedCookies();
            }
        }
    }

    // Refresh cookie list to show stats badge
    filterCookies({ target: document.getElementById('cookieSearch') });

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

        // Refresh cookie list to remove stats badge
        filterCookies({ target: document.getElementById('cookieSearch') });
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

// ==============================================
// COUNTER-TEAM GENERATOR
// ==============================================

let enemySelectedCookies = [];

// Display enemy cookie list
function displayEnemyCookieList(cookies) {
    const cookieList = document.getElementById('enemyCookieList');
    cookieList.innerHTML = '';

    cookies.forEach(cookie => {
        const cookieItem = document.createElement('div');
        cookieItem.className = 'cookie-item';

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
            <button class="btn-add" onclick="event.stopPropagation(); toggleEnemyCookie('${cookie.name.replace(/'/g, "\\'")}')">+</button>
        `;

        cookieItem.addEventListener('click', () => toggleEnemyCookie(cookie.name));
        cookieList.appendChild(cookieItem);
    });
}

// Filter enemy cookies based on search
function filterEnemyCookies(event) {
    const searchTerm = event.target.value.toLowerCase();
    const excludeAscended = document.getElementById('excludeAscended').checked;

    let filtered = allCookies.filter(cookie =>
        cookie.name.toLowerCase().includes(searchTerm) ||
        cookie.role.toLowerCase().includes(searchTerm) ||
        cookie.position.toLowerCase().includes(searchTerm) ||
        (cookie.element && cookie.element.toLowerCase().includes(searchTerm))
    );

    if (excludeAscended) {
        filtered = filtered.filter(cookie => !cookie.rarity.includes('Ascended'));
    }

    displayEnemyCookieList(filtered);
}

// Toggle enemy cookie selection
function toggleEnemyCookie(cookieName) {
    const cookie = allCookies.find(c => c.name === cookieName);
    if (!cookie) return;

    const index = enemySelectedCookies.findIndex(c => c.name === cookieName);

    if (index > -1) {
        enemySelectedCookies.splice(index, 1);
    } else {
        if (enemySelectedCookies.length < 5) {
            enemySelectedCookies.push(cookie);
        } else {
            alert('Maximum 5 enemy cookies allowed!');
            return;
        }
    }

    updateEnemySelectedCookies();
}

// Update enemy selected cookies display
function updateEnemySelectedCookies() {
    const container = document.getElementById('enemySelectedCookies');

    if (enemySelectedCookies.length === 0) {
        container.innerHTML = '<p class="no-selection">No enemy cookies selected</p>';
        return;
    }

    container.innerHTML = enemySelectedCookies.map(cookie => `
        <div class="selected-cookie-item">
            <div class="selected-cookie-info">
                <div class="cookie-rarity-badge" style="background-color: ${cookie.color}"></div>
                <span class="cookie-name">${cookie.name}</span>
            </div>
            <button class="btn-remove" onclick="toggleEnemyCookie('${cookie.name.replace(/'/g, "\\'")}')">×</button>
        </div>
    `).join('');
}

// Generate counter-teams
async function generateCounterTeams() {
    if (enemySelectedCookies.length !== 5) {
        alert('Please select exactly 5 enemy cookies to generate counter-teams!');
        return;
    }

    const method = document.getElementById('counterMethod').value;
    const numCounterTeams = parseInt(document.getElementById('numCounterTeams').value);

    const counterResultsSection = document.getElementById('counterResultsSection');
    counterResultsSection.style.display = 'block';
    counterResultsSection.innerHTML = '<div class="loading-indicator"><div class="spinner"></div><p>Analyzing enemy team and generating counters...</p></div>';

    try {
        const response = await fetch('/api/counter-teams', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                enemyTeam: enemySelectedCookies.map(c => c.name),
                numCounterTeams: numCounterTeams,
                method: method,
                requiredCookies: []
            })
        });

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Failed to generate counter-teams');
        }

        displayCounterResults(data);
    } catch (error) {
        counterResultsSection.innerHTML = `<div class="error-message">❌ Error: ${error.message}</div>`;
    }
}

// Display counter-team results
function displayCounterResults(data) {
    const counterResultsSection = document.getElementById('counterResultsSection');
    counterResultsSection.style.display = 'block';

    let html = `
        <div class="results-header">
            <h3>⚔️ Counter-Team Analysis</h3>
            <div class="results-stats">Found ${data.counterTeams.length} counter-teams • ${data.weaknesses.length} weaknesses identified</div>
        </div>

        <!-- Enemy Team Display -->
        <div class="enemy-team-display">
            <h4>🎯 Enemy Team</h4>
            <div class="cookies-grid">
                ${enemySelectedCookies.map(cookie => `
                    <div class="cookie-card">
                        <div class="cookie-card-header">
                            <div class="cookie-rarity-badge" style="background-color: ${cookie.color}"></div>
                            <h4>${cookie.name}</h4>
                        </div>
                        <div class="cookie-card-body">
                            <p><strong>Role:</strong> ${cookie.role}</p>
                            <p><strong>Position:</strong> ${cookie.position}</p>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- Enemy Analysis -->
        <div class="enemy-analysis-section">
            <h4>📊 Enemy Composition Analysis</h4>
            <div class="analysis-grid">
                <div class="analysis-item">
                    <span class="analysis-label">Healers:</span>
                    <span class="analysis-value">${data.enemyAnalysis.healers}</span>
                </div>
                <div class="analysis-item">
                    <span class="analysis-label">Tanks:</span>
                    <span class="analysis-value">${data.enemyAnalysis.tanks}</span>
                </div>
                <div class="analysis-item">
                    <span class="analysis-label">DPS:</span>
                    <span class="analysis-value">${data.enemyAnalysis.dpsCount}</span>
                </div>
                <div class="analysis-item">
                    <span class="analysis-label">Front:</span>
                    <span class="analysis-value">${data.enemyAnalysis.frontPosition}</span>
                </div>
                <div class="analysis-item">
                    <span class="analysis-label">Middle:</span>
                    <span class="analysis-value">${data.enemyAnalysis.middlePosition}</span>
                </div>
                <div class="analysis-item">
                    <span class="analysis-label">Rear:</span>
                    <span class="analysis-value">${data.enemyAnalysis.rearPosition}</span>
                </div>
                ${data.enemyAnalysis.hasShadowMilk ? '<div class="analysis-item critical"><span class="analysis-label">⚠️ Has Shadow Milk!</span></div>' : ''}
                ${data.enemyAnalysis.beastCookies > 0 ? `<div class="analysis-item"><span class="analysis-label">Beast Cookies:</span><span class="analysis-value">${data.enemyAnalysis.beastCookies}</span></div>` : ''}
            </div>
        </div>

        <!-- Weaknesses -->
        <div class="weaknesses-section">
            <h4>⚠️ Weaknesses Identified (${data.weaknesses.length})</h4>
            <div class="weaknesses-list">
                ${data.weaknesses.map(weakness => `
                    <div class="weakness-card priority-${weakness.priority.toLowerCase()}">
                        <div class="weakness-header">
                            <span class="weakness-title">${weakness.weakness}</span>
                            <span class="weakness-confidence">${weakness.confidence}% confidence</span>
                        </div>
                        <p class="weakness-description">${weakness.description}</p>
                        <p class="weakness-exploit"><strong>Exploit:</strong> ${weakness.exploit}</p>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- Counter Strategy -->
        <div class="counter-strategy-section">
            <h4>🎯 Recommended Counter Strategy</h4>
            <div class="strategy-card">
                <div class="strategy-header">
                    <span class="strategy-archetype">${data.counterStrategy.teamArchetype}</span>
                    <span class="strategy-confidence">${data.counterStrategy.confidence}% confidence</span>
                </div>
                <p class="strategy-description">${data.counterStrategy.description}</p>
                ${data.counterStrategy.recommendedCookies.length > 0 ? `
                    <div class="recommended-cookies">
                        <strong>Recommended Cookies:</strong>
                        <div class="cookie-tags">
                            ${data.counterStrategy.recommendedCookies.slice(0, 10).map(name => `<span class="cookie-tag">${name}</span>`).join('')}
                        </div>
                    </div>
                ` : ''}
            </div>
        </div>

        <!-- Counter Teams -->
        <h4>🏆 Top Counter-Teams</h4>
        <div class="teams-list">
            ${data.counterTeams.map((teamData, index) => renderCounterTeam(teamData, index + 1)).join('')}
        </div>
    `;

    counterResultsSection.innerHTML = html;
}

// Render individual counter-team card
function renderCounterTeam(teamData, rank) {
    const roleLabels = {
        'Charge': '🛡️', 'Defense': '🛡️', 'Magic': '✨', 'Healing': '💚',
        'Support': '🎵', 'Ranged': '🏹', 'Bomber': '💣', 'Ambush': '🗡️'
    };

    return `
        <div class="team-card">
            <div class="team-header">
                <div class="team-rank">#${rank}</div>
                <div class="team-scores">
                    <span class="team-score">Counter: ${teamData.counterScore}/100</span>
                    <span class="team-score">Team: ${teamData.score}/120</span>
                    <span class="team-score combined">Combined: ${teamData.combinedScore}/100</span>
                </div>
            </div>

            <div class="counter-strategy-tag">${teamData.strategy}</div>

            ${teamData.priorityTargets.length > 0 ? `
                <div class="priority-targets">
                    <strong>🎯 Priority Targets:</strong> ${teamData.priorityTargets.join(', ')}
                </div>
            ` : ''}

            <div class="cookies-grid">
                ${teamData.cookies.map(cookie => `
                    <div class="cookie-card">
                        <div class="cookie-card-header">
                            <div class="cookie-rarity-badge" style="background-color: ${cookie.color}"></div>
                            <h4>${cookie.name}</h4>
                        </div>
                        <div class="cookie-card-body">
                            <p><strong>Role:</strong> ${roleLabels[cookie.role] || ''} ${cookie.role}</p>
                            <p><strong>Position:</strong> ${cookie.position}</p>
                            ${cookie.element !== 'N/A' ? `<p><strong>Element:</strong> ${cookie.element}</p>` : ''}
                            <p><strong>Power:</strong> ${cookie.power}</p>
                        </div>
                    </div>
                `).join('')}
            </div>

            <div class="team-stats">
                <div class="stat-row">
                    <span class="stat-label">Roles:</span>
                    <span class="stat-value">${Object.entries(teamData.roleDistribution).map(([role, count]) => `${roleLabels[role] || ''} ${role}: ${count}`).join(', ')}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Positions:</span>
                    <span class="stat-value">${Object.entries(teamData.positionDistribution).map(([pos, count]) => `${pos}: ${count}`).join(', ')}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Weaknesses Exploited:</span>
                    <span class="stat-value">${teamData.weaknessesExploited}</span>
                </div>
            </div>

            ${teamData.synergy && teamData.synergy.total_score ? renderSynergyBreakdown(teamData.synergy) : ''}
        </div>
    `;
}
