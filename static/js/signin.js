function isLoggedIn() {
    return document.cookie.includes('user_id=');
}

document.addEventListener("DOMContentLoaded", () => {
    const signinBtn = document.getElementById('signin-btn');

    signinBtn.addEventListener('click', (event) => {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // 유저가 로그인폼에 입력한 정보 받기
        const userCredentials = {
            'email': email,
            'password': password
        }

        fetch('/api/accounts/signin/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userCredentials)
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(response => {
                        alert(response.message);
                    })
                }
                return response.json();
            })
            .then(data => {
                // 로그인 성공 시 쿠키에 유저 아이디 저장
                var result = document.getElementById('result');
                result.innerHTML = '';
                document.cookie = `user_id=${data.user_id}; path=/`;
                saveToken(data.access, data.refresh, data.user_id);
                window.location.href = 'main.html';
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});

function saveToken(access_token, refresh_token, user_id) {
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    localStorage.setItem('user_id', user_id);
}