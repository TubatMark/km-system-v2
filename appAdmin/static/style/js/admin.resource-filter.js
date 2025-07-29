/**
 * Simple Resource Filtering System
 * Uses form submission to your existing URL
 */
class ResourceFilterManager {
    constructor() {
        this.filterForm = document.getElementById('resourceFilterForm');
        this.filterCheckboxes = document.querySelectorAll('.filter-checkbox');
        this.resetButton = document.getElementById('resetFilters');
        
        this.initializeFilters();
    }
    
    initializeFilters() {
        // Auto-submit on checkbox change (with debounce)
        this.filterCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', this.debounce(this.handleFilterChange.bind(this), 300));
        });
        
        // Radio button changes
        const radioButtons = document.querySelectorAll('input[type="radio"]');
        radioButtons.forEach(radio => {
            radio.addEventListener('change', this.handleFilterChange.bind(this));
        });
        
        // Reset functionality
        this.resetButton.addEventListener('click', this.resetAllFilters.bind(this));
        
        // Search input with debounce
        const searchInput = document.querySelector('input[name="search"]');
        if (searchInput) {
            searchInput.addEventListener('input', this.debounce(this.handleFilterChange.bind(this), 500));
        }
    }
    
    handleFilterChange() {
        // Simply submit the form - it will go to your existing URL
        this.filterForm.submit();
    }
    
    resetAllFilters() {
        // Uncheck all checkboxes
        this.filterCheckboxes.forEach(checkbox => {
            checkbox.checked = false;
        });
        
        // Reset radio buttons to default (This Year)
        const defaultRadio = document.getElementById('filterYear');
        if (defaultRadio) {
            defaultRadio.checked = true;
        }
        
        // Clear search input
        const searchInput = document.querySelector('input[name="search"]');
        if (searchInput) {
            searchInput.value = '';
        }
        
        // Go to base URL without parameters
        window.location.href = window.location.pathname;
    }
    
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Initialize the filter manager when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if we're on the resources page
    if (document.getElementById('resourceFilterForm')) {
        new ResourceFilterManager();
    }
});