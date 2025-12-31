// ==================== GLOBAL STATE ====================
let allCookies = [];
let selectedCookies = [];
let enemySelectedCookies = [];
let cookieStats = {};
let currentEditingCookie = null;
let currentToppings = [];

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadCookies();
    updateMethodDescription(); // Set initial description
});

// ==================== EVENT LISTENERS ====================
function setupEventListeners() {
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    // Team Optimizer tab
    document.getElementById('optimizeBtn').addEventListener('click', optimizeTeams);
    document.getElementById('cookieSearch').addEventListener('input', filterCookies);
    document.getElementById('rarityFilter').addEventListener('change', filterCookies);
    document.getElementById('roleFilter').addEventListener('change', filterCookies);
    document.getElementById('positionFilter').addEventListener('change', filterCookies);
    document.getElementById('excludeAscended').addEventListener('change', handleExcludeAscendedChange);
    document.getElementById('method').addEventListener('change', updateMethodDescription);

    // Counter-Team tab
    document.getElementById('generateCounterBtn').addEventListener('click', generateCounterTeams);
    document.getElementById('enemyCookieSearch').addEventListener('input', filterEnemyCookies);
    document.getElementById('enemyRarityFilter').addEventListener('change', filterEnemyCookies);
    document.getElementById('enemyRoleFilter').addEventListener('change', filterEnemyCookies);

    // Cookie Manager tab
    document.getElementById('managerCookieSearch').addEventListener('input', filterManagerCookies);
    document.getElementById('managerRarityFilter').addEventListener('change', filterManagerCookies);
    document.getElementById('statsFilterSelect').addEventListener('change', filterManagerCookies);
    document.getElementById('clearAllStatsBtn').addEventListener('click', clearAllStats);
}

// ==================== TAB SWITCHING ====================
function switchTab(tabId) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.closest('.tab-btn').classList.add('active');

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(tabId).classList.add('active');
}

// ==================== EXCLUDE ASCENDED HANDLER ====================
function handleExcludeAscendedChange() {
    // Refresh all cookie lists
    filterCookies();
    filterEnemyCookies();
    filterManagerCookies();

    // Remove Ascended cookies from selected
    const excludeAscended = document.getElementById('excludeAscended').checked;
    if (excludeAscended) {
        selectedCookies = selectedCookies.filter(c => !c.rarity.includes('Ascended'));
        updateSelectedCookiesDisplay();

        enemySelectedCookies = enemySelectedCookies.filter(c => !c.rarity.includes('Ascended'));
        updateEnemySelectedCookiesDisplay();
    }
}

// ==================== METHOD DESCRIPTION UPDATE ====================
function updateMethodDescription() {
    const method = document.getElementById('method').value;
    const descriptionEl = document.getElementById('methodDescription');

    const descriptions = {
        'random': 'Fast exploration, generates diverse teams quickly. Good for browsing options. (⚡⚡⚡ Speed)',
        'greedy': 'Prioritizes highest-rarity cookies first. Power-focused approach. Good for raw strength. (⚡⚡⚡ Speed)',
        'genetic': 'Evolutionary algorithm that optimizes team composition over generations. Best overall results (92-96/100 scores). Recommended for most users. (⚡⚡ Speed)',
        'exhaustive': 'Tests ALL possible combinations. Guaranteed optimal, but slow. Only use with 3+ required cookies selected. (⚡ Speed varies)'
    };

    descriptionEl.textContent = descriptions[method] || '';
}

// ==================== COOKIE LOADING ====================
async function loadCookies() {
    try {
        const response = await fetch('/api/cookies');
        allCookies = await response.json();

        // Initial display
        displayCookieGrid(allCookies, 'cookieGrid', 'team-optimizer');
        displayCookieGrid(allCookies, 'enemyCookieGrid', 'counter-team');
        displayCookieGrid(allCookies, 'managerCookieGrid', 'cookie-manager');

        updateStatsCount();
    } catch (error) {
        console.error('Error loading cookies:', error);
    }
}

