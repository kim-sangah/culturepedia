function isLoggedIn() {
    return document.cookie.includes('user_id=');
}

// 로그인 상태에 따라 표시되는 버튼 바꾸기
window.onload = function() {
    const signinBtn = document.getElementById('signin-btn');
    const signupBtn = document.getElementById('signup-btn');
    const signoutBtn = document.getElementById('signout-btn');
    const profileBtn = document.getElementById('profile-btn');

    if (isLoggedIn()) {
        // If the user is logged in, show signout and profile buttons
        signinBtn.style.display = 'none';
        signupBtn.style.display = 'none';
        signoutBtn.style.display = 'block';
        profileBtn.style.display = 'block';
    } else {
        // If the user is not logged in, show signin and signup buttons
        signinBtn.style.display = 'block';
        signupBtn.style.display = 'block';
        signoutBtn.style.display = 'none';
        profileBtn.style.display = 'none';
    }
};


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
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // 로그인 성공 시 쿠키에 유저 아이디 저장
            document.cookie = `user_id=${data.user_id}`;
        })
        .catch(error => console.error('Error:', error));
    });
});