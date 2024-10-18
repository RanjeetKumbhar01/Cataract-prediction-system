<script type="module">
  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-app.js";
  import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-analytics.js";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyCEg6imc99Lof26pww78KADbUF7pj_vGhM",
    authDomain: "cataract-classification-system.firebaseapp.com",
    projectId: "cataract-classification-system",
    storageBucket: "cataract-classification-system.appspot.com",
    messagingSenderId: "214128466244",
    appId: "1:214128466244:web:44c5734349cd52c4f05f11",
    measurementId: "G-MBJB9LKKFC"
  };


// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Initialize Firebase Authentication
const auth = firebase.auth();

// Register user with Firebase
document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();  // Prevent the default form submission behavior

    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    // Use Firebase Auth to register the user
    auth.createUserWithEmailAndPassword(email, password)
        .then((userCredential) => {
            // Registered successfully
            const user = userCredential.user;
            console.log('User registered:', user);
            document.getElementById('authMessage').innerText = 'User registered successfully: ' + user.email;
        })
        .catch((error) => {
            // Error handling
            const errorMessage = error.message;
            document.getElementById('authMessage').innerText = 'Error: ' + errorMessage;
            console.error('Registration error:', error);
        });
});