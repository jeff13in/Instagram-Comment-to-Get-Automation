// Google OAuth Authentication Integration with Flask Backend
// This script integrates with the Flask /login, /logout, and /api/user endpoints

let googleUser = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeAuth();
});

// Initialize authentication
async function initializeAuth() {
    // Check if user is logged in
    await checkUserAuth();

    // Setup the Google Sign-In button
    setupGoogleSignInButton();
}

// Check if user is authenticated
async function checkUserAuth() {
    try {
        const response = await fetch('/api/user');
        const data = await response.json();

        if (data.logged_in && data.user) {
            // User is logged in
            googleUser = data.user;
            showUserProfile(data.user);
        } else {
            // User is not logged in
            googleUser = null;
            hideUserProfile();
        }
    } catch (error) {
        console.error('Error checking auth:', error);
        hideUserProfile();
    }
}

// Setup Google Sign-In button
function setupGoogleSignInButton() {
    const signInBtn = document.getElementById('googleSignInBtn');
    if (signInBtn && !googleUser) {
        signInBtn.innerHTML = `
            <a href="/login" style="text-decoration: none;">
                <button class="google-signin-btn" style="
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    padding: 10px 24px;
                    background: white;
                    border: 1px solid #dadce0;
                    border-radius: 4px;
                    font-family: 'Inter', 'Google Sans', arial, sans-serif;
                    font-size: 14px;
                    font-weight: 500;
                    color: #3c4043;
                    cursor: pointer;
                    transition: all 0.2s ease;
                ">
                    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M17.64 9.20443C17.64 8.56625 17.5827 7.95262 17.4764 7.36353H9V10.8449H13.8436C13.635 11.9699 13.0009 12.9231 12.0477 13.5613V15.8194H14.9564C16.6582 14.2526 17.64 11.9453 17.64 9.20443Z" fill="#4285F4"/>
                        <path d="M9 18C11.43 18 13.4673 17.1941 14.9564 15.8195L12.0477 13.5613C11.2418 14.1013 10.2109 14.4204 9 14.4204C6.65591 14.4204 4.67182 12.8372 3.96409 10.71H0.957275V13.0418C2.43818 15.9831 5.48182 18 9 18Z" fill="#34A853"/>
                        <path d="M3.96409 10.71C3.78409 10.17 3.68182 9.59318 3.68182 9C3.68182 8.40682 3.78409 7.82999 3.96409 7.28999V4.95817H0.957275C0.347727 6.17363 0 7.54772 0 9C0 10.4523 0.347727 11.8264 0.957275 13.0418L3.96409 10.71Z" fill="#FBBC05"/>
                        <path d="M9 3.57955C10.3214 3.57955 11.5077 4.03364 12.4405 4.92545L15.0218 2.34409C13.4632 0.891818 11.4259 0 9 0C5.48182 0 2.43818 2.01682 0.957275 4.95818L3.96409 7.29C4.67182 5.16273 6.65591 3.57955 9 3.57955Z" fill="#EA4335"/>
                    </svg>
                    Sign in with Google
                </button>
            </a>
        `;

        // Add hover effects
        const btn = signInBtn.querySelector('.google-signin-btn');
        if (btn) {
            btn.addEventListener('mouseenter', () => {
                btn.style.boxShadow = '0 1px 2px 0 rgba(60,64,67,.3), 0 1px 3px 1px rgba(60,64,67,.15)';
                btn.style.backgroundColor = '#f8f9fa';
            });
            btn.addEventListener('mouseleave', () => {
                btn.style.boxShadow = 'none';
                btn.style.backgroundColor = 'white';
            });
        }
    }
}

// Show user profile
function showUserProfile(user) {
    // Hide sign-in button
    const signInBtn = document.getElementById('googleSignInBtn');
    if (signInBtn) {
        signInBtn.style.display = 'none';
    }

    // Show user profile — build DOM safely to prevent XSS
    const userProfile = document.getElementById('userProfile');
    if (userProfile) {
        userProfile.style.display = 'flex';
        userProfile.innerHTML = '';

        const img = document.createElement('img');
        // Validate picture URL is http/https before assigning (blocks javascript: URLs)
        if (user.picture && /^https?:\/\//.test(user.picture)) {
            img.src = user.picture;
        }
        img.alt = '';
        img.style.cssText = 'width:32px;height:32px;border-radius:50%;object-fit:cover;';

        const span = document.createElement('span');
        span.textContent = user.name;  // textContent, never innerHTML — prevents XSS
        span.style.cssText = 'font-size:14px;font-weight:500;color:#1f2937;';

        const a = document.createElement('a');
        a.href = '/logout';
        a.style.cssText = 'text-decoration:none;margin-left:8px;';

        const logoutBtn = document.createElement('button');
        logoutBtn.textContent = 'Logout';
        logoutBtn.style.cssText = 'padding:6px 16px;background:#f3f4f6;border:1px solid #d1d5db;border-radius:4px;font-size:13px;font-weight:500;color:#374151;cursor:pointer;transition:all 0.2s ease;';

        a.appendChild(logoutBtn);
        userProfile.appendChild(img);
        userProfile.appendChild(span);
        userProfile.appendChild(a);
    }
}

// Hide user profile
function hideUserProfile() {
    // Show sign-in button
    const signInBtn = document.getElementById('googleSignInBtn');
    if (signInBtn) {
        signInBtn.style.display = 'flex';
    }

    // Hide user profile
    const userProfile = document.getElementById('userProfile');
    if (userProfile) {
        userProfile.style.display = 'none';
        userProfile.innerHTML = '';
    }
}

// Export functions for use in other scripts
window.checkUserAuth = checkUserAuth;
window.googleUser = () => googleUser;

// ===== DM Bot Configuration =====

// Test DM Button Handler
document.addEventListener('DOMContentLoaded', function() {
    const testDMBtn = document.getElementById('testDMBtn');
    const dmSettingsBtn = document.getElementById('dmSettingsBtn');

    if (testDMBtn) {
        testDMBtn.addEventListener('click', async function() {
            // Check if user is logged in
            if (!googleUser) {
                alert('Please sign in with Google first to test the DM feature.');
                window.location.href = '/login';
                return;
            }

            // Show loading state
            const originalText = testDMBtn.innerHTML;
            testDMBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="margin-right: 8px; animation: spin 1s linear infinite;">
                    <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="2" stroke-dasharray="12 12"/>
                </svg>
                Testing...
            `;
            testDMBtn.disabled = true;

            try {
                // Call the backend API to test DM functionality
                const response = await fetch('/api/test-dm', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        keywords: ['cyber', 'books', 'project'],
                        test_mode: true
                    })
                });

                const data = await response.json();

                if (data.success) {
                    // Create detailed success message
                    const stats = data.stats || {};
                    const message = `
                        📊 Scan Results:
                        • Posts scanned: ${stats.total_posts_scanned || 0}
                        • Comments found: ${stats.total_comments || 0}
                        • Keyword matches: ${stats.matching_comments || 0}
                        • Replies sent: ${stats.replies_sent || 0}
                        • DMs sent: ${stats.dms_sent || 0}
                    `;

                    // Show success notification with details
                    showDMNotification('✅ DM Test Complete!', message, 'success');

                    // Update stats on the page
                    updateDMStats(stats);

                    // Log processed comments
                    if (data.processed_comments && data.processed_comments.length > 0) {
                        console.log('Processed Comments:', data.processed_comments);
                    }
                } else {
                    showDMNotification('⚠️ DM Test Failed', data.message || 'Please check your Instagram configuration and permissions.', 'error');
                }
            } catch (error) {
                console.error('Error testing DM:', error);
                showDMNotification('❌ Error', 'Failed to test DM feature. Please try again.', 'error');
            } finally {
                // Restore button
                testDMBtn.innerHTML = originalText;
                testDMBtn.disabled = false;
            }
        });
    }

    if (dmSettingsBtn) {
        dmSettingsBtn.addEventListener('click', function() {
            showDMNotification('⚙️ Settings', 'DM configuration settings coming soon! Currently using default keywords: cyber, books, project', 'info');
        });
    }
});

// Show DM notification
function showDMNotification(title, message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `dm-notification dm-notification-${type}`;
    notification.innerHTML = `
        <div class="dm-notification-content">
            <h4>${title}</h4>
            <p>${message}</p>
        </div>
        <button class="dm-notification-close">&times;</button>
    `;

    // Add styles if not already added
    if (!document.getElementById('dm-notification-styles')) {
        const style = document.createElement('style');
        style.id = 'dm-notification-styles';
        style.textContent = `
            .dm-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                max-width: 400px;
                background: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.15);
                z-index: 10000;
                animation: slideInRight 0.3s ease-out;
                border-left: 4px solid #6366F1;
            }
            .dm-notification-success { border-left-color: #10b981; }
            .dm-notification-error { border-left-color: #ef4444; }
            .dm-notification-info { border-left-color: #3b82f6; }
            .dm-notification-content h4 {
                margin: 0 0 8px 0;
                font-size: 16px;
                font-weight: 600;
                color: #1f2937;
            }
            .dm-notification-content p {
                margin: 0;
                font-size: 14px;
                color: #6b7280;
                line-height: 1.5;
                white-space: pre-line;
            }
            .dm-notification-close {
                position: absolute;
                top: 16px;
                right: 16px;
                background: none;
                border: none;
                font-size: 24px;
                color: #9ca3af;
                cursor: pointer;
                line-height: 1;
                padding: 0;
                width: 24px;
                height: 24px;
            }
            .dm-notification-close:hover {
                color: #374151;
            }
            @keyframes slideInRight {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
    }

    // Add to document
    document.body.appendChild(notification);

    // Close button handler
    const closeBtn = notification.querySelector('.dm-notification-close');
    closeBtn.addEventListener('click', () => {
        notification.style.animation = 'slideInRight 0.3s ease-out reverse';
        setTimeout(() => notification.remove(), 300);
    });

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideInRight 0.3s ease-out reverse';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// Update DM stats
function updateDMStats(stats) {
    if (!stats) {
        // Just increment test count if no stats provided
        const dmSentCount = document.getElementById('dmSentCount');
        if (dmSentCount) {
            const current = parseInt(dmSentCount.textContent) || 0;
            dmSentCount.textContent = current + 1;
        }
        return;
    }

    // Update with actual stats from backend
    const dmSentCount = document.getElementById('dmSentCount');
    const dmResponseRate = document.getElementById('dmResponseRate');
    const dmActiveKeywords = document.getElementById('dmActiveKeywords');

    if (dmSentCount && stats.dms_sent !== undefined) {
        const current = parseInt(dmSentCount.textContent) || 0;
        dmSentCount.textContent = current + stats.dms_sent;
    }

    if (dmResponseRate && stats.matching_comments && stats.total_comments) {
        const rate = ((stats.matching_comments / stats.total_comments) * 100).toFixed(1);
        dmResponseRate.textContent = rate + '%';
    }

    if (dmActiveKeywords) {
        dmActiveKeywords.textContent = '3'; // cyber, books, project
    }
}