// ==================== COOKIE GRID DISPLAY ====================
function displayCookieGrid(cookies, gridId, tabContext) {
    const grid = document.getElementById(gridId);
    grid.innerHTML = '';

    cookies.forEach(cookie => {
        const card = document.createElement('div');
        card.className = 'cookie-card';

        // Check if cookie is selected
        const isSelected = (tabContext === 'team-optimizer' && selectedCookies.some(c => c.name === cookie.name)) ||
                          (tabContext === 'counter-team' && enemySelectedCookies.some(c => c.name === cookie.name));

        if (isSelected) {
            card.classList.add('selected');
        }

        // Check if cookie has stats
        if (cookieStats[cookie.name]) {
            card.classList.add('has-stats');
        }

        card.innerHTML = `
            <div class="cookie-icon">
                <img src="${cookie.image_url}"
                     alt="${cookie.name}"
                     onerror="this.style.display='none'; this.parentElement.textContent='🍪';">
            </div>
            <div class="cookie-name">${cookie.name}</div>
            <div class="cookie-meta">${cookie.role} • ${cookie.position}</div>
            <div class="cookie-rarity-badge" style="background-color: ${cookie.color}"></div>
        `;

        // Click handlers based on tab
        if (tabContext === 'team-optimizer') {
            card.addEventListener('click', () => toggleCookieSelection(cookie));
        } else if (tabContext === 'counter-team') {
            card.addEventListener('click', () => toggleEnemyCookieSelection(cookie));
        } else if (tabContext === 'cookie-manager') {
            card.addEventListener('click', () => openStatsPanel(cookie));
        }

        grid.appendChild(card);
    });
}

// ==================== COOKIE SELECTION (TEAM OPTIMIZER) ====================
function toggleCookieSelection(cookie) {
    const index = selectedCookies.findIndex(c => c.name === cookie.name);

    if (index > -1) {
        selectedCookies.splice(index, 1);
    } else {
        if (selectedCookies.length < 5) {
            selectedCookies.push(cookie);
        } else {
            alert('Maximum 5 cookies allowed!');
            return;
        }
    }

    updateSelectedCookiesDisplay();
    filterCookies(); // Refresh to update selection state
}

function updateSelectedCookiesDisplay() {
    const container = document.getElementById('selectedCookies');

    if (selectedCookies.length === 0) {
        container.innerHTML = '<p class="empty-state">None selected</p>';
        return;
    }

    container.innerHTML = selectedCookies.map(cookie => `
        <div class="selected-cookie-chip">
            <span>${cookie.name}</span>
            <button class="chip-remove" onclick="removeCookie('${cookie.name.replace(/'/g, "\\'")}')">×</button>
        </div>
    `).join('');
}

function removeCookie(cookieName) {
    selectedCookies = selectedCookies.filter(c => c.name !== cookieName);
    updateSelectedCookiesDisplay();
    filterCookies();
}

// ==================== ENEMY COOKIE SELECTION (COUNTER-TEAM) ====================
function toggleEnemyCookieSelection(cookie) {
    const index = enemySelectedCookies.findIndex(c => c.name === cookie.name);

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

    updateEnemySelectedCookiesDisplay();
    filterEnemyCookies();
}

function updateEnemySelectedCookiesDisplay() {
    const container = document.getElementById('enemySelectedCookies');

    if (enemySelectedCookies.length === 0) {
        container.innerHTML = '<p class="empty-state">Select 5 cookies</p>';
        return;
    }

    container.innerHTML = enemySelectedCookies.map(cookie => `
        <div class="selected-cookie-chip">
            <span>${cookie.name}</span>
            <button class="chip-remove" onclick="removeEnemyCookie('${cookie.name.replace(/'/g, "\\'")}')">×</button>
        </div>
    `).join('');
}

function removeEnemyCookie(cookieName) {
    enemySelectedCookies = enemySelectedCookies.filter(c => c.name !== cookieName);
    updateEnemySelectedCookiesDisplay();
    filterEnemyCookies();
}

// ==================== FILTERING ====================
function filterCookies() {
    const searchTerm = document.getElementById('cookieSearch').value.toLowerCase();
    const rarityFilter = document.getElementById('rarityFilter').value;
    const roleFilter = document.getElementById('roleFilter').value;
    const positionFilter = document.getElementById('positionFilter').value;
    const excludeAscended = document.getElementById('excludeAscended').checked;

    let filtered = allCookies.filter(cookie => {
        const matchesSearch = cookie.name.toLowerCase().includes(searchTerm);
        const matchesRarity = !rarityFilter || cookie.rarity === rarityFilter;
        const matchesRole = !roleFilter || cookie.role === roleFilter;
        const matchesPosition = !positionFilter || cookie.position === positionFilter;
        const notAscended = !excludeAscended || !cookie.rarity.includes('Ascended');

        return matchesSearch && matchesRarity && matchesRole && matchesPosition && notAscended;
    });

    displayCookieGrid(filtered, 'cookieGrid', 'team-optimizer');
}

