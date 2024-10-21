function getJwtToken() {
    return localStorage.getItem('access_token');
}

function getUserId() {
    return localStorage.getItem('user_id');
}

document.getElementById('accountupdateForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let userData = {
        password: document.getElementById('password').value,
        username: document.getElementById('username').value,
        gender: document.getElementById('gender').value,
        birthday: document.getElementById('birthday').value,
    };

    const token = getJwtToken();

    fetch(`/api/accounts/profile/${userId}/`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token}`,
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
            document.getElementById('response').innerText = data.message;
        })
        .catch(error => console.error('Error:', error));
});