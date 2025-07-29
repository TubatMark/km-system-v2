// AdminUI: Sidebar and overlay logic matching admin-index.css
// Handles both desktop (collapsed) and mobile (show/overlay) sidebar
// Assumes .sidebar, .sidebar.collapsed, .sidebar.show, .sidebar-overlay, .sidebar-toggle

(function(window, document) {
    'use strict';

    // Selectors
    const sidebar = document.querySelector('.sidebar');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    let sidebarOverlay = document.querySelector('.sidebar-overlay');

    // Create overlay if not present
    if (!sidebarOverlay) {
        sidebarOverlay = document.createElement('div');
        sidebarOverlay.className = 'sidebar-overlay';
        document.body.appendChild(sidebarOverlay);
    }

    // Helper: check if mobile
    function isMobile() {
        return window.innerWidth <= 768;
    }

    // Toggle sidebar
    function toggleSidebar() {
        if (isMobile()) {
            sidebar.classList.toggle('show');
            sidebarOverlay.classList.toggle('show');
        } else {
            sidebar.classList.toggle('collapsed');
        }
    }

    // Hide sidebar (mobile)
    function hideSidebarMobile() {
        sidebar.classList.remove('show');
        sidebarOverlay.classList.remove('show');
    }

    // Event: toggle button
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            toggleSidebar();
        });
    }

    // Event: overlay click (mobile)
    sidebarOverlay.addEventListener('click', function() {
        hideSidebarMobile();
    });

    // Responsive: hide overlay/sidebar on resize
    window.addEventListener('resize', function() {
        if (!isMobile()) {
            hideSidebarMobile();
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
        }
    });

    // Optional: close sidebar on navigation (mobile)
    document.addEventListener('click', function(e) {
        if (isMobile() && sidebar.classList.contains('show')) {
            // Only close if clicking a nav-link inside sidebar
            if (e.target.closest('.sidebar .nav-link')) {
                hideSidebarMobile();
            }
        }
    });

    // Expose for debugging
    window.AdminUI = {
        toggleSidebar,
        hideSidebarMobile,
        isMobile
    };

})(window, document); 