function filterEnemyCookies() {
    const searchTerm = document.getElementById('enemyCookieSearch').value.toLowerCase();
    const rarityFilter = document.getElementById('enemyRarityFilter').value;
    const roleFilter = document.getElementById('enemyRoleFilter').value;
    const excludeAscended = document.getElementById('excludeAscended').checked;

    let filtered = allCookies.filter(cookie => {
        const matchesSearch = cookie.name.toLowerCase().includes(searchTerm);
        const matchesRarity = !rarityFilter || cookie.rarity === rarityFilter;
        const matchesRole = !roleFilter || cookie.role === roleFilter;
        const notAscended = !excludeAscended || !cookie.rarity.includes('Ascended');

        return matchesSearch && matchesRarity && matchesRole && notAscended;
    });

    displayCookieGrid(filtered, 'enemyCookieGrid', 'counter-team');
}

function filterManagerCookies() {
    const searchTerm = document.getElementById('managerCookieSearch').value.toLowerCase();
    const rarityFilter = document.getElementById('managerRarityFilter').value;
    const statsFilter = document.getElementById('statsFilterSelect').value;

    let filtered = allCookies.filter(cookie => {
        const matchesSearch = cookie.name.toLowerCase().includes(searchTerm);
        const matchesRarity = !rarityFilter || cookie.rarity === rarityFilter;

        let matchesStats = true;
        if (statsFilter === 'with-stats') {
            matchesStats = cookieStats[cookie.name] !== undefined;
        } else if (statsFilter === 'without-stats') {
            matchesStats = cookieStats[cookie.name] === undefined;
        }

        return matchesSearch && matchesRarity && matchesStats;
    });

    displayCookieGrid(filtered, 'managerCookieGrid', 'cookie-manager');
}

// ==================== TEAM OPTIMIZATION ====================
async function optimizeTeams() {
    const method = document.getElementById('method').value;
    const numCandidates = parseInt(document.getElementById('numCandidates').value);
    const topN = parseInt(document.getElementById('topN').value);

    // Show loading
    document.getElementById('loadingIndicator').style.display = 'flex';

    try {
        const response = await fetch('/api/optimize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                method: method,
                numCandidates: numCandidates,
                topN: topN,
                requiredCookies: selectedCookies.map(c => c.name),
                cookieStats: cookieStats
            })
        });

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Optimization failed');
        }

        displayTeamResults(data.teams);
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        document.getElementById('loadingIndicator').style.display = 'none';
    }
}

function displayTeamResults(teams) {
    const resultsSection = document.getElementById('resultsSection');
    const teamsList = document.getElementById('teamsList');

    resultsSection.style.display = 'block';
    teamsList.innerHTML = '';

    teams.forEach((team, index) => {
        const item = createTeamAccordionItem(team, index);
        teamsList.appendChild(item);
    });

    // Auto-expand first team
    if (teams.length > 0) {
        const firstHeader = teamsList.querySelector('.team-accordion-header');
        const firstBody = teamsList.querySelector('.team-accordion-body');
        firstHeader.classList.add('active');
        firstBody.classList.add('expanded');
    }
}

function createTeamAccordionItem(team, index) {
    const div = document.createElement('div');
    div.className = 'team-accordion-item';

    div.innerHTML = `
        <div class="team-accordion-header" onclick="toggleAccordion(this)">
            <div class="team-accordion-title">Team #${index + 1}</div>
            <div class="team-accordion-score">Score: ${team.score}</div>
            <div class="team-accordion-icon">▼</div>
        </div>
        <div class="team-accordion-body">
            <div class="team-accordion-content">
                <div class="team-cookies-grid">
                    ${team.cookies.map(cookie => `
                        <div class="team-cookie-mini">
                            <div class="cookie-icon">
                                <img src="${cookie.image_url || ''}"
                                     alt="${cookie.name}"
                                     onerror="this.style.display='none'; this.parentElement.textContent='🍪';">
                            </div>
                            <div class="cookie-name">${cookie.name}</div>
                            <div class="cookie-rarity-badge" style="background-color: ${cookie.color}"></div>
                        </div>
                    `).join('')}
                </div>
                <div class="team-stats">
                    <div class="team-stat-item">
                        <span class="team-stat-label">Roles:</span>
                        <span class="team-stat-value">${Object.entries(team.roleDistribution).map(([k,v]) => `${k}:${v}`).join(', ')}</span>
                    </div>
                    <div class="team-stat-item">
                        <span class="team-stat-label">Positions:</span>
                        <span class="team-stat-value">${Object.entries(team.positionDistribution).map(([k,v]) => `${k}:${v}`).join(', ')}</span>
                    </div>
                    <div class="team-stat-item">
                        <span class="team-stat-label">Has Tank:</span>
                        <span class="team-stat-value">${team.hasTank ? '✓' : '✗'}</span>
                    </div>
                    <div class="team-stat-item">
                        <span class="team-stat-label">Has Healer:</span>
                        <span class="team-stat-value">${team.hasHealer ? '✓' : '✗'}</span>
                    </div>
                </div>
            </div>
        </div>
    `;

    return div;
}

