// Employee page functionality
frappe.ready(function() {
    console.log("Employee page JS loaded!");
    
    // Search functionality
    const searchInput = document.getElementById('tableSearchInput');
    const departmentFilter = document.getElementById('departmentFilter');
    const statusFilter = document.getElementById('statusFilter');
    const sortBySelect = document.getElementById('sortBy');
    const resetFiltersBtn = document.getElementById('resetFilters');
    const tableRows = document.querySelectorAll('#employeesTable tbody tr');
    
    // Filter functionality
    function filterEmployees() {
        const searchTerm = searchInput?.value?.toLowerCase() || '';
        const department = departmentFilter?.value || '';
        const status = statusFilter?.value || '';
        
        let visibleCount = 0;
        
        tableRows.forEach(row => {
            const nameCell = row.querySelector('.employee-name');
            const emailCell = row.querySelector('.employee-email');
            const departmentCell = row.cells[2]?.textContent;
            const statusCell = row.cells[4]?.querySelector('.status-pill')?.textContent?.trim();
            
            const nameMatch = nameCell ? nameCell.textContent.toLowerCase().includes(searchTerm) : false;
            const emailMatch = emailCell ? emailCell.textContent.toLowerCase().includes(searchTerm) : false;
            const departmentMatch = department === '' || (departmentCell && departmentCell.includes(department));
            const statusMatch = status === '' || (statusCell && statusCell.includes(status));
            
            if ((nameMatch || emailMatch) && departmentMatch && statusMatch) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });
        
        // Update showing X of Y employees text
        document.getElementById('startRange').textContent = visibleCount > 0 ? '1' : '0';
        document.getElementById('endRange').textContent = visibleCount;
    }
    
    // Sort functionality
    function sortEmployees() {
        const sortBy = sortBySelect?.value || 'name';
        const tbody = document.querySelector('#employeesTable tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        rows.sort((a, b) => {
            let aValue, bValue;
            
            switch(sortBy) {
                case 'name':
                    aValue = a.querySelector('.employee-name')?.textContent.toLowerCase() || '';
                    bValue = b.querySelector('.employee-name')?.textContent.toLowerCase() || '';
                    return aValue.localeCompare(bValue);
                case 'name_desc':
                    aValue = a.querySelector('.employee-name')?.textContent.toLowerCase() || '';
                    bValue = b.querySelector('.employee-name')?.textContent.toLowerCase() || '';
                    return bValue.localeCompare(aValue);
                case 'date_asc':
                    aValue = new Date(a.cells[3]?.textContent || '');
                    bValue = new Date(b.cells[3]?.textContent || '');
                    return aValue - bValue;
                case 'date_desc':
                    aValue = new Date(a.cells[3]?.textContent || '');
                    bValue = new Date(b.cells[3]?.textContent || '');
                    return bValue - aValue;
                default:
                    return 0;
            }
        });
        
        // Remove all rows
        rows.forEach(row => row.remove());
        
        // Add sorted rows
        rows.forEach(row => tbody.appendChild(row));
    }
    
    // Add event listeners
    if (searchInput) {
        searchInput.addEventListener('input', filterEmployees);
    }
    
    if (departmentFilter) {
        departmentFilter.addEventListener('change', filterEmployees);
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', filterEmployees);
    }
    
    if (sortBySelect) {
        sortBySelect.addEventListener('change', function() {
            sortEmployees();
            filterEmployees(); // Re-apply filters after sorting
        });
    }
    
    if (resetFiltersBtn) {
        resetFiltersBtn.addEventListener('click', function() {
            if (searchInput) searchInput.value = '';
            if (departmentFilter) departmentFilter.selectedIndex = 0;
            if (statusFilter) statusFilter.selectedIndex = 0;
            if (sortBySelect) sortBySelect.selectedIndex = 0;
            
            filterEmployees();
            sortEmployees();
        });
    }
    
    // Enhance table hover effects
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            const actionButtons = this.querySelectorAll('.btn');
            actionButtons.forEach(btn => {
                btn.classList.remove('btn-light');
                btn.classList.add('btn-outline-primary');
            });
        });
        
        row.addEventListener('mouseleave', function() {
            const actionButtons = this.querySelectorAll('.btn');
            actionButtons.forEach(btn => {
                btn.classList.remove('btn-outline-primary');
                btn.classList.add('btn-light');
            });
        });
    });
    
    // Initialize filters on page load
    filterEmployees();
}); 