document.getElementById('accountsForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let birthday= document.getElementById('birthday').value
    if (!birthday){
        birthday=null
    }
    let userData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        username: document.getElementById('username').value,
        gender: document.getElementById('gender').value,
        birthday: birthday
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
                return response.json().then(errors => {
                    alert(errors.message);
                });
            }
            return response.json();
        })
        .then(data => {
            document.cookie = `user_id=${data.user_id}; path=/`;
            saveToken(data.access, data.refresh, data.user_id);
            let myModal = new bootstrap.Modal(document.getElementById('signup'));
            myModal.show();
        }) 
        .catch(error => console.error('Error:', error));
});

function saveToken(access, refresh, user_id) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    localStorage.setItem('user_id', user_id);
}

document.getElementById('modal-confirm-btn').addEventListener('click', function () {
    window.location.href = 'main.html';
});
document.getElementById('modal-close-btn').addEventListener('click', function () {
    window.location.href = 'main.html';
});