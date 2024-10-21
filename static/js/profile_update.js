function getJwtToken() {
    return {
    access : localStorage.getItem('access_token'),
    refresh : localStorage.getItem('refresh_token'),
    user_id : localStorage.getItem('user_id')
    }
    }

document.getElementById('accountupdateForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let birthday= document.getElementById('birthday').value
    if (!birthday){
        birthday=null
    }
    
    let userData = {        
            gender: document.getElementById('gender').value,
            birthday: birthday,
        };
        if (document.getElementById('username').value) {
            userData.username = document.getElementById('username').value;
        }
        if (document.getElementById('password').value) {
            userData.password = document.getElementById('password').value;
        }
    
    console.log(userData)

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

