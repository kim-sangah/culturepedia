document.getElementById('accountsForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let userData = {
        email: document.getElementById('email').value,
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        gender: document.getElementById('gender').value,
        birthday: document.getElementById('birthday').value,
    };
    var myModal = new bootstrap.Modal(document.getElementById('signup'));
        myModal.show();

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
            // document.getElementById('response').innerText = 'User created:' + data.message;
            document.cookie = `user_id=${data.user_id}; path=/`;
            saveToken(data.access);
        }) 
        .catch(error => console.error('Error:', error));
});

document.getElementById('modal-confirm-btn').addEventListener('click', function () {
    window.location.href = 'main.html';
});
document.getElementById('modal-close-btn').addEventListener('click', function () {
    window.location.href = 'main.html';
});