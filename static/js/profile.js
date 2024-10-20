function getQueryParameter(param) {
    let urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// JWT 토큰을 로컬 스토리지에서 가져오는 함수
function getJwtToken() {
    return localStorage.getItem('access_token'); 
}

// 서버에서 유저 아이디 받아오기
function fetchCurrentUserId() {
    const token = getJwtToken();

    return fetch('/api/performances/api/user/status/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch user info');
        }
        return response.json();
    })
    .then(data => {
        return data.user_id;
    })
    .catch(error => {
        console.error('Error fetching user ID:', error);
        return null;
    });
}

// 사용자 인증 상태 확인 함수, 인증 상태에 따라 UI 업데이트
function checkUserAuthentication() {
    const token = getJwtToken();
    const navSigninBtn = document.getElementById('nav-signin-btn');
    const navSignupBtn = document.getElementById('nav-signup-btn');
    const navSignoutBtn = document.getElementById('nav-signout-btn');
    const navProfileBtn = document.getElementById('nav-profile-btn');
    const navRecommendationsBtn = document.getElementById('nav-recommendations-btn');

    if (!token) {
        // 토큰이 없는 경우
        navSigninBtn.style.display = 'block';
        navSignupBtn.style.display = 'block';
        navSignoutBtn.style.display = 'none';
        navProfileBtn.display = 'none';
        navRecommendationsBtn.style.display = 'none';
        return;
    }

    // JWT 토큰을 Authorization 헤더에 추가하여 API 요청
    fetch('/api/performances/api/user/status/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`, 
        }
    })
    .then(response => {
        if (response.ok) {
            navSigninBtn.style.display = 'none';
            navSignupBtn.style.display = 'none';
            navSignoutBtn.style.display = 'block';
            navProfileBtn.display = 'block';
            navRecommendationsBtn.style.display = 'block';
        } else {
            navSigninBtn.style.display = 'block';
            navSignupBtn.style.display = 'block';
            navSignoutBtn.style.display = 'none';
            navProfileBtn.display = 'none';
            navRecommendationsBtn.style.display = 'none';
        }
    })
    .catch(error => console.error('Error fetching user status:', error));
}


document.addEventListener('DOMContentLoaded', () => {
    const UserReviewsLikesContainer = document.getElementById('user-reviews-likes-container');
    const userReviewsContainer = document.getElementById('user-reviews-container');
    const userLikesContainer = document.getElementById('user-likes-container');

    fetchCurrentUserId.then((userId) => {
        if (!userId) {

        }
    })


})