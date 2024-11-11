document.getElementById('authForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const submitButton = document.getElementById('submitButton');

    submitButton.disabled = true;
    submitButton.textContent = 'Submitting...';

    fetch('/api/auth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Log the response to debug
        submitButton.disabled = false;
        submitButton.textContent = 'Submit';
        if (data.success) {
            window.location.href = '/todo_list.html';
        } else {
            alert('Authentication failed. Please check your username and password.');
        }
    })
    .catch(error => {
        submitButton.disabled = false;
        submitButton.textContent = 'Submit';
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
});
