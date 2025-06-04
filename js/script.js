document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('#contact-form form');

    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent actual submission

            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const message = document.getElementById('message').value.trim();

            if (name === '' || email === '' || message === '') {
                alert('Please fill in all fields.');
            } else {
                // Basic email validation (regex for simplicity)
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(email)) {
                    alert('Please enter a valid email address.');
                    return;
                }
                alert('Message sent successfully! (This is a demo)');
                contactForm.reset(); // Reset form fields
            }
        });
    }
});
