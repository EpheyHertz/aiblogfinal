// document.addEventListener('DOMContentLoaded', () => {
//   const formData = document.getElementById('myform');
//   const username = document.getElementById('username');
//   const email = document.getElementById('email');
//   const password = document.getElementById('password');
//   const confirmPassword = document.getElementById('confirm_password');
//   const errorMessage = document.getElementById('error-message');

//   formData.addEventListener('submit', async (e) => {
//       e.preventDefault();
      
//       const errors = getSignupFormErrors(username.value, email.value, password.value, confirmPassword.value);
  
//       if (errors.length > 0) {
//         errorMessage.innerText = errors.join('. ');
//         return;
//       }
//     //   endpoint = '/register';
  
//     //   // Perform registration
//     //   const response = await fetch('/register', {
//     //     method: 'POST',
//     //     headers: {
//     //       'Content-Type': 'application/json'
//     //     },
//     //     body: JSON.stringify({
//     //       username: username.value,
//     //       email: email.value,
//     //       password: password.value
//     //     })
//     //   });
  
//     //   const result = await response.json();
  
//     //   if (response.status === 200) {
//     //     alert(result.message);
//     //     formData.reset();
//     //     if (endpoint === '/register') {
//     //       // Redirect to login page after successful registration
//     //       window.location.href = '/login';
//     //     }
//     //   } else {
//     //     alert(result.error);
//     //   }
//     // });
  
//     function getSignupFormErrors(userName, Email, Password, confirmpassword) {
//       let errors = [];
//       const passwordRegex = /^(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.{8,})/;
      
//       if (userName === '' || userName == null) {
//         errors.push('Username required');
//         username.parentElement.classList.add('incorrect');
//       }
//       if (Email === '' || Email == null) {
//         errors.push('Email address required');
//         email.parentElement.classList.add('incorrect');
//       }
//       if (Password === '' || Password == null) {
//         errors.push('You must set a Password');
//         password.parentElement.classList.add('incorrect');
//       } else if (!passwordRegex.test(Password)) {
//         errors.push('Password must be at least 8 characters long, contain at least one uppercase letter, and at least one special symbol');
//         password.parentElement.classList.add('incorrect');
//       }
//       if (Password !== confirmpassword) {
//         errors.push('Password does not match the repeated password');
//         password.parentElement.classList.add('incorrect');
//         confirmPassword.parentElement.classList.add('incorrect');
//       }
//       return errors;
//     }
//   });

//     formData.addEventListener('submit', (e) => {
//         let errors = [];
//         let data = {};

//         if (username) {
//             errors = getSignupFormErrors(username.value, email.value, password.value, confirmPassword.value);
//             data = {
//                 username: username.value,
//                 email: email.value,
//                 password: password.value
//             };
//         } else {
//             // We are in login form
//             errors = getLoginFormErrors(email.value, password.value);
//             data = {
//                 email: email.value,
//                 password: password.value
//             };
//         }

//         if (errors.length > 0) {
//             // If errors in the array
//             console.log(errors);
//             e.preventDefault();
//             errorMessage.innerText = errors.join(". ");
//         } else {
//             // No errors, send the data to the backend
//             e.preventDefault(); // Prevent the default form submission

//             const endpoint = username ? '/register' : '/login'; // Define the endpoint based on form type

//             fetch(endpoint, {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json'
//                 },
//                 body: JSON.stringify(data)
//             })
//             .then(response => response.json())
//             .then(result => {
//                 console.log('Success:', result);
//                 // Handle success, e.g., redirect to another page
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//                 errorMessage.innerText = 'An error occurred. Please try again.';
//             });
//             // const result = await response.json();

//     // if (response.status === 200) {
//     //   alert(result.message);
//     //   formData.reset();
//     // } else {
//     //   alert(result.error);
//     // }
//         }
//  });

    // function getSignupFormErrors(userName, Email, Password, confirmpassword) {
    //     let errors = [];
    //     if (userName === '' || userName == null) {
    //         errors.push('Username required');
    //         username.parentElement.classList.add('incorrect');
    //     }
    //     if (Email === '' || Email == null) {
    //         errors.push('Email address required');
    //         email.parentElement.classList.add('incorrect');
    //     }
    //     if (Password === '' || Password == null) {
    //         errors.push('You must set a Password');
    //         password.parentElement.classList.add('incorrect');
    //     }
    //     if (Password !== confirmpassword) {
    //         errors.push('Password Does not match the Repeated Password');
    //         password.parentElement.classList.add('incorrect');
    //         confirmPassword.parentElement.classList.add('incorrect');
    //     }
    //     return errors;
    // }

//     function getLoginFormErrors(Email, Password) {
//         let errors = [];
//         if (Email === '' || Email == null) {
//             errors.push('Email address required');
//             email.parentElement.classList.add('incorrect');
//         }
//         if (Password === '' || Password == null) {
//             errors.push('Password cannot be empty!!');
//             password.parentElement.classList.add('incorrect');
//         }
//         return errors;
//     }

//     const allInputs = [username, email, password, confirmPassword].filter(input => input != null);
//     allInputs.forEach(input => {
//         input.addEventListener('input', () => {
//             if (input.parentElement.classList.contains('incorrect')) {
//                 input.parentElement.classList.remove('incorrect');
//                 errorMessage.innerText = '';
//             }
//         });
//     });
// });




















// document.addEventListener('DOMContentLoaded', () => {
//     const formData = document.getElementById('myform')
//     const username = document.getElementById('username')
//     const email = document.getElementById('email')
//     const password = document.getElementById('password')
//     const confirmPassword = document.getElementById('confirm_password')
//     const errorMessage = document.getElementById('error-message')
//     formData.addEventListener('submit',(e)=>{
//         let errors = []
//         if (username){
//             errors = getSignupFormErrors(username.value, email.value,password.value,confirmPassword.value)
    
//         }else{
//             //We are in login forms
//             errors = getLoginFormErrors(email.value,password.value)
//         }
    
//         if (errors.length > 0){
//             //if errors in the array
//             console.log(errors)
//             e.preventDefault()
//             errorMessage.innerText = errors.join(". ")
//         }
//     })
    
//     function getSignupFormErrors(userName,Email,Password,confirmpassword){
//         let errors=[]
//         if(userName === ''|| userName==null){
//             errors.push('Username required')
//             username.parentElement.classList.add('incorrect')
//         }
//         if(Email === ''|| Email==null){
//             errors.push('Email address required')
//             email.parentElement.classList.add('incorrect')
//         }
//         if(Password === ''|| Password==null){
//             errors.push('You must set a Password')
//             password.parentElement.classList.add('incorrect')
//         }
        
//         if(Password !== confirmpassword){
//             errors.push('Password Does not match the Repeated Password')
//             password.parentElement.classList.add('incorrect')
//             confirmPassword.parentElement.classList.add('incorrect')
//         }
//         return errors;
//     }
//     function getLoginFormErrors(Email,Password){

//         let errors=[]
//         if(Email === ''|| Email==null){
//             errors.push('Email address required')
//             email.parentElement.classList.add('incorrect')
//         }
//         if(Password === ''|| Password==null){
//             errors.push('Password cannot be empty!!')
//             password.parentElement.classList.add('incorrect')
//         }
//         return errors;

//     }
  

//     const allInputs =[username,email,password,confirmPassword].filter(input => input != null)
//     allInputs.forEach(input =>{
//         input.addEventListener('input', ()=>{
//             if(input.parentElement.classList.contains('incorrect')){
//                 input.parentElement.classList.remove('incorrect')
//                  errorMessage.innerText =''
//              }
//         })
//     })
// })