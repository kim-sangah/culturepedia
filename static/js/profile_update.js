function getJwtToken() {
    return {
    access : localStorage.getItem('access_token'),
    refresh : localStorage.getItem('refresh_token'),
    user_id : localStorage.getItem('user_id')
    }
    }

document.getElementById('accountupdateForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let userData = {
        password: document.getElementById('password').value,
        username: document.getElementById('username').value,
        gender: document.getElementById('gender').value,
        birthday: document.getElementById('birthday').value,
    };
    var myModal = new bootstrap.Modal(document.getElementById('accountupdate'));
        myModal.show();

    const token = getJwtToken();

    fetch(`/api/accounts/profile/${token.user_id}/`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token.access}`,
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

document.getElementById('modal-confirm-btn').addEventListener('click', function () {
    window.location.href = 'profile.html';
});
document.getElementById('modal-close-btn').addEventListener('click', function () {
    window.location.href = 'profile.html';
});