function toggleAccordion(header) {
    const body = header.nextElementSibling;
    const isActive = header.classList.contains('active');

    header.classList.toggle('active');
    body.classList.toggle('expanded');
}

// ==================== COUNTER-TEAM GENERATION ====================
async function generateCounterTeams() {
    if (enemySelectedCookies.length !== 5) {
        alert('Please select exactly 5 enemy cookies!');
        return;
    }

    const method = document.getElementById('counterMethod').value;
    const numCounterTeams = parseInt(document.getElementById('numCounterTeams').value);

    document.getElementById('loadingIndicator').style.display = 'flex';

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
            throw new Error(data.error || 'Counter-team generation failed');
        }

        displayCounterResults(data);
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        document.getElementById('loadingIndicator').style.display = 'none';
    }
}

function displayCounterResults(data) {
    const resultsSection = document.getElementById('counterResultsSection');
    const teamsList = document.getElementById('counterTeamsList');

    resultsSection.style.display = 'block';
    teamsList.innerHTML = '';

    data.counterTeams.forEach((teamData, index) => {
        const item = createCounterTeamAccordionItem(teamData, index);
        teamsList.appendChild(item);
    });

    // Auto-expand first team
    if (data.counterTeams.length > 0) {
        const firstHeader = teamsList.querySelector('.team-accordion-header');
        const firstBody = teamsList.querySelector('.team-accordion-body');
        firstHeader.classList.add('active');
        firstBody.classList.add('expanded');
    }
}

