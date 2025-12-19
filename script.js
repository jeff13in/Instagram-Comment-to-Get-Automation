// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offset = 80; // Account for fixed navbar
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.boxShadow = 'none';
    }

    lastScroll = currentScroll;
});

// FAQ accordion functionality
const faqItems = document.querySelectorAll('.faq-item');
faqItems.forEach((item, index) => {
    const question = item.querySelector('.faq-question');
    const answer = item.querySelector('.faq-answer');

    // Initially hide all answers except the first one
    if (index !== 0) {
        answer.style.display = 'none';
        question.style.cursor = 'pointer';
    }

    question.addEventListener('click', () => {
        const isOpen = answer.style.display !== 'none';

        // Close all other answers
        faqItems.forEach(otherItem => {
            otherItem.querySelector('.faq-answer').style.display = 'none';
        });

        // Toggle current answer
        if (!isOpen) {
            answer.style.display = 'block';
        }
    });
});

// Email form validation and submission
const ctaForm = document.querySelector('.cta-form');
const emailInput = document.querySelector('.cta-input');
const submitButton = document.querySelector('.cta-form .btn');

if (ctaForm && emailInput && submitButton) {
    submitButton.addEventListener('click', async (e) => {
        e.preventDefault();
        const email = emailInput.value.trim();

        // Basic email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!email) {
            showNotification('Please enter your email address', 'error');
            emailInput.focus();
            return;
        }

        if (!emailRegex.test(email)) {
            showNotification('Please enter a valid email address', 'error');
            emailInput.focus();
            return;
        }

        // Disable button and show loading state
        const originalText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Subscribing...';
        submitButton.style.opacity = '0.7';

        try {
            // Send email to backend API
            const response = await fetch('/api/subscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email })
            });

            const data = await response.json();

            if (data.success) {
                showNotification(data.message, 'success');
                emailInput.value = '';
            } else {
                showNotification(data.message || 'Something went wrong. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Error submitting email:', error);
            showNotification('Network error. Please check your connection and try again.', 'error');
        } finally {
            // Re-enable button
            submitButton.disabled = false;
            submitButton.textContent = originalText;
            submitButton.style.opacity = '1';
        }
    });

    // Allow form submission with Enter key
    emailInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            submitButton.click();
        }
    });
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 24px;
        background: ${type === 'success' ? '#10B981' : type === 'error' ? '#EF4444' : '#6366F1'};
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
        font-weight: 500;
        max-width: 300px;
    `;

    document.body.appendChild(notification);

    // Auto-remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
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
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for scroll animations
document.querySelectorAll('.feature-card, .use-case, .pricing-card, .faq-item').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(el);
});

// Pricing card hover effect - highlight features
const pricingCards = document.querySelectorAll('.pricing-card');
pricingCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.borderColor = '#6366F1';
    });

    card.addEventListener('mouseleave', () => {
        if (!card.classList.contains('featured')) {
            card.style.borderColor = '#F1F5F9';
        }
    });
});

// Stats counter animation
function animateCounter(element, target, duration = 2000) {
    let current = 0;
    const increment = target / (duration / 16);
    const isPercentage = String(target).includes('%');
    const numericTarget = parseInt(String(target).replace(/\D/g, ''));

    const timer = setInterval(() => {
        current += increment;
        if (current >= numericTarget) {
            current = numericTarget;
            clearInterval(timer);
        }

        if (isPercentage) {
            element.textContent = Math.floor(current) + '%';
        } else if (String(target).includes('K')) {
            element.textContent = (current / 1000).toFixed(1) + 'K+';
        } else if (String(target).includes('s')) {
            element.textContent = '<' + Math.floor(current) + 's';
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Trigger counter animation when stats section is visible
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumbers = entry.target.querySelectorAll('.stat-number');
            statNumbers.forEach((stat, index) => {
                const targets = ['10K+', '95%', '<60s'];
                setTimeout(() => {
                    animateCounter(stat, targets[index]);
                }, index * 100);
            });
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) {
    statsObserver.observe(heroStats);
}

// Mobile menu toggle (for responsive design)
function createMobileMenu() {
    const navWrapper = document.querySelector('.nav-wrapper');
    const navLinks = document.querySelector('.nav-links');

    if (window.innerWidth <= 768 && !document.querySelector('.mobile-menu-toggle')) {
        const menuToggle = document.createElement('button');
        menuToggle.className = 'mobile-menu-toggle';
        menuToggle.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
        `;
        menuToggle.style.cssText = `
            background: none;
            border: none;
            cursor: pointer;
            color: var(--dark);
            display: block;
        `;

        navWrapper.insertBefore(menuToggle, document.querySelector('.nav-cta'));

        menuToggle.addEventListener('click', () => {
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
            if (navLinks.style.display === 'flex') {
                navLinks.style.cssText = `
                    position: absolute;
                    top: 100%;
                    left: 0;
                    right: 0;
                    background: white;
                    flex-direction: column;
                    padding: 24px;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                    gap: 16px;
                `;
            }
        });
    }
}

