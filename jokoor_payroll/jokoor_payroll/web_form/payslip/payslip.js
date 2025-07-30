frappe.ready(function() {
    
    frappe.web_form.after_save = function() {
        
        setTimeout(function() {
            // Try multiple methods to get the employee ID

            id = frappe.web_form.doc.name 

            
           
            if (id) {
                console.log('Redirecting to:', '/payroll/payslip/view?id=' + id);
                window.parent.location.href = '/payroll/payslip/view?id=' + id;
            } else {
                console.log('No employee ID found, redirecting to employees list');
                window.parent.location.href = '/payroll/payslip';
            }
        }, 100); // Increased timeout to ensure form is fully saved
    };
    
    // Alternative approach - listen for successful submission
    frappe.web_form.on('after_save', function() {
        console.log('Form saved successfully');
    });
});