function createCounterTeamAccordionItem(teamData, index) {
    const div = document.createElement('div');
    div.className = 'team-accordion-item';

    div.innerHTML = `
        <div class="team-accordion-header" onclick="toggleAccordion(this)">
            <div class="team-accordion-title">Counter-Team #${index + 1}</div>
            <div class="team-accordion-score">Combined: ${teamData.combinedScore}/100</div>
            <div class="team-accordion-icon">▼</div>
        </div>
        <div class="team-accordion-body">
            <div class="team-accordion-content">
                <p style="margin-bottom: 15px;"><strong>Strategy:</strong> ${teamData.strategy}</p>
                <div class="team-cookies-grid">
                    ${teamData.cookies.map(cookie => `
                        <div class="team-cookie-mini">
                            <div class="cookie-icon">
                                <img src="${cookie.image_url || ''}"
                                     alt="${cookie.name}"
                                     onerror="this.style.display='none'; this.parentElement.textContent='🍪';">
                            </div>
                            <div class="cookie-name">${cookie.name}</div>
                            <div class="cookie-rarity-badge" style="background-color: ${cookie.color}"></div>
                        </div>
                    `).join('')}
                </div>
                ${teamData.recommendedTreasures && teamData.recommendedTreasures.length > 0 ? `
                    <div style="margin-top: 20px;">
                        <strong>🎁 Recommended Treasures:</strong>
                        ${teamData.recommendedTreasures.map(t => `
                            <div style="margin: 10px 0; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px;">
                                <strong>${t.name}</strong> (${t.tier}) - ${t.reason}
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
            </div>
        </div>
    `;

    return div;
}

// ==================== STATS PANEL ====================
function openStatsPanel(cookie) {
    currentEditingCookie = cookie;
    const panel = document.getElementById('statsPanel');

    // Update panel content
    document.getElementById('statsCookieName').textContent = cookie.name;
    document.getElementById('statsCookieInfo').innerHTML = `
        <div><strong>Rarity:</strong> ${cookie.rarity}</div>
        <div><strong>Role:</strong> ${cookie.role}</div>
        <div><strong>Position:</strong> ${cookie.position}</div>
        <div><strong>Power:</strong> ${cookie.power}</div>
    `;

    // Load existing stats if available
    if (cookieStats[cookie.name]) {
        const stats = cookieStats[cookie.name];
        document.getElementById('statsCookieLevel').value = stats.cookie_level || 90;
        document.getElementById('statsSkillLevel').value = stats.skill_level || 90;
        document.getElementById('statsStarLevel').value = stats.star_level !== undefined ? stats.star_level : 5;
        currentToppings = stats.toppings || [];
    } else {
        document.getElementById('statsCookieLevel').value = 90;
        document.getElementById('statsSkillLevel').value = 90;
        document.getElementById('statsStarLevel').value = 5;
        currentToppings = [];
    }

    renderToppings();

    // Open panel
    panel.classList.add('open');
}

function closeStatsPanel() {
    document.getElementById('statsPanel').classList.remove('open');
    currentEditingCookie = null;
    currentToppings = [];
}

function saveStatsPanel() {
    if (!currentEditingCookie) return;

    const cookieLevel = parseInt(document.getElementById('statsCookieLevel').value);
    const skillLevel = parseInt(document.getElementById('statsSkillLevel').value);
    const starLevel = parseInt(document.getElementById('statsStarLevel').value);
    const addToRequired = document.getElementById('statsAddToRequired').checked;

    // Calculate topping quality
    let toppingQuality = 0;
    if (currentToppings.length > 0) {
        const avgLevel = currentToppings.reduce((sum, t) => sum + t.level, 0) / currentToppings.length;
        toppingQuality = (avgLevel / 12) * 5;
    }

    cookieStats[currentEditingCookie.name] = {
        cookie_level: cookieLevel,
        skill_level: skillLevel,
        star_level: starLevel,
        topping_quality: toppingQuality,
        toppings: [...currentToppings]
    };

    updateStatsCount();

    // Add to required if checked
    if (addToRequired && !selectedCookies.some(c => c.name === currentEditingCookie.name)) {
        if (selectedCookies.length < 5) {
            selectedCookies.push(currentEditingCookie);
            updateSelectedCookiesDisplay();
        }
    }

    // Refresh manager grid
    filterManagerCookies();

    closeStatsPanel();
}

function deleteStatsPanel() {
    if (!currentEditingCookie) return;

    if (confirm(`Delete stats for ${currentEditingCookie.name}?`)) {
        delete cookieStats[currentEditingCookie.name];
        updateStatsCount();
        filterManagerCookies();
        closeStatsPanel();
    }
}

function renderToppings() {
    const container = document.getElementById('statsToppingsContainer');
    container.innerHTML = currentToppings.map((topping, index) => `
        <div class="topping-slot">
            <select class="input-field" onchange="updateTopping(${index}, 'type', this.value)" style="margin-bottom: 5px;">
                <option value="Swift Chocolate" ${topping.type === 'Swift Chocolate' ? 'selected' : ''}>Swift Chocolate</option>
                <option value="Solid Almond" ${topping.type === 'Solid Almond' ? 'selected' : ''}>Solid Almond</option>
                <option value="Searing Raspberry" ${topping.type === 'Searing Raspberry' ? 'selected' : ''}>Searing Raspberry</option>
                <option value="Bouncy Caramel" ${topping.type === 'Bouncy Caramel' ? 'selected' : ''}>Bouncy Caramel</option>
                <option value="Healthy Peanut" ${topping.type === 'Healthy Peanut' ? 'selected' : ''}>Healthy Peanut</option>
                <option value="Fresh Apple Jelly" ${topping.type === 'Fresh Apple Jelly' ? 'selected' : ''}>Fresh Apple Jelly</option>
            </select>
            <input type="number" class="input-field" placeholder="Level (0-12)" value="${topping.level}"
                   min="0" max="12" onchange="updateTopping(${index}, 'level', parseInt(this.value))">
            <button class="btn-secondary" onclick="removeTopping(${index})" style="margin-top: 5px;">Remove</button>
        </div>
    `).join('');
}

function addToppingSlot() {
    if (currentToppings.length < 5) {
        currentToppings.push({ type: 'Swift Chocolate', level: 12 });
        renderToppings();
    } else {
        alert('Maximum 5 toppings allowed!');
    }
}

function updateTopping(index, field, value) {
    currentToppings[index][field] = value;
}

function removeTopping(index) {
    currentToppings.splice(index, 1);
    renderToppings();
}

function updateStatsCount() {
    const count = Object.keys(cookieStats).length;
    document.getElementById('statsCount').innerHTML = `<strong>${count}</strong> cookies with stats`;
}

function clearAllStats() {
    if (confirm('Delete all cookie stats? This cannot be undone.')) {
        cookieStats = {};
        updateStatsCount();
        filterManagerCookies();
    }
}
