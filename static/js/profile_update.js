function getJwtToken() {
    return {
    access : localStorage.getItem('access_token'),
    refresh : localStorage.getItem('refresh_token'),
    user_id : localStorage.getItem('user_id')
    }
    }

document.getElementById('accountupdateForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let password = document.getElementById('password').value,
        username = document.getElementById('username').value,
        gender = document.getElementById('gender').value,
        birthday= document.getElementById('birthday').value
    if (!password){
        password=null
    }
    if (!username){
        username=null
    }
    if (!gender){
        gender=null
    }
    if (!birthday){
        birthday=null
    }
    username
    let userData = {
        password: password,
        username: username,
        gender: gender,
        birthday: birthday,
    };

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
                return response.json().then(errors => {
                    alert(errors.message);
                    //document.getElementById('response').innerText = errors.message;
                    //throw new Error(errors.message);
                });
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('response').innerText = data.message;
            let myModal = new bootstrap.Modal(document.getElementById('accountupdate'));
            myModal.show();
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('modal-confirm-btn').addEventListener('click', function () {
    window.location.href = 'profile.html';
});
document.getElementById('modal-close-btn').addEventListener('click', function () {
    window.location.href = 'profile.html';
});

