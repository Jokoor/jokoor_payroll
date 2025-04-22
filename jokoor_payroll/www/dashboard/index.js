document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts and other dashboard functionality
    initExpensesChart();
    
    // Add event listeners
    setupEventListeners();
});

function initExpensesChart() {
    const ctx = document.createElement('canvas');
    document.querySelector('.expenses-chart').appendChild(ctx);
    
    // Sample data for the chart
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'];
    
    // Create gradient background for the bars
    const gradientBase = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradientBase.addColorStop(0, 'rgba(123, 93, 210, 0.8)');
    gradientBase.addColorStop(1, 'rgba(123, 93, 210, 0.2)');
    
    // Chart data
    const data = {
        labels: months,
        datasets: [
            {
                label: 'Base Salary',
                data: [28000, 32000, 30000, 29000, 33000, 31000, 34000, 32500, 31500],
                backgroundColor: gradientBase,
                barThickness: 35,
                borderRadius: 8,
                borderSkipped: false,
            }
        ]
    };
    
    // Chart configuration
    const config = {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        display: true,
                        drawBorder: false,
                        color: 'rgba(200, 200, 200, 0.2)'
                    },
                    ticks: {
                        font: {
                            family: "'Inter', sans-serif",
                            size: 12
                        },
                        color: '#8A8A8F'
                    }
                },
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            family: "'Inter', sans-serif",
                            size: 12
                        },
                        color: '#8A8A8F'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: '#181818',
                    titleFont: {
                        family: "'Inter', sans-serif",
                        size: 14
                    },
                    bodyFont: {
                        family: "'Inter', sans-serif",
                        size: 13
                    },
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('en-US', { 
                                    style: 'currency', 
                                    currency: 'USD' 
                                }).format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            }
        }
    };
    
    // Initialize the chart
    new Chart(ctx, config);
}

function setupEventListeners() {
    // Add event listeners for buttons and interactive elements
    const actionButtons = document.querySelectorAll('.action-btn');
    actionButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Handle action button clicks (can be enhanced with actual functionality)
            const action = this.textContent.trim();
            console.log(`${action} button clicked`);
        });
    });
    
    // See more buttons
    const seeMoreButtons = document.querySelectorAll('.see-more-btn');
    seeMoreButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Handle see more clicks
            const section = this.closest('.dashboard-card').querySelector('h5').textContent;
            console.log(`See more clicked for ${section}`);
        });
    });
    
    // Notification icon click
    const notificationIcon = document.querySelector('.notification-icon');
    if (notificationIcon) {
        notificationIcon.addEventListener('click', function() {
            console.log('Notification icon clicked');
            // Show notifications dropdown (to be implemented)
        });
    }
    
    // Profile avatar click
    const profileAvatar = document.querySelector('.profile-avatar');
    if (profileAvatar) {
        profileAvatar.addEventListener('click', function() {
            console.log('Profile avatar clicked');
            // Show profile dropdown (to be implemented)
        });
    }
    
    // Search functionality
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                console.log('Search query:', this.value);
                // Implement search functionality
            }
        });
    }
}

// Function to format currency values
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', { 
        style: 'currency', 
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}

// Dummy data handlers (can be replaced with actual API calls)
function fetchEmployeeData() {
    // This would be an API call in a real application
    return {
        totalEmployees: 103,
        regularStaff: 93,
        contractStaff: 10
    };
}

function fetchPayrollData() {
    // This would be an API call in a real application
    return {
        processed: 40000,
        pending: 40000,
        taxDeduction: 6000
    };
}

function renderExpensesChart() {
    const ctx = document.createElement('canvas');
    document.querySelector('.expenses-chart').appendChild(ctx);
    
    // Sample month labels
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'];
    
    // Create bar chart with hashed background pattern
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: months,
            datasets: [{
                label: 'Monthly Expenses',
                data: [25000, 28000, 32000, 24000, 26000, 28000, 30000, 29000, 31000],
                backgroundColor: '#af7dff',
                borderWidth: 0,
                borderRadius: 6,
                barThickness: 20
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: '#333',
                    bodyFont: {
                        family: "'Inter', sans-serif",
                        size: 13
                    },
                    callbacks: {
                        label: function(context) {
                            return '$' + context.raw.toLocaleString();
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        color: '#aaa',
                        font: {
                            family: "'Inter', sans-serif",
                            size: 12
                        }
                    }
                },
                y: {
                    display: false
                }
            }
        }
    });
} 