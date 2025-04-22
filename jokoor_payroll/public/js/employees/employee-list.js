// Employee list page handling
$(document).ready(function() {
    console.log("Document ready, setting up Add Employee button handler");
    
    // Handle add employee button click to navigate to the add employee page
    $("#addEmployeeBtn").on("click", function() {
        console.log("Add Employee button clicked");
        window.location.href = "/dashboard/employees/add";
    });
    
    // Alternatively, add the handler this way
    $(document).on("click", "#addEmployeeBtn", function() {
        console.log("Add Employee button clicked (alternative handler)");
        window.location.href = "/dashboard/employees/add";
    });
    
    // Other employee list functionality
    // ...
}); 