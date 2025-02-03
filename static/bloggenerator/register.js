document.addEventListener('DOMContentLoaded', () => {
  const formData = document.getElementById('myform');
  const username = document.getElementById('username');
  const email = document.getElementById('email');
  const password = document.getElementById('password');
  const confirmPassword = document.getElementById('confirm_password');
  const errorMessage = document.getElementById('error-message');

  // Function to retrieve CSRF token from cookies
  function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      let [name, value] = cookie.trim().split('=');
      if (name === 'csrftoken') {
        return value;
      }
    }
    return null;
  }

  const csrfToken = getCSRFToken();

  formData.addEventListener('submit', async (e) => {
    e.preventDefault();

    let errors = [];
    let data = {};
    let endpoint = '';

    if (username) {
      // Signup form
      errors = getSignupFormErrors(username.value, email.value, password.value, confirmPassword.value);
      data = {
        username: username.value,
        email: email.value,
        password: password.value
      };
      endpoint = '/register/';
    } else {
      // Login form
      errors = getLoginFormErrors(email.value, password.value);
      data = {
        email: email.value,
        password: password.value
      };
      endpoint = '/login/';
    }

    if (errors.length > 0) {
      // Display errors
      console.log(errors);
      errorMessage.innerText = errors.join(". ");
    } else {
      try {
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken // Include CSRF token here
          },
          body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
          alert(result.message || 'Success!');
          formData.reset();
          if (endpoint === '/register/') {
            // Redirect to login page after successful registration
            window.location.href = '/login/';
          }
        } else {
          alert(result.error || 'An error occurred. Please try again.');
        }
      } catch (error) {
        console.error('Error:', error);
        errorMessage.innerText = 'An error occurred. Please try again.';
      }
    }
  });

  function getSignupFormErrors(userName, Email, Password, confirmPassword) {
    let errors = [];
    const passwordRegex = /^(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.{8,})/;

    if (userName === '' || userName == null) {
      errors.push('Username required');
      username.parentElement.classList.add('incorrect');
    }
    if (Email === '' || Email == null) {
      errors.push('Email address required');
      email.parentElement.classList.add('incorrect');
    }
    if (Password === '' || Password == null) {
      errors.push('You must set a Password');
      password.parentElement.classList.add('incorrect');
    } else if (!passwordRegex.test(Password)) {
      errors.push('Password must be at least 8 characters long, contain at least one uppercase letter, and at least one special symbol');
      password.parentElement.classList.add('incorrect');
    }
    if (Password !== confirmPassword) {
      errors.push('Password does not match the repeated password');
      password.parentElement.classList.add('incorrect');
      confirmPassword.parentElement.classList.add('incorrect');
    }
    return errors;
  }

  function getLoginFormErrors(Email, Password) {
    let errors = [];
    if (Email === '' || Email == null) {
      errors.push('Email address required');
      email.parentElement.classList.add('incorrect');
    }
    if (Password === '' || Password == null) {
      errors.push('Password cannot be empty!');
      password.parentElement.classList.add('incorrect');
    }
    return errors;
  }

  // Reset error styling on input change
  const allInputs = [username, email, password, confirmPassword].filter(input => input != null);
  allInputs.forEach(input => {
    input.addEventListener('input', () => {
      if (input.parentElement.classList.contains('incorrect')) {
        input.parentElement.classList.remove('incorrect');
        errorMessage.innerText = '';
      }
    });
  });
});