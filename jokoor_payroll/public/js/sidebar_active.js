document.addEventListener('DOMContentLoaded', function() {
    // Set active sidebar item based on current URL
    setSidebarActiveState();
});

function setSidebarActiveState() {
    // Get the current URL path
    const currentPath = window.location.pathname;
    
    // First, remove active class from all nav items
    document.querySelectorAll('.nav-item').forEach(link => {
        link.classList.remove('active');
    });
    
    // Determine which section should be active based on URL
    let activeSection = '';
    
    // Check URL patterns and set appropriate section
    if (currentPath.includes('/employees') || 
        currentPath.includes('/employee') || 
        currentPath.includes('/add-employee')) {
        activeSection = 'employees';
    } else if (currentPath.includes('/attendance')) {
        activeSection = 'attendance';
    } else if (currentPath.includes('/payroll')) {
        activeSection = 'payroll';
    } else if (currentPath.includes('/payslips')) {
        activeSection = 'payslips';
    } else if (currentPath.includes('/reports')) {
        activeSection = 'reports';
    } else if (currentPath.includes('/profile')) {
        activeSection = 'profile';
    } else if (currentPath.includes('/settings')) {
        activeSection = 'settings';
    } else if (currentPath.includes('/subscription')) {
        activeSection = 'subscription';
    } else if (currentPath.includes('/dashboard') || currentPath === '/') {
        activeSection = 'dashboard';
    }
    
    // Set the active class on the correct link
    if (activeSection) {
        // Find links by their text content and href attributes
        document.querySelectorAll('.nav-item').forEach(link => {
            const linkHref = link.getAttribute('href') || '';
            const linkText = link.textContent.trim().toLowerCase();
            
            if (linkHref.includes(activeSection) || linkText.includes(activeSection)) {
                link.classList.add('active');
            }
        });
    }
} 