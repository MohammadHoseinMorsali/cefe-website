// cafe_core/static/cafe_core/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('#contact-form form');

    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const message = document.getElementById('message').value.trim();
            let isValid = true;

            if (name === '' || email === '' || message === '') {
                alert('Please fill in all fields.');
                isValid = false;
            } else {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(email)) {
                    alert('Please enter a valid email address.');
                    isValid = false;
                }
            }

            if (!isValid) {
                event.preventDefault(); // Prevent submission ONLY if validation fails
            }
            // If isValid is true, form will submit naturally to the server.
            // The server will then handle success messages and form reset via redirect.
            // So, remove the client-side success alert and reset for non-AJAX form.
        });
    }
});
