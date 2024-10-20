function isLoggedIn() {
    return document.cookie.includes('user_id=');
}

// 로그인 상태에 따라 표시되는 버튼 바꾸기
window.onload = function () {
    const navSigninBtn = document.getElementById('nav-signin-btn');
    const navSignupBtn = document.getElementById('nav-signup-btn');
    const navSignoutBtn = document.getElementById('nav-signout-btn');
    const navProfileBtn = document.getElementById('nav-profile-btn');
    const navRecommendationsBtn = document.getElementById('nav-recommendations-btn');

    if (isLoggedIn()) {
        // 로그인 되어있으면 signout, profile 버튼만 보이게
        navSigninBtn.style.display = 'none';
        navSignupBtn.style.display = 'none';
        navSignoutBtn.style.display = 'block';
        navProfileBtn.style.display = 'block';
        navRecommendationsBtn.style.display = 'block';
    } else {
        // 로그인 되어있지 않으면 signin, signup 버튼만 보이게
        navSigninBtn.style.display = 'block';
        navSignupBtn.style.display = 'block';
        navSignoutBtn.style.display = 'none';
        navProfileBtn.style.display = 'none';
        navRecommendationsBtn.style.display = 'none';
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
                console.log(data);
                // 로그인 성공 시 쿠키에 유저 아이디 저장
                var result = document.getElementById('result');
                result.innerHTML = '';
                document.cookie = `user_id=${data.user_id}; path=/`;
                result.innerHTML = `<div>${data.refresh}</div>`;
                saveToken(data.access);
                window.history.back();
            })
            .catch(error => {
                console.error('Error:', error);
                var result = document.getElementById('result');
                result.innerHTML = `<div style="color:red;">Login failed. Please check your credentials.</div>`;
            });
    });
});

function saveToken(token) {
    localStorage.setItem('access_token', token);
}