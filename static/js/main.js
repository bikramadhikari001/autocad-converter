// Main JavaScript file for common functionality

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 5000);
    });

    // Mobile detection and messaging
    if (window.innerWidth < 768) {
        const mobileMessage = document.createElement('div');
        mobileMessage.className = 'alert alert-info';
        mobileMessage.innerHTML = '📱 For the best experience, please use a desktop computer.';
        mobileMessage.style.position = 'fixed';
        mobileMessage.style.top = '0';
        mobileMessage.style.left = '0';
        mobileMessage.style.right = '0';
        mobileMessage.style.zIndex = '1000';
        mobileMessage.style.textAlign = 'center';
        mobileMessage.style.background = '#dbeafe';
        mobileMessage.style.color = '#1e40af';
        mobileMessage.style.padding = '0.5rem';
        mobileMessage.style.fontSize = '0.9rem';
        
        document.body.insertBefore(mobileMessage, document.body.firstChild);
        
        // Auto-hide mobile message after 8 seconds
        setTimeout(function() {
            mobileMessage.style.opacity = '0';
            setTimeout(function() {
                mobileMessage.remove();
            }, 300);
        }, 8000);
    }

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form validation helpers
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    field.style.borderColor = '#dc2626';
                    isValid = false;
                } else {
                    field.style.borderColor = '#d1d5db';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
});
