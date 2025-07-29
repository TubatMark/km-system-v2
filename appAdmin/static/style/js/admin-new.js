// Sidebar Toggle Functionality
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');
const mainWrapper = document.getElementById('mainWrapper');
const sidebarOverlay = document.getElementById('sidebarOverlay');

sidebarToggle.addEventListener('click', function() {
    if (window.innerWidth <= 768) {
        sidebar.classList.toggle('show');
        sidebarOverlay.classList.toggle('show');
    } else {
        sidebar.classList.toggle('collapsed');
        mainWrapper.classList.toggle('expanded');
    }
});

// Close sidebar when clicking overlay
sidebarOverlay.addEventListener('click', function() {
    sidebar.classList.remove('show');
    sidebarOverlay.classList.remove('show');
});

// Handle window resize
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        sidebar.classList.remove('show');
        sidebarOverlay.classList.remove('show');
    }
});

// Dropdown Menu Functionality
document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
    toggle.addEventListener('click', function(e) {
        e.preventDefault();
        const dropdownId = this.getAttribute('data-dropdown') + '-dropdown';
        const dropdown = document.getElementById(dropdownId);
        const arrow = this.querySelector('.dropdown-arrow');
        
        // Close other dropdowns
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            if (menu.id !== dropdownId) {
                menu.classList.remove('show');
            }
        });
        
        document.querySelectorAll('.dropdown-toggle').forEach(t => {
            if (t !== this) {
                t.classList.remove('active');
            }
        });
        
        // Toggle current dropdown
        dropdown.classList.toggle('show');
        this.classList.toggle('active');
    });
});

// Animated Counter Function
function animateCounter(element, start, end, duration) {
    const startTimestamp = performance.now();
    const step = (timestamp) => {
        const elapsed = timestamp - startTimestamp;
        const progress = Math.min(elapsed / duration, 1);
        const current = Math.floor(progress * (end - start) + start);
        element.textContent = current.toLocaleString();
        
        if (progress < 1) {
            requestAnimationFrame(step);
        }
    };
    requestAnimationFrame(step);
}

// Initialize counters when page loads
window.addEventListener('load', function() {
    const userCountElement = document.getElementById('userCount');
    const commodityCountElement = document.getElementById('commodityCount');
    const cmiCountElement = document.getElementById('cmiCount');
    const resourceCountElement = document.getElementById('resourceCount');

    // Helper to parse the initial value from the element
    function getTargetValue(element) {
        if (!element) return 0;
        const val = parseInt(element.textContent.replace(/,/g, ''), 10);
        return isNaN(val) ? 0 : val;
    }

    if (userCountElement) {
        animateCounter(userCountElement, 0, getTargetValue(userCountElement), 2000);
    }
    if (commodityCountElement) {
        animateCounter(commodityCountElement, 0, getTargetValue(commodityCountElement), 2000);
    }
    if (cmiCountElement) {
        animateCounter(cmiCountElement, 0, getTargetValue(cmiCountElement), 2000);
    }
    if (resourceCountElement) {
        animateCounter(resourceCountElement, 0, getTargetValue(resourceCountElement), 2000);
    }
});

// Search functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            // Implement search logic here
            console.log('Searching for:', searchTerm);
        });
    }
});

// Notification badge click
document.addEventListener('DOMContentLoaded', function() {
    const notificationBadge = document.getElementById('notificationBadge');
    if (notificationBadge) {
        notificationBadge.addEventListener('click', function() {
            // Toggle notification dropdown
            console.log('Notifications clicked');
        });
    }
});

// User profile click
document.addEventListener('DOMContentLoaded', function() {
    const userProfile = document.getElementById('userProfile');
    if (userProfile) {
        userProfile.addEventListener('click', function() {
            // Toggle user menu
            console.log('User profile clicked');
        });
    }
});

// Chart period selector
document.addEventListener('DOMContentLoaded', function() {
    const chartPeriod = document.getElementById('chartPeriod');
    if (chartPeriod) {
        chartPeriod.addEventListener('change', function(e) {
            const period = e.target.value;
            // Update chart data based on selected period
            console.log('Chart period changed to:', period);
        });
    }
});

// Map toggle button
document.addEventListener('DOMContentLoaded', function() {
    const mapToggle = document.getElementById('mapToggle');
    if (mapToggle) {
        mapToggle.addEventListener('click', function() {
            // Toggle map layers
            console.log('Map layers toggled');
        });
    }
});

// Progressive Enhancement - Add smooth scrolling
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Add keyboard navigation support
document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const searchInput = document.querySelector('.search-input');
    
    document.addEventListener('keydown', function(e) {
        // Toggle sidebar with Ctrl+B
        if (e.ctrlKey && e.key === 'b') {
            e.preventDefault();
            if (sidebarToggle) {
                sidebarToggle.click();
            }
        }
        
        // Focus search with Ctrl+K
        if (e.ctrlKey && e.key === 'k') {
            e.preventDefault();
            if (searchInput) {
                searchInput.focus();
            }
        }
    });
});

// Add loading states for async operations
function showLoading(element) {
    element.innerHTML = '<div class="loading"></div>';
}

function hideLoading(element, content) {
    element.innerHTML = content;
}

// Toast notification system
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#D71313' : '#0C356A'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Example usage
// showToast('Welcome to AANR Knowledge Hub!', 'success');

// Initialize tooltips (if needed)
function initTooltips() {
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.style.cssText = `
                position: absolute;
                background: rgba(0,0,0,0.8);
                color: white;
                padding: 0.5rem;
                border-radius: 4px;
                font-size: 0.8rem;
                z-index: 10000;
                pointer-events: none;
            `;
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
            
            this.addEventListener('mouseleave', function() {
                document.body.removeChild(tooltip);
            }, { once: true });
        });
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
    
    // Add some sample data loading simulation
    setTimeout(() => {
        showToast('Dashboard data loaded successfully!', 'success');
    }, 1500);
});