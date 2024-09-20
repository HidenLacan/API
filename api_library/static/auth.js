// Handle login form submission
document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault();  // Prevent the form from submitting the traditional way

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Send login data to the Django API for authentication
    fetch('/api/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access) {
            // Save the access and refresh tokens in localStorage
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);

            document.getElementById('response').innerHTML = 'Login successful! Tokens saved.';
        } else {
            document.getElementById('response').innerHTML = `Login failed: ${data.detail}`;
        }
    })
    .catch(error => {
        document.getElementById('response').innerHTML = `Error: ${error}`;
    });
});


// Retrieve the access token from localStorage
const token = localStorage.getItem('access_token');

if (token) {
    // Make an authenticated request to a protected endpoint
    fetch('/api/recommendations/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Process the data (e.g., display recommended books)
    })
    .catch(error => {
        console.error('Error:', error);
    });
} else {
    console.log('No token found, please log in.');
}


function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    document.getElementById('response').innerHTML = 'Logged out successfully.';
}

// Call this function when the user clicks a "Logout" button
document.getElementById('logout-button').addEventListener('click', logout);

