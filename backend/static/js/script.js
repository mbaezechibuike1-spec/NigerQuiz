// ============================================
// NIGER QUIZ - Complete JavaScript
// ============================================

// ============ GLOBAL VARIABLES ============
let currentUser = null;
let isLoggedIn = false;

// ============ AUTHENTICATION FUNCTIONS ============

// Check if user is logged in
async function checkAuth() {
    try {
        const response = await fetch('/api/profile');
        if (response.ok) {
            const data = await response.json();
            currentUser = data;
            isLoggedIn = true;
            updateUIForLoggedIn();
            return true;
        } else {
            isLoggedIn = false;
            updateUIForLoggedOut();
            return false;
        }
    } catch (error) {
        console.error('Auth check error:', error);
        isLoggedIn = false;
        updateUIForLoggedOut();
        return false;
    }
}

// Update UI for logged in user
function updateUIForLoggedIn() {
    // Hide auth sections
    const authSection = document.getElementById('auth-section');
    if (authSection) authSection.style.display = 'none';
    
    // Show dashboard link
    const dashboardLink = document.getElementById('dashboard-link');
    if (dashboardLink) dashboardLink.style.display = 'block';
    
    // Hide forms
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    if (registerForm) registerForm.style.display = 'none';
    if (loginForm) loginForm.style.display = 'none';
}

// Update UI for logged out user
function updateUIForLoggedOut() {
    // Show auth sections
    const authSection = document.getElementById('auth-section');
    if (authSection) authSection.style.display = 'block';
    
    // Hide dashboard link
    const dashboardLink = document.getElementById('dashboard-link');
    if (dashboardLink) dashboardLink.style.display = 'none';
}

// ============ REGISTRATION ============

async function registerUser(userData) {
    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showNotification('✅ Registration successful! Please login.', 'success');
            return { success: true, data: result };
        } else {
            showNotification('❌ ' + (result.error || 'Registration failed'), 'error');
            return { success: false, error: result.error };
        }
    } catch (error) {
        showNotification('❌ Network error. Please try again.', 'error');
        return { success: false, error: error.message };
    }
}

// ============ LOGIN ============

async function loginUser(credentials) {
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credentials)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showNotification('✅ Welcome back, ' + result.user + '!', 'success');
            currentUser = result;
            isLoggedIn = true;
            updateUIForLoggedIn();
            return { success: true, data: result };
        } else {
            showNotification('❌ ' + (result.error || 'Invalid credentials'), 'error');
            return { success: false, error: result.error };
        }
    } catch (error) {
        showNotification('❌ Network error. Please try again.', 'error');
        return { success: false, error: error.message };
    }
}

// ============ LOGOUT ============

function logoutUser() {
    window.location.href = '/logout';
}

// ============ NOTIFICATION SYSTEM ============

function showNotification(message, type = 'info') {
    // Check if notification container exists
    let container = document.getElementById('notification-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
            width: 100%;
        `;
        document.body.appendChild(container);
    }
    
    const notification = document.createElement('div');
    const colors = {
        success: '#00ff88',
        error: '#ff4444',
        info: '#ffd700',
        warning: '#ff8800'
    };
    
    notification.style.cssText = `
        background: rgba(26, 26, 46, 0.95);
        color: #fff;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 10px;
        border-left: 4px solid ${colors[type] || colors.info};
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        animation: slideIn 0.3s ease;
        backdrop-filter: blur(10px);
        font-size: 0.95rem;
    `;
    
    notification.textContent = message;
    container.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
}

// Add notification animations
const styleSheet = document.createElement('style');
styleSheet.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(styleSheet);

// ============ FORM HANDLING ============

// Handle registration form
document.addEventListener('DOMContentLoaded', function() {
    const regForm = document.getElementById('regForm');
    if (regForm) {
        regForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const password = document.getElementById('reg-password').value;
            const confirm = document.getElementById('reg-confirm').value;
            
            if (password !== confirm) {
                showNotification('❌ Passwords do not match!', 'error');
                return;
            }
            
            if (password.length < 6) {
                showNotification('❌ Password must be at least 6 characters!', 'error');
                return;
            }
            
            const userData = {
                username: document.getElementById('reg-username').value.trim(),
                email: document.getElementById('reg-email').value.trim(),
                phone: document.getElementById('reg-phone').value.trim(),
                country: document.getElementById('reg-country').value.trim(),
                password: password
            };
            
            // Validate
            if (!userData.username || !userData.email || !userData.phone || !userData.country) {
                showNotification('❌ Please fill in all fields!', 'error');
                return;
            }
            
            const result = await registerUser(userData);
            if (result.success) {
                document.getElementById('regForm').reset();
                showLogin();
            }
        });
    }
    
    // Handle login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const credentials = {
                username: document.getElementById('login-username').value.trim(),
                password: document.getElementById('login-password').value
            };
            
            if (!credentials.username || !credentials.password) {
                showNotification('❌ Please fill in all fields!', 'error');
                return;
            }
            
            const result = await loginUser(credentials);
            if (result.success) {
                window.location.href = '/dashboard';
            }
        });
    }
});

// ============ FORM TOGGLES ============

function showRegister() {
    const authSection = document.getElementById('auth-section');
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    
    if (authSection) authSection.style.display = 'none';
    if (registerForm) registerForm.style.display = 'block';
    if (loginForm) loginForm.style.display = 'none';
}

function showLogin() {
    const authSection = document.getElementById('auth-section');
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    
    if (authSection) authSection.style.display = 'none';
    if (registerForm) registerForm.style.display = 'none';
    if (loginForm) loginForm.style.display = 'block';
}

// ============ PROFILE FUNCTIONS ============

async function loadUserProfile(username) {
    try {
        const response = await fetch(`/api/user/${username}`);
        if (response.ok) {
            const user = await response.json();
            return user;
        } else {
            showNotification('❌ User not found', 'error');
            return null;
        }
    } catch (error) {
        showNotification('❌ Error loading profile', 'error');
        return null;
    }
}

// ============ LEADERBOARD FUNCTIONS ============

async function loadLeaderboard() {
    try {
        const response = await fetch('/api/leaderboard');
        if (response.ok) {
            const users = await response.json();
            return users;
        } else {
            showNotification('❌ Error loading leaderboard', 'error');
            return [];
        }
    } catch (error) {
        showNotification('❌ Network error', 'error');
        return [];
    }
}

// ============ QUIZ FUNCTIONS ============

async function loadQuestions(count = 10) {
    try {
        const response = await fetch(`/api/questions/${count}`);
        if (response.ok) {
            const questions = await response.json();
            return questions;
        } else {
            showNotification('❌ Error loading questions', 'error');
            return [];
        }
    } catch (error) {
        showNotification('❌ Network error', 'error');
        return [];
    }
}

async function submitQuizResults(score, correct, total) {
    try {
        const response = await fetch('/api/submit_quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                score: score,
                correct_count: correct,
                total_count: total
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            return result;
        } else {
            showNotification('❌ Error submitting quiz', 'error');
            return null;
        }
    } catch (error) {
        showNotification('❌ Network error', 'error');
        return null;
    }
}

// ============ WITHDRAWAL FUNCTIONS ============

async function submitWithdrawal(withdrawalData) {
    try {
        const response = await fetch('/api/withdraw', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(withdrawalData)
        });
        
        if (response.ok) {
            const result = await response.json();
            showNotification('✅ Withdrawal request submitted successfully!', 'success');
            return result;
        } else {
            const error = await response.json();
            showNotification('❌ ' + (error.error || 'Withdrawal failed'), 'error');
            return null;
        }
    } catch (error) {
        showNotification('❌ Network error', 'error');
        return null;
    }
}

// ============ SEASON FUNCTIONS ============

async function loadSeasonInfo() {
    try {
        const response = await fetch('/api/season');
        if (response.ok) {
            const season = await response.json();
            return season;
        } else {
            return null;
        }
    } catch (error) {
        console.error('Season error:', error);
        return null;
    }
}

// ============ UTILITY FUNCTIONS ============

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Get rank badge class
function getRankClass(rank) {
    return 'rank-' + rank.toLowerCase().replace(/ /g, '-');
}

// Truncate text
function truncateText(text, length = 50) {
    if (text.length <= length) return text;
    return text.substring(0, length) + '...';
}

// ============ ANIMATION HELPERS ============

// Animate counter
function animateCounter(element, target, duration = 1000) {
    const start = 0;
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const current = Math.floor(progress * target);
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.textContent = target;
        }
    }
    
    requestAnimationFrame(update);
}

// ============ INITIALIZATION ============

// Check auth on page load
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    checkAuth();
    
    // Add any additional initialization here
    console.log('🚀 Niger Quiz loaded successfully!');
});

// ============ EXPOSE FUNCTIONS GLOBALLY ============

// Make functions available globally
window.showRegister = showRegister;
window.showLogin = showLogin;
window.logoutUser = logoutUser;
window.registerUser = registerUser;
window.loginUser = loginUser;
window.loadLeaderboard = loadLeaderboard;
window.loadQuestions = loadQuestions;
window.submitQuizResults = submitQuizResults;
window.submitWithdrawal = submitWithdrawal;
window.loadSeasonInfo = loadSeasonInfo;
window.loadUserProfile = loadUserProfile;
window.showNotification = showNotification;
window.formatNumber = formatNumber;
window.getRankClass = getRankClass;
window.animateCounter = animateCounter;
