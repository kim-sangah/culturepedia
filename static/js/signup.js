document.getElementById('accountsForm').addEventListener('submit', function(event) {
    event.preventDefault();
    let userData = {        
        email: document.getElementById('email').value,
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        gender: document.getElementById('gender').value,
        birthday: document.getElementById('birthday').value,
    };

    fetch('/api/accounts/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('response').innerText = 'User created:' + data.message;
    }) //innerHTML
    .catch(error => console.error('Error:', error));
});