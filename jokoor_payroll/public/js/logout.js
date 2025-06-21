$(document).on('click', '.navbar-right a[href="/logout"], .sidebar a[href="/logout"]', function(e) {
    e.preventDefault();
    
    // Get current page path
    const currentPath = window.location.pathname + window.location.search;
    
    // Redirect to logout page with the redirect parameter
    window.location.href = `/logout?redirect-to=${encodeURIComponent(currentPath)}`;
}); 