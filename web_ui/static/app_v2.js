// ==================== GLOBAL STATE ====================
let allCookies = [];
let selectedCookies = [];
let enemySelectedCookies = [];
let cookieStats = {};
let currentEditingCookie = null;
let currentToppings = [];

// ==================== HELPER FUNCTIONS ====================
function getElementColor(element) {
    const elementColors = {
        'Light': 'linear-gradient(135deg, #fff9c4, #fff59d)',
        'Darkness': 'linear-gradient(135deg, #4a148c, #6a1b9a)',
        'Fire': 'linear-gradient(135deg, #ff6b6b, #ff5252)',
        'Water': 'linear-gradient(135deg, #4fc3f7, #29b6f6)',
        'Ice': 'linear-gradient(135deg, #b3e5fc, #81d4fa)',
        'Earth': 'linear-gradient(135deg, #8d6e63, #a1887f)',
        'Grass': 'linear-gradient(135deg, #66bb6a, #81c784)',
        'Wind': 'linear-gradient(135deg, #b2dfdb, #80cbc4)',
        'Electricity': 'linear-gradient(135deg, #ffd54f, #ffeb3b)',
        'Steel': 'linear-gradient(135deg, #90a4ae, #b0bec5)',
        'Poison': 'linear-gradient(135deg, #9c27b0, #ab47bc)'
    };
    return elementColors[element] || 'rgba(255, 255, 255, 0.1)';
}

function meetsMaxRarityConstraint(cookieRarity, maxRarity) {
    if (!maxRarity) return true; // No constraint if maxRarity is empty

    // Rarity hierarchy (from lowest to highest)
    const rarityOrder = [
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
    ];

    // Get indices
    const cookieIndex = rarityOrder.indexOf(cookieRarity);
    const maxIndex = rarityOrder.indexOf(maxRarity);

    // If either rarity not found, allow it (edge case)
    if (cookieIndex === -1 || maxIndex === -1) return true;

    // Cookie rarity must be less than or equal to max rarity
    return cookieIndex <= maxIndex;
}

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadCookies();
    updateMethodDescription(); // Set initial description
    initializeBookmarks(); // Initialize bookmarks system
});

// ==================== EVENT LISTENERS ====================
function setupEventListeners() {
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    // Bookmarks
    document.getElementById('toggleBookmarksBtn').addEventListener('click', toggleBookmarksPanel);

    // Team Optimizer tab
    document.getElementById('optimizeBtn').addEventListener('click', optimizeTeams);
    document.getElementById('resetOptimizerBtn').addEventListener('click', resetOptimizer);
    document.getElementById('cookieSearch').addEventListener('input', filterCookies);
    document.getElementById('rarityFilter').addEventListener('change', filterCookies);
    document.getElementById('roleFilter').addEventListener('change', filterCookies);
    document.getElementById('positionFilter').addEventListener('change', filterCookies);
    document.getElementById('maxRarity').addEventListener('change', filterCookies);
    document.getElementById('excludeAscended').addEventListener('change', handleExcludeAscendedChange);
    document.getElementById('method').addEventListener('change', updateMethodDescription);

    // Counter-Team tab
    document.getElementById('generateCounterBtn').addEventListener('click', generateCounterTeams);
    document.getElementById('resetCounterBtn').addEventListener('click', resetCounter);
    document.getElementById('enemyCookieSearch').addEventListener('input', filterEnemyCookies);
    document.getElementById('enemyRarityFilter').addEventListener('change', filterEnemyCookies);
    document.getElementById('enemyRoleFilter').addEventListener('change', filterEnemyCookies);
    document.getElementById('counterMaxRarity').addEventListener('change', filterEnemyCookies);

    // Guild Battle tab
    document.getElementById('guildBoss').addEventListener('change', updateBossInfo);
    document.getElementById('generateGuildBtn').addEventListener('click', generateGuildTeams);
    document.getElementById('resetGuildBtn').addEventListener('click', resetGuildBattle);
    document.getElementById('guildCookieSearch').addEventListener('input', loadGuildCookies);
    document.getElementById('guildRarityFilter').addEventListener('change', loadGuildCookies);
    document.getElementById('guildRoleFilter').addEventListener('change', loadGuildCookies);

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

    // Load tab-specific content
    if (tabId === 'guild-battle') {
        loadGuildCookies();
        updateBossInfo();
    }
}

// ==================== EXCLUDE ASCENDED HANDLER ====================
function handleExcludeAscendedChange() {
    // Refresh all cookie lists
    filterCookies();
    filterEnemyCookies();
    loadGuildCookies();
    filterManagerCookies();

    // Remove Ascended cookies from selected
    const excludeAscended = document.getElementById('excludeAscended').checked;
    if (excludeAscended) {
        selectedCookies = selectedCookies.filter(c => !c.rarity.includes('Ascended'));
        updateSelectedCookiesDisplay();

        enemySelectedCookies = enemySelectedCookies.filter(c => !c.rarity.includes('Ascended'));
        updateEnemySelectedCookiesDisplay();

        guildSelectedCookies = guildSelectedCookies.filter(c => !c.rarity.includes('Ascended'));
        updateGuildSelectedCookiesDisplay();
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
        'synergy': '🌟 NEW! Optimizes for synergy bonuses: special combos (Citrus Party, Team Drizzle), group synergies (Beast, Dragon, Ancient), and element matching. Best for thematic teams. (⚡⚡ Speed)',
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
        container.innerHTML = '<p class="empty-state">Select 1-5 enemy cookies</p>';
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
    const maxRarity = document.getElementById('maxRarity').value;

    let filtered = allCookies.filter(cookie => {
        const matchesSearch = cookie.name.toLowerCase().includes(searchTerm);
        const matchesRarity = !rarityFilter || cookie.rarity === rarityFilter;
        const matchesRole = !roleFilter || cookie.role === roleFilter;
        const matchesPosition = !positionFilter || cookie.position === positionFilter;
        const notAscended = !excludeAscended || !cookie.rarity.includes('Ascended');
        const meetsMaxRarity = meetsMaxRarityConstraint(cookie.rarity, maxRarity);

        return matchesSearch && matchesRarity && matchesRole && matchesPosition && notAscended && meetsMaxRarity;
    });

    displayCookieGrid(filtered, 'cookieGrid', 'team-optimizer');
}

function filterEnemyCookies() {
    const searchTerm = document.getElementById('enemyCookieSearch').value.toLowerCase();
    const rarityFilter = document.getElementById('enemyRarityFilter').value;
    const roleFilter = document.getElementById('enemyRoleFilter').value;
    const excludeAscended = document.getElementById('excludeAscended').checked;
    const maxRarity = document.getElementById('counterMaxRarity').value;

    let filtered = allCookies.filter(cookie => {
        const matchesSearch = cookie.name.toLowerCase().includes(searchTerm);
        const matchesRarity = !rarityFilter || cookie.rarity === rarityFilter;
        const matchesRole = !roleFilter || cookie.role === roleFilter;
        const notAscended = !excludeAscended || !cookie.rarity.includes('Ascended');
        const meetsMaxRarity = meetsMaxRarityConstraint(cookie.rarity, maxRarity);

        return matchesSearch && matchesRarity && matchesRole && notAscended && meetsMaxRarity;
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
    const maxRarity = document.getElementById('maxRarity').value;

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
                cookieStats: cookieStats,
                maxRarity: maxRarity
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

    // Save teams for bookmarking
    currentOptimizerTeams = { teams: teams };

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
            <button class="bookmark-team-btn" onclick="event.stopPropagation(); bookmarkTeam('optimizer', ${index}, this)" title="Bookmark this team">⭐</button>
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
                            ${cookie.element ? `<div class="cookie-element-badge" style="background: ${getElementColor(cookie.element)};">${cookie.element}</div>` : ''}
                            ${(cookie.synergyGroups && cookie.synergyGroups.length > 0) || (cookie.specialCombos && cookie.specialCombos.length > 0) ? `
                                <div class="cookie-synergy-tags">
                                    ${(cookie.synergyGroups || []).slice(0, 2).map(group => `<span class="synergy-tag">${group}</span>`).join('')}
                                    ${(cookie.specialCombos || []).map(combo => `<span class="synergy-tag special-combo-tag">★ ${combo}</span>`).join('')}
                                </div>
                            ` : ''}
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
                    ${team.advancedSynergy ? `
                        <div class="team-stat-item team-synergy-header">
                            <span class="team-stat-label">🌟 Advanced Synergy:</span>
                            <span class="team-stat-value synergy-total">${team.advancedSynergy.totalSynergy}/60</span>
                        </div>
                        <div class="team-synergy-breakdown">
                            <div class="synergy-bar-item">
                                <span class="synergy-label">🔥 Element Synergy:</span>
                                <div class="synergy-bar-container">
                                    <div class="synergy-bar" style="width: ${(team.advancedSynergy.elementSynergy / 15) * 100}%; background: linear-gradient(90deg, #ff6b6b, #ff8787);"></div>
                                    <span class="synergy-value">${team.advancedSynergy.elementSynergy}/15</span>
                                </div>
                            </div>
                            <div class="synergy-bar-item">
                                <span class="synergy-label">👥 Group Synergy:</span>
                                <div class="synergy-bar-container">
                                    <div class="synergy-bar" style="width: ${(team.advancedSynergy.groupSynergy / 20) * 100}%; background: linear-gradient(90deg, #4ecdc4, #5fd9d0);"></div>
                                    <span class="synergy-value">${team.advancedSynergy.groupSynergy}/20</span>
                                </div>
                            </div>
                            <div class="synergy-bar-item">
                                <span class="synergy-label">⭐ Special Combo:</span>
                                <div class="synergy-bar-container">
                                    <div class="synergy-bar" style="width: ${(team.advancedSynergy.specialCombo / 25) * 100}%; background: linear-gradient(90deg, #ffd93d, #ffe66d);"></div>
                                    <span class="synergy-value">${team.advancedSynergy.specialCombo}/25</span>
                                </div>
                            </div>
                        </div>
                    ` : ''}
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
    if (enemySelectedCookies.length < 1 || enemySelectedCookies.length > 5) {
        alert('Please select 1-5 enemy cookies!');
        return;
    }

    const method = document.getElementById('counterMethod').value;
    const numCounterTeams = parseInt(document.getElementById('numCounterTeams').value);
    const maxRarity = document.getElementById('counterMaxRarity').value;

    document.getElementById('loadingIndicator').style.display = 'flex';

    try {
        const response = await fetch('/api/counter-teams', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                enemyTeam: enemySelectedCookies.map(c => c.name),
                numCounterTeams: numCounterTeams,
                method: method,
                requiredCookies: [],
                maxRarity: maxRarity
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

    // Save teams for bookmarking
    currentCounterTeams = data;

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
            <button class="bookmark-team-btn" onclick="event.stopPropagation(); bookmarkTeam('counter', ${index}, this)" title="Bookmark this team">⭐</button>
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
                ${teamData.advancedSynergy ? `
                    <div class="team-stats" style="margin-top: 15px;">
                        <div class="team-stat-item team-synergy-header">
                            <span class="team-stat-label">🌟 Advanced Synergy:</span>
                            <span class="team-stat-value synergy-total">${teamData.advancedSynergy.totalSynergy}/60</span>
                        </div>
                        <div class="team-synergy-breakdown">
                            <div class="synergy-bar-item">
                                <span class="synergy-label">🔥 Element Synergy:</span>
                                <div class="synergy-bar-container">
                                    <div class="synergy-bar" style="width: ${(teamData.advancedSynergy.elementSynergy / 15) * 100}%; background: linear-gradient(90deg, #ff6b6b, #ff8787);"></div>
                                    <span class="synergy-value">${teamData.advancedSynergy.elementSynergy}/15</span>
                                </div>
                            </div>
                            <div class="synergy-bar-item">
                                <span class="synergy-label">👥 Group Synergy:</span>
                                <div class="synergy-bar-container">
                                    <div class="synergy-bar" style="width: ${(teamData.advancedSynergy.groupSynergy / 20) * 100}%; background: linear-gradient(90deg, #4ecdc4, #5fd9d0);"></div>
                                    <span class="synergy-value">${teamData.advancedSynergy.groupSynergy}/20</span>
                                </div>
                            </div>
                            <div class="synergy-bar-item">
                                <span class="synergy-label">⭐ Special Combo:</span>
                                <div class="synergy-bar-container">
                                    <div class="synergy-bar" style="width: ${(teamData.advancedSynergy.specialCombo / 25) * 100}%; background: linear-gradient(90deg, #ffd93d, #ffe66d);"></div>
                                    <span class="synergy-value">${teamData.advancedSynergy.specialCombo}/25</span>
                                </div>
                            </div>
                        </div>
                    </div>
                ` : ''}
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


// ==================== GUILD BATTLE ====================

let guildSelectedCookies = [];
const guildBosses = {
    'Red Velvet Dragon': {
        icon: '🐉',
        description: '75% damage reflection, high DEF. Prioritize DEF shred and indirect damage.'
    },
    'Avatar of Destiny': {
        icon: '👁️',
        description: 'Immune to debuffs (triggers Reversal). Use periodic damage, shields, and ATK SPD buffs.'
    },
    'Living Abyss': {
        icon: '🌊',
        description: '95% damage reduction on boss. Target ooze blobs with AOE damage and crowd control.'
    },
    'Machine-God of the Eternal Void': {
        icon: '⚙️',
        description: 'Water-element focus. Multi-part boss weak to water, immune to electric.'
    }
};

function updateBossInfo() {
    const boss = document.getElementById('guildBoss').value;
    const descEl = document.getElementById('bossDescription');

    if (guildBosses[boss]) {
        descEl.textContent = guildBosses[boss].description;
    }
}

function loadGuildCookies() {
    const grid = document.getElementById('guildCookieGrid');
    grid.innerHTML = '';

    const searchTerm = document.getElementById('guildCookieSearch').value.toLowerCase();
    const rarityFilter = document.getElementById('guildRarityFilter').value;
    const roleFilter = document.getElementById('guildRoleFilter').value;

    let filtered = allCookies.filter(cookie => {
        const matchesSearch = cookie.name.toLowerCase().includes(searchTerm);
        const matchesRarity = !rarityFilter || cookie.rarity === rarityFilter;
        const matchesRole = !roleFilter || cookie.role === roleFilter;
        return matchesSearch && matchesRarity && matchesRole;
    });

    filtered.forEach(cookie => {
        const isSelected = guildSelectedCookies.some(c => c.name === cookie.name);

        const card = document.createElement('div');
        card.className = `cookie-card` + (isSelected ? ' selected' : '');
        card.style.borderColor = cookie.color;

        card.innerHTML = `
            <div class="cookie-icon">
                <img src="` + cookie.image_url + `"
                     alt="` + cookie.name + `"
                     onerror="this.style.display='none'; this.parentElement.textContent='🍪';">
            </div>
            <div class="cookie-name">` + cookie.name + `</div>
            <div class="cookie-meta">` + cookie.role + ` • ` + cookie.position + `</div>
            <div class="cookie-rarity-badge" style="background-color: ` + cookie.color + `"></div>
        `;

        card.addEventListener('click', () => toggleGuildCookieSelection(cookie));
        grid.appendChild(card);
    });
}

function toggleGuildCookieSelection(cookie) {
    const index = guildSelectedCookies.findIndex(c => c.name === cookie.name);

    if (index > -1) {
        guildSelectedCookies.splice(index, 1);
    } else {
        if (guildSelectedCookies.length < 5) {
            guildSelectedCookies.push(cookie);
        } else {
            alert('Maximum 5 cookies allowed for required selection!');
            return;
        }
    }

    updateGuildSelectedCookiesDisplay();
    loadGuildCookies();
}

function updateGuildSelectedCookiesDisplay() {
    const container = document.getElementById('guildSelectedCookies');

    if (guildSelectedCookies.length === 0) {
        container.innerHTML = '<p class="empty-state">None selected</p>';
        return;
    }

    container.innerHTML = guildSelectedCookies.map(cookie => `
        <div class="selected-cookie-chip">
            <span>` + cookie.name + `</span>
            <button class="chip-remove" onclick="removeGuildCookie('` + cookie.name.replace(/'/g, "\\'") + `')">×</button>
        </div>
    `).join('');
}

function removeGuildCookie(cookieName) {
    guildSelectedCookies = guildSelectedCookies.filter(c => c.name !== cookieName);
    updateGuildSelectedCookiesDisplay();
    loadGuildCookies();
}

async function generateGuildTeams() {
    const boss = document.getElementById('guildBoss').value;
    const numTeams = parseInt(document.getElementById('guildTeamsCount').value);
    const prioritizeSTier = document.getElementById('prioritizeSTier').checked;

    document.getElementById('loadingIndicator').style.display = 'flex';

    try {
        const response = await fetch('/api/guild-battle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                boss: boss,
                requiredCookies: guildSelectedCookies.map(c => c.name),
                numTeams: numTeams,
                prioritizeSTier: prioritizeSTier
            })
        });

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Guild Battle team generation failed');
        }

        displayGuildResults(data);
    } catch (error) {
        alert(`Error: ` + error.message);
    } finally {
        document.getElementById('loadingIndicator').style.display = 'none';
    }
}

function displayGuildResults(data) {
    const resultsSection = document.getElementById('guildResultsSection');
    const teamsList = document.getElementById('guildTeamsList');
    const bossNameSpan = document.getElementById('selectedBossName');

    resultsSection.style.display = 'block';
    bossNameSpan.textContent = data.boss;
    teamsList.innerHTML = '';

    data.teams.forEach((teamData, index) => {
        const item = createGuildTeamAccordionItem(teamData, index, data.bossInfo);
        teamsList.appendChild(item);
    });

    // Save teams for bookmarking
    currentGuildTeams = data;

    // Auto-expand first team
    if (data.teams.length > 0) {
        const firstHeader = teamsList.querySelector('.team-accordion-header');
        const firstBody = teamsList.querySelector('.team-accordion-body');
        if (firstHeader && firstBody) {
            firstHeader.classList.add('active');
            firstBody.classList.add('expanded');
        }
    }

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function createGuildTeamAccordionItem(teamData, index, bossInfo) {
    const item = document.createElement('div');
    item.className = 'team-accordion-item';

    // Header
    const header = document.createElement('div');
    header.className = 'team-accordion-header';
    header.innerHTML = `
        <div class="team-accordion-title">Team #` + (index + 1) + `</div>
        <div class="team-accordion-score">Score: ` + teamData.score + `/100</div>
        <button class="bookmark-team-btn" onclick="event.stopPropagation(); bookmarkTeam('guild', ` + index + `, this)" title="Bookmark this team">⭐</button>
        <div class="team-accordion-icon">▼</div>
    `;

    // Body
    const body = document.createElement('div');
    body.className = 'team-accordion-body';

    // Cookie cards
    const cookieCards = teamData.cookies.map(cookie => `
        <div class="team-cookie-mini">
            <div class="cookie-icon">
                <img src="` + cookie.image_url + `"
                     alt="` + cookie.name + `"
                     onerror="this.style.display='none'; this.parentElement.textContent='🍪';">
            </div>
            <div class="cookie-name">` + cookie.name + `</div>
            <div class="cookie-rarity-badge" style="background-color: ` + cookie.color + `"></div>
        </div>
    `).join('');

    // Strategy section
    const strategyHTML = `
        <div class="strategy-section">
            <h4>🎯 Strategy</h4>
            <p>` + teamData.strategy + `</p>
        </div>
    `;

    // Boss Info
    const bossInfoHTML = `
        <div class="boss-strategy-section">
            <h4>📚 Boss Tips</h4>
            <p><strong>Description:</strong> ` + bossInfo.description + `</p>
            <details>
                <summary><strong>S-Tier Cookies</strong></summary>
                <ul>` + bossInfo.sTierCookies.map(c => `<li>` + c + `</li>`).join('') + `</ul>
            </details>
        </div>
    `;

    // Role & Position Distribution
    const roleDistHTML = Object.entries(teamData.roleDistribution)
        .map(([role, count]) => `<span class="stat-badge">` + role + `: ` + count + `</span>`)
        .join('');

    const posDistHTML = Object.entries(teamData.positionDistribution)
        .map(([pos, count]) => `<span class="stat-badge">` + pos + `: ` + count + `</span>`)
        .join('');

    // Synergy section
    const synergyHTML = teamData.advancedSynergy ? `
        <div class="team-stats" style="margin-top: 15px;">
            <div class="team-stat-item team-synergy-header">
                <span class="team-stat-label">🌟 Advanced Synergy:</span>
                <span class="team-stat-value synergy-total">` + teamData.advancedSynergy.totalSynergy + `/60</span>
            </div>
            <div class="team-synergy-breakdown">
                <div class="synergy-bar-item">
                    <span class="synergy-label">🔥 Element Synergy:</span>
                    <div class="synergy-bar-container">
                        <div class="synergy-bar" style="width: ` + ((teamData.advancedSynergy.elementSynergy / 15) * 100) + `%; background: linear-gradient(90deg, #ff6b6b, #ff8787);"></div>
                        <span class="synergy-value">` + teamData.advancedSynergy.elementSynergy + `/15</span>
                    </div>
                </div>
                <div class="synergy-bar-item">
                    <span class="synergy-label">👥 Group Synergy:</span>
                    <div class="synergy-bar-container">
                        <div class="synergy-bar" style="width: ` + ((teamData.advancedSynergy.groupSynergy / 20) * 100) + `%; background: linear-gradient(90deg, #4ecdc4, #5fd9d0);"></div>
                        <span class="synergy-value">` + teamData.advancedSynergy.groupSynergy + `/20</span>
                    </div>
                </div>
                <div class="synergy-bar-item">
                    <span class="synergy-label">⭐ Special Combo:</span>
                    <div class="synergy-bar-container">
                        <div class="synergy-bar" style="width: ` + ((teamData.advancedSynergy.specialCombo / 25) * 100) + `%; background: linear-gradient(90deg, #ffd93d, #ffe66d);"></div>
                        <span class="synergy-value">` + teamData.advancedSynergy.specialCombo + `/25</span>
                    </div>
                </div>
            </div>
        </div>
    ` : '';

    body.innerHTML = `
        <div class="team-accordion-content">
            <div class="team-cookies-grid">
                ` + cookieCards + `
            </div>
            ` + strategyHTML + `
            ` + bossInfoHTML + `
            <div class="team-stats">
                <div class="stat-group">
                    <h4>Role Distribution</h4>
                    <div class="stat-badges">` + roleDistHTML + `</div>
                </div>
                <div class="stat-group">
                    <h4>Position Distribution</h4>
                    <div class="stat-badges">` + posDistHTML + `</div>
                </div>
            </div>
            ` + synergyHTML + `
        </div>
    `;

    // Toggle functionality - use the standard toggleAccordion function
    header.onclick = function() { toggleAccordion(this); };

    item.appendChild(header);
    item.appendChild(body);

    return item;
}
// ==================== BOOKMARKS SYSTEM ====================

let bookmarks = [];
let bookmarkIdCounter = 1;

// Initialize bookmarks from localStorage
function initializeBookmarks() {
    const saved = localStorage.getItem('crk_bookmarks');
    if (saved) {
        try {
            const data = JSON.parse(saved);
            bookmarks = data.bookmarks || [];
            bookmarkIdCounter = data.counter || 1;
            updateBookmarkCount();
        } catch (e) {
            console.error('Failed to load bookmarks:', e);
        }
    }
}

function saveBookmarksToStorage() {
    localStorage.setItem('crk_bookmarks', JSON.stringify({
        bookmarks: bookmarks,
        counter: bookmarkIdCounter
    }));
}

function updateBookmarkCount() {
    document.getElementById('bookmarkCount').textContent = bookmarks.length;
}

function toggleBookmarksPanel() {
    const panel = document.getElementById('bookmarksPanel');
    panel.classList.toggle('open');
    renderBookmarks();
}

function closeBookmarksPanel() {
    document.getElementById('bookmarksPanel').classList.remove('open');
}

function renderBookmarks() {
    const list = document.getElementById('bookmarksList');

    if (bookmarks.length === 0) {
        list.innerHTML = '<p class="empty-state">No bookmarked teams yet. Generate teams and click "⭐ Bookmark" to save them here!</p>';
        return;
    }

    list.innerHTML = bookmarks.map(bookmark => createBookmarkItem(bookmark)).join('');
}

function createBookmarkItem(bookmark) {
    const typeIcons = {
        'optimizer': '⚙️',
        'counter': '⚔️',
        'guild': '🏰'
    };

    // Show cookie names
    const cookieNames = bookmark.cookies.join(', ');

    return `
        <div class="bookmark-item" onclick="viewBookmark(${bookmark.id})">
            <div class="bookmark-header">
                <div>
                    <div class="bookmark-title">${typeIcons[bookmark.type]} ${bookmark.title}</div>
                    <div class="bookmark-info">${bookmark.timestamp}</div>
                </div>
                <button class="bookmark-delete" onclick="event.stopPropagation(); deleteBookmark(${bookmark.id})">×</button>
            </div>
            <div class="bookmark-teams-preview">
                <div class="bookmark-cookies">${cookieNames}</div>
                <div class="bookmark-score">Score: ${bookmark.score}/100</div>
            </div>
        </div>
    `;
}

function deleteBookmark(id) {
    if (confirm('Delete this bookmark?')) {
        bookmarks = bookmarks.filter(b => b.id !== id);
        saveBookmarksToStorage();
        updateBookmarkCount();
        renderBookmarks();
    }
}

function viewBookmark(id) {
    const bookmark = bookmarks.find(b => b.id === id);
    if (!bookmark) return;

    const typeLabels = {
        'optimizer': 'Team Optimizer',
        'counter': 'Counter-Team',
        'guild': 'Guild Battle'
    };

    let message = `${typeLabels[bookmark.type]}: ${bookmark.title}\n`;
    message += `Generated: ${bookmark.timestamp}\n`;
    message += `Score: ${bookmark.score}/100\n`;
    message += `\nTeam Cookies:\n`;
    bookmark.cookies.forEach((cookie, idx) => {
        message += `${idx + 1}. ${cookie}\n`;
    });

    if (bookmark.type === 'counter' && bookmark.enemyTeam) {
        message += `\nEnemy Team:\n`;
        bookmark.enemyTeam.forEach((cookie, idx) => {
            message += `${idx + 1}. ${cookie}\n`;
        });
    }

    if (bookmark.type === 'guild' && bookmark.boss) {
        message += `\nBoss: ${bookmark.boss}`;
    }

    alert(message);
}

// ==================== RESET FUNCTIONS ====================

function resetOptimizer() {
    selectedCookies = [];
    updateSelectedCookiesDisplay();

    document.getElementById('cookieSearch').value = '';
    document.getElementById('rarityFilter').value = '';
    document.getElementById('roleFilter').value = '';
    document.getElementById('positionFilter').value = '';
    document.getElementById('maxRarity').value = '';
    document.getElementById('method').value = 'genetic';
    document.getElementById('numCandidates').value = '100';
    document.getElementById('topN').value = '5';
    document.getElementById('excludeAscended').checked = false;

    document.getElementById('resultsSection').style.display = 'none';

    filterCookies();
    showFeedback('resetOptimizerBtn', '✓ Reset!');
}

function resetCounter() {
    enemySelectedCookies = [];
    updateEnemySelectedCookiesDisplay();

    document.getElementById('enemyCookieSearch').value = '';
    document.getElementById('enemyRarityFilter').value = '';
    document.getElementById('enemyRoleFilter').value = '';
    document.getElementById('counterMaxRarity').value = '';
    document.getElementById('counterMethod').value = 'random';
    document.getElementById('numCounterTeams').value = '5';

    document.getElementById('counterResultsSection').style.display = 'none';

    filterEnemyCookies();
    showFeedback('resetCounterBtn', '✓ Reset!');
}

function resetGuildBattle() {
    guildSelectedCookies = [];
    updateGuildSelectedCookiesDisplay();

    document.getElementById('guildCookieSearch').value = '';
    document.getElementById('guildRarityFilter').value = '';
    document.getElementById('guildRoleFilter').value = '';
    document.getElementById('guildBoss').value = 'Red Velvet Dragon';
    document.getElementById('guildTeamsCount').value = '5';
    document.getElementById('prioritizeSTier').checked = true;

    document.getElementById('guildResultsSection').style.display = 'none';

    updateBossInfo();
    loadGuildCookies();
    showFeedback('resetGuildBtn', '✓ Reset!');
}

// ==================== BOOKMARK FUNCTIONS ====================

let currentOptimizerTeams = null;
let currentCounterTeams = null;
let currentGuildTeams = null;

function bookmarkTeam(type, teamIndex, buttonElement) {
    let team, title, extraData = {};

    // Get the team data based on type
    if (type === 'optimizer') {
        if (!currentOptimizerTeams || !currentOptimizerTeams.teams) return;
        team = currentOptimizerTeams.teams[teamIndex];
        title = `Team Optimizer #${teamIndex + 1}`;
        extraData.method = document.getElementById('method').value;
    } else if (type === 'counter') {
        if (!currentCounterTeams || !currentCounterTeams.counterTeams) return;
        team = currentCounterTeams.counterTeams[teamIndex];
        title = `Counter-Team #${teamIndex + 1}`;
        extraData.enemyTeam = team.cookies.slice(0, 5).map(c => c.name);
    } else if (type === 'guild') {
        if (!currentGuildTeams || !currentGuildTeams.teams) return;
        team = currentGuildTeams.teams[teamIndex];
        title = `${currentGuildTeams.boss} Team #${teamIndex + 1}`;
        extraData.boss = currentGuildTeams.boss;
    }

    if (!team) return;

    // Get score based on type
    const score = type === 'counter' ? team.combinedScore : team.score;

    // Create bookmark
    const bookmark = {
        id: bookmarkIdCounter++,
        type: type,
        title: title,
        timestamp: new Date().toLocaleString(),
        score: score,
        cookies: team.cookies.map(c => c.name),
        ...extraData
    };

    bookmarks.push(bookmark);
    saveBookmarksToStorage();
    updateBookmarkCount();

    // Update button to show confirmation
    const originalText = buttonElement.innerHTML;
    buttonElement.innerHTML = '✓';
    buttonElement.style.color = '#4caf50';
    setTimeout(() => {
        buttonElement.innerHTML = originalText;
        buttonElement.style.color = '';
    }, 1500);
}

// ==================== HELPER FUNCTIONS ====================

function showFeedback(btnId, text) {
    const btn = document.getElementById(btnId);
    const originalText = btn.innerHTML;
    btn.innerHTML = text;
    btn.style.background = '#4caf50';
    setTimeout(() => {
        btn.innerHTML = originalText;
        btn.style.background = '';
    }, 1500);
}
