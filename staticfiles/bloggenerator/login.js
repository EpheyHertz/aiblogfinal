document.addEventListener('DOMContentLoaded', () => {
    const formData = document.getElementById('form');
    const username = document.getElementById('username');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    const errorMessage = document.getElementById('error-message');

    formData.addEventListener('submit', (e) => {
        let errors = [];
        let data = {};

        if (username) {
            errors = getSignupFormErrors(username.value, email.value, password.value, confirmPassword.value);
            data = {
                username: username.value,
                email: email.value,
                password: password.value
            };
        } else {
            // We are in login form
            errors = getLoginFormErrors(email.value, password.value);
            data = {
                email: email.value,
                password: password.value
            };
        }

        if (errors.length > 0) {
            // If errors in the array
            console.log(errors);
            e.preventDefault();
            errorMessage.innerText = errors.join(". ");
        } else {
            alert("Data sent successfully")
        //     // No errors, send the data to the backend
        //     e.preventDefault(); // Prevent the default form submission
        //     let endpoint;
        //     endpoint = '/login'
        //     // const endpoint = username ? '/register' : '/login' : '/dashboard'; // Define the endpoint based on form type

        //     fetch(endpoint, {
        //         method: 'POST',
        //         headers: {
        //             'Content-Type': 'application/json'
        //         },
        //         body: JSON.stringify(data)
        //     })
        //     .then(response => response.json())
        //     .then(result => {
        //         console.log('Success:', result);
        //         // Handle success, e.g., redirect to another page
        //         // if (response.ok) {
        //         //     alert(result.message);  
        //         //     formData.reset();
        //         // } else {
        //         //     alert(result.error)
        //         // }
        //         if(result.message === 'Login successful!' ){
        //             alert(result.message)
        //             formData.reset();
        //             if (endpoint === '/login') {
        //                 // Redirect to login page after successful registration
        //                 window.location.href = '/dashboard';
        //                 document.getElementById('clickhere').style.display = 'block';
        //                 // Optionally hide the login form
        //                 document.getElementById('login-container').style.display = 'none'
                       
                        
        //             }

                    

        //         }else{
        //             alert(result.error)
        //         }
                
        //     })
        //     .catch(error =>{
        //         console.log(error)
        //        errorMessage.innerText = '';
        //        })
               
        }
    });

    function getSignupFormErrors(userName, Email, Password, confirmpassword) {
        let errors = [];
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
        }
        if (Password !== confirmpassword) {
            errors.push('Password Does not match the Repeated Password');
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
            errors.push('Password cannot be empty!!');
            password.parentElement.classList.add('incorrect');
        }
        return errors;
    }

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