window.addEventListener('resize', createMobileMenu);
createMobileMenu();

// Add typing effect to hero title (optional enhancement)
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.textContent = '';

    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }

    type();
}

// Google Authentication
let googleUser = null;

// Initialize Google Sign-In
function initializeGoogleSignIn() {
    // Replace 'YOUR_GOOGLE_CLIENT_ID' with your actual Google OAuth Client ID
    const CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com';

    google.accounts.id.initialize({
        client_id: CLIENT_ID,
        callback: handleCredentialResponse,
        auto_select: false,
    });

    // Render the Google Sign-In button
    google.accounts.id.renderButton(
        document.getElementById('googleSignInBtn'),
        {
            theme: 'outline',
            size: 'large',
            text: 'signin_with',
            shape: 'rectangular',
            logo_alignment: 'left',
        }
    );

    // Check if user is already logged in (from localStorage)
    const savedUser = localStorage.getItem('googleUser');
    if (savedUser) {
        try {
            googleUser = JSON.parse(savedUser);
            showUserProfile(googleUser);
        } catch (error) {
            console.error('Error parsing saved user:', error);
            localStorage.removeItem('googleUser');
        }
    }
}

// Handle Google Sign-In response
function handleCredentialResponse(response) {
    // Decode the JWT token to get user information
    const userInfo = parseJwt(response.credential);

    googleUser = {
        id: userInfo.sub,
        name: userInfo.name,
        email: userInfo.email,
        picture: userInfo.picture,
        credential: response.credential,
    };

    // Save to localStorage
    localStorage.setItem('googleUser', JSON.stringify(googleUser));

    // Show user profile
    showUserProfile(googleUser);

    // Show success notification
    showNotification(`Welcome, ${googleUser.name}!`, 'success');
}

// Parse JWT token
function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

// Show user profile
function showUserProfile(user) {
    // Hide sign-in button
    document.getElementById('googleSignInBtn').style.display = 'none';

    // Show user profile
    const userProfile = document.getElementById('userProfile');
    userProfile.style.display = 'block';

    // Update profile information
    document.getElementById('profileAvatar').src = user.picture;
    document.getElementById('profileName').textContent = user.name;
    document.getElementById('dropdownAvatar').src = user.picture;
    document.getElementById('dropdownName').textContent = user.name;
    document.getElementById('dropdownEmail').textContent = user.email;
}

// Hide user profile (on sign out)
function hideUserProfile() {
    // Show sign-in button
    document.getElementById('googleSignInBtn').style.display = 'flex';

    // Hide user profile
    document.getElementById('userProfile').style.display = 'none';

    // Clear profile information
    document.getElementById('profileAvatar').src = '';
    document.getElementById('profileName').textContent = '';
}

// Profile dropdown toggle
const profileButton = document.querySelector('.profile-button');
const profileDropdown = document.getElementById('profileDropdown');

if (profileButton && profileDropdown) {
    profileButton.addEventListener('click', (e) => {
        e.stopPropagation();
        profileButton.classList.toggle('active');
        profileDropdown.classList.toggle('active');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!profileButton.contains(e.target) && !profileDropdown.contains(e.target)) {
            profileButton.classList.remove('active');
            profileDropdown.classList.remove('active');
        }
    });
}

// Sign out functionality
const signOutBtn = document.getElementById('signOutBtn');
if (signOutBtn) {
    signOutBtn.addEventListener('click', () => {
        // Clear user data
        googleUser = null;
        localStorage.removeItem('googleUser');

        // Hide profile UI
        hideUserProfile();

        // Close dropdown
        profileButton.classList.remove('active');
        profileDropdown.classList.remove('active');

        // Show notification
        showNotification('You have been signed out successfully', 'info');

        // Sign out from Google
        google.accounts.id.disableAutoSelect();
    });
}

// Initialize Google Sign-In when the page loads
if (typeof google !== 'undefined') {
    initializeGoogleSignIn();
} else {
    // Wait for Google API to load
    window.addEventListener('load', () => {
        setTimeout(initializeGoogleSignIn, 500);
    });
}

// Console message for developers
console.log('%c3p99 Instagram Bot', 'font-size: 20px; font-weight: bold; color: #6366F1;');
console.log('%cBuilt with Instagram Graph API v21.0', 'font-size: 12px; color: #64748B;');
console.log('%cInterested in the tech? Check out our docs!', 'font-size: 12px; color: #64748B;');
