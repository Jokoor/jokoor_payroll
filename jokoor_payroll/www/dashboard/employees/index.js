document.addEventListener('DOMContentLoaded', function() {
    // Employee data - in a real application, this would come from a database
    const employeeData = [
        {
            id: 1,
            name: "Guy Hawkins",
            position: "HR Manager",
            department: "HR",
            joiningDate: "Feb 1, 2025",
            salary: "$4,200",
            status: "Active",
            lastLogin: "Mar 10, 2025",
            image: "https://randomuser.me/api/portraits/men/91.jpg"
        },
        {
            id: 2,
            name: "Floyd Miles",
            position: "Recruitment Specialist",
            department: "HR",
            joiningDate: "Feb 1, 2025",
            salary: "$3,800",
            status: "Active",
            lastLogin: "Mar 11, 2025",
            image: "https://randomuser.me/api/portraits/men/32.jpg"
        },
        {
            id: 3,
            name: "John Doe",
            position: "Product Designer",
            department: "IT",
            joiningDate: "Jan 10, 2023",
            salary: "$3,500",
            status: "Active",
            lastLogin: "Mar 12, 2025",
            image: "https://randomuser.me/api/portraits/men/42.jpg"
        },
        {
            id: 4,
            name: "Wade Warren",
            position: "Network Administrator",
            department: "IT",
            joiningDate: "Feb 1, 2025",
            salary: "$3,900",
            status: "Active",
            lastLogin: "Mar 8, 2025",
            image: "https://randomuser.me/api/portraits/men/22.jpg"
        },
        {
            id: 5,
            name: "Jane Cooper",
            position: "Chief Financial Officer",
            department: "Finance",
            joiningDate: "Feb 1, 2025",
            salary: "$5,200",
            status: "Active",
            lastLogin: "Mar 14, 2025",
            image: "https://randomuser.me/api/portraits/women/65.jpg"
        },
        {
            id: 6,
            name: "Jenny Wilson",
            position: "Accountant",
            department: "Finance",
            joiningDate: "Feb 1, 2025",
            salary: "$3,700",
            status: "Active",
            lastLogin: "Mar 13, 2025",
            image: "https://randomuser.me/api/portraits/women/55.jpg"
        },
        {
            id: 7,
            name: "Arlene McCoy",
            position: "Payroll Specialist",
            department: "Finance",
            joiningDate: "Feb 1, 2025",
            salary: "$3,600",
            status: "Active",
            lastLogin: "Mar 9, 2025",
            image: "https://randomuser.me/api/portraits/women/5.jpg"
        },
        {
            id: 8,
            name: "Jerome Bell",
            position: "Sales Manager",
            department: "Sales",
            joiningDate: "Feb 1, 2025",
            salary: "$4,100",
            status: "Active",
            lastLogin: "Mar 7, 2025",
            image: "https://randomuser.me/api/portraits/men/52.jpg"
        },
        {
            id: 9,
            name: "Albert Flores",
            position: "Marketing Manager",
            department: "Marketing",
            joiningDate: "Feb 1, 2025",
            salary: "$4,000",
            status: "Active",
            lastLogin: "Mar 5, 2025",
            image: "https://randomuser.me/api/portraits/men/62.jpg"
        }
    ];

    // Function to update profile card with employee data
    function updateEmployeeProfile(employee) {
        
        // Update profile image
        document.querySelector('.profile-avatar-large img').src = employee.image;
        
        // Update profile header
        document.querySelector('.profile-header h4').textContent = employee.name;
        document.querySelector('.profile-header p').textContent = employee.position;
        
        // Update profile details
        const profileValues = document.querySelectorAll('.profile-value');
        profileValues[0].textContent = employee.position;
        profileValues[1].textContent = employee.department;
        profileValues[2].textContent = employee.joiningDate;
        profileValues[3].textContent = employee.salary;
        
        // Handle status pill separately
        const statusPill = document.querySelector('.profile-value .status-pill');
        statusPill.textContent = employee.status;
        
        // Update last login
        profileValues[5].textContent = employee.lastLogin;
        
        // Add animation effect for better user experience
        const profileCard = document.querySelector('.employee-profile-card');
        profileCard.classList.add('fade-effect');
        setTimeout(() => {
            profileCard.classList.remove('fade-effect');
        }, 500);
    }

    // Handle employee row clicks to update profile view
    const employeeRows = document.querySelectorAll('tbody tr');
    employeeRows.forEach((row, index) => {
        row.addEventListener('click', function() {
            // Highlight the selected row with enhanced styling
            employeeRows.forEach(r => r.classList.remove('row-selected', 'bg-light'));
            this.classList.add('row-selected');
            
            // Get the corresponding employee data and update profile
            if (index < employeeData.length) {
                updateEmployeeProfile(employeeData[index]);
            }
        });
    });
    
    // Set the initial profile (default to first employee)
    if (employeeData.length > 0) {
        updateEmployeeProfile(employeeData[0]); // First employee is displayed by default
        employeeRows[0].classList.add('row-selected'); // Highlight first employee row
    }
    
    // Add search functionality
    const searchInput = document.querySelector('.search-input');
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        
        employeeRows.forEach((row, index) => {
            const employeeName = employeeData[index].name.toLowerCase();
            const position = employeeData[index].position.toLowerCase();
            const department = employeeData[index].department.toLowerCase();
            
            if (employeeName.includes(searchTerm) || 
                position.includes(searchTerm) || 
                department.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
    
    // Connect the add button to the modal
    const addButton = document.querySelector('.add-button');
    if (addButton) {
        addButton.setAttribute('data-bs-toggle', 'modal');
        addButton.setAttribute('data-bs-target', '#addEmployeeModal');
    }
});