// Employee creation form handling
$(document).ready(function() {
    // Handle plus button click to open the employee creation modal
    $("#addEmployeeBtn").on("click", function() {
        $("#createEmployeeModal").modal("show");
    });
    
    // Handle form submission
    $("#employeeForm").on("submit", function(e) {
        e.preventDefault();
        
        // Show loading state
        $("#submitEmployeeBtn").prop("disabled", true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Creating...');
        
        // Collect form data
        const formData = {
            full_name: $("#employeeName").val(),
            email: $("#employeeEmail").val(),
            phone: $("#employeePhone").val(),
            position: $("#employeePosition").val(),
            department: $("#employeeDepartment").val(),
            hire_date: $("#employeeHireDate").val(),
            salary: $("#employeeSalary").val(),
            address: $("#employeeAddress").val(),
            employment_type: $("input[name='employmentType']:checked").val()
        };
        
        // Send AJAX request to create employee
        frappe.call({
            method: "jokoor_payroll.www.dashboard.employees.index.create_employee",
            args: formData,
            callback: function(response) {
                // Reset button state
                $("#submitEmployeeBtn").prop("disabled", false).html('Create Employee');
                
                if (response.message.success) {
                    // Show success message
                    frappe.show_alert({
                        message: response.message.message,
                        indicator: 'green'
                    }, 5);
                    
                    // Close modal
                    $("#createEmployeeModal").modal("hide");
                    
                    // Reset form
                    $("#employeeForm")[0].reset();
                    
                    // Reload page to show new employee
                    setTimeout(function() {
                        window.location.reload();
                    }, 1000);
                } else {
                    // Show error message
                    frappe.show_alert({
                        message: response.message.message,
                        indicator: 'red'
                    }, 5);
                }
            },
            error: function(xhr, status, error) {
                // Reset button state
                $("#submitEmployeeBtn").prop("disabled", false).html('Create Employee');
                
                // Show error message
                frappe.show_alert({
                    message: "An error occurred while creating employee",
                    indicator: 'red'
                }, 5);
            }
        });
    });
}); 