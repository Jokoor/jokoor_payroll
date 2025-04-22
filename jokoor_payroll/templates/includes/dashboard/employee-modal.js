// Initialize the employee modal functionality
function initEmployeeModal() {
    // Multi-step form navigation
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    const steps = document.querySelectorAll('.form-step');
    const stepDots = document.querySelectorAll('.step-dot');
    let currentStep = 1;
    
    // Function to show a specific step
    function showStep(stepNumber) {
        // Hide all steps
        steps.forEach(step => step.classList.add('d-none'));
        
        // Show the current step
        document.getElementById('step' + stepNumber).classList.remove('d-none');
        
        // Update step dots
        stepDots.forEach(dot => {
            const dotStep = parseInt(dot.dataset.step);
            dot.classList.remove('active', 'completed');
            
            if (dotStep < stepNumber) {
                dot.classList.add('completed');
            } else if (dotStep === stepNumber) {
                dot.classList.add('active');
            }
        });
        
        // Update buttons
        prevBtn.disabled = (stepNumber === 1);
        
        if (stepNumber === 4) {
            nextBtn.classList.add('d-none');
            submitBtn.classList.remove('d-none');
            // Update confirmation screen with form values
            updateConfirmationScreen();
        } else {
            nextBtn.classList.remove('d-none');
            submitBtn.classList.add('d-none');
        }
    }
    
    // Function to validate the current step
    function validateCurrentStep() {
        const currentStepEl = document.getElementById('step' + currentStep);
        const inputs = currentStepEl.querySelectorAll('input[required], select[required], textarea[required]');
        
        let isValid = true;
        inputs.forEach(input => {
            if (!input.value) {
                isValid = false;
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
        });
        
        return isValid;
    }
    
    // Function to update the confirmation screen
    function updateConfirmationScreen() {
        document.getElementById('confirm-name').textContent = `${document.getElementById('firstName').value} ${document.getElementById('lastName').value}`;
        document.getElementById('confirm-position').textContent = document.getElementById('position').value;
        document.getElementById('confirm-department').textContent = document.getElementById('department').value;
        document.getElementById('confirm-joiningDate').textContent = document.getElementById('joiningDate').value;
        document.getElementById('confirm-status').textContent = document.getElementById('status').value;
        document.getElementById('confirm-salary').textContent = `$${document.getElementById('salary').value}`;
        document.getElementById('confirm-email').textContent = document.getElementById('email').value;
        document.getElementById('confirm-phone').textContent = document.getElementById('phone').value;
    }
    
    
    // Next button click handler
    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            if (validateCurrentStep()) {
                currentStep++;
                showStep(currentStep);
            }
        });
    }
    
    // Previous button click handler
    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            if (currentStep > 1) {
                currentStep--;
                showStep(currentStep);
            }
        });
    }
    
    // Submit button click handler
    if (submitBtn) {
        submitBtn.addEventListener('click', function() {
            // Here you would normally submit the form data to the server
            const modal = bootstrap.Modal.getInstance(document.getElementById('addEmployeeModal'));
            modal.hide();
            
            // Create success notification
            createNotification('success', 'Success', 'Employee created successfully!');
            
            // In a real app, you would add the new employee to the table
            // and refresh the employee list
        });
    }
    
    // Profile image upload preview
    const profileUpload = document.getElementById('profile-upload');
    const profileContainer = document.querySelector('.profile-upload-container');
    const profilePlaceholder = document.querySelector('.profile-upload-placeholder');
    
    if (profileUpload && profileContainer && profilePlaceholder) {
        profileUpload.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                const file = e.target.files[0];
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    profilePlaceholder.innerHTML = `<img src="${e.target.result}" alt="Profile Preview" style="width: 100%; height: 100%; object-fit: cover;">`;
                }
                
                reader.readAsDataURL(file);
            }
        });
        
        // Make the profile container clickable
        profileContainer.addEventListener('click', function() {
            profileUpload.click();
        });
    }
}

// Helper function to create notifications
function createNotification(type, title, message) {
    const notificationHtml = `
        <div class="toast-container position-fixed top-0 end-0 p-3">
            <div class="toast align-items-center text-white bg-${type === 'success' ? 'success' : 'danger'} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        <strong>${title}:</strong> ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        </div>
    `;
    
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = notificationHtml;
    document.body.appendChild(tempDiv.firstElementChild);
    
    const toastElement = document.querySelector('.toast');
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove notification after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.parentNode.remove();
    });
}

// Create a function to initialize the modal when the trigger is clicked
function setupEmployeeModalTriggers() {
    document.querySelectorAll('[data-bs-target="#addEmployeeModal"]').forEach(trigger => {
        trigger.addEventListener('click', function() {
            // Initialize modal on first click
            setTimeout(() => {
                initEmployeeModal();
            }, 300); // Small delay to ensure modal is in DOM
        });
    });
}

// Setup modal triggers when the document is ready
document.addEventListener('DOMContentLoaded', function() {
    setupEmployeeModalTriggers();
}); 
