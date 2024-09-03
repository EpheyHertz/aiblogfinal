document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contact-form');
    const responseMessage = document.getElementById('response-message');

    contactForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const formData = new FormData(contactForm);
        const name = formData.get('name');
        const email = formData.get('email');
        const message = formData.get('message');

        // Simple form validation
        if (name && email && message) {
            // Send data to backend
            fetch('/contact/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'), // If using Django with CSRF protection
                    'Accept': 'application/json',
                },
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Handle successful response
                responseMessage.textContent = `Thank you, ${name}! Your message has been sent.`;
                responseMessage.style.color = 'green';
                contactForm.reset();
            })
            .catch(error => {
                // Handle error response
                responseMessage.textContent = 'There was a problem sending your message. Please try again later.';
                responseMessage.style.color = 'red';
                console.error('There was an error:', error);
            });
        } else {
            responseMessage.textContent = 'Please fill out all fields.';
            responseMessage.style.color = 'red';
        }
    });
});
