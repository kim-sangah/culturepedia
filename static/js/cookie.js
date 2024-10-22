// JWT 토큰을 로컬 스토리지에서 가져오는 함수
function getJwtTokens() {
    return {
        accessToken: localStorage.getItem('access_token'),
        refreshToken: localStorage.getItem('refresh_token'),
        user_id: localStorage.getItem('user_id'),
    }
}

// 서버에서 유저 아이디 받아오기
function fetchCurrentUserId() {
    return new Promise(async (resolve, reject) => {
        try {
            const token = getJwtTokens();

            const response = await fetch('/api/performances/api/user/status/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token.accessToken}`,
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch user info');
            }

            const data = await response.json();
            resolve(data.user_id);  // Return user ID on success
        } catch (error) {
            console.error('Error fetching user ID:', error);
            resolve(null);  // Resolve as null if an error occurs
        }
    });
}

// 사용자 인증 상태 확인 함수, 인증 상태에 따라 UI 업데이트

function checkUserAuthentication() {
    const token = getJwtTokens();
    const navSigninBtn = document.getElementById('nav-signin-btn');
    const navSignupBtn = document.getElementById('nav-signup-btn');
    const navSignoutBtn = document.getElementById('nav-signout-btn');
    const navProfileBtn = document.getElementById('nav-profile-btn');
    const navRecommendationsBtn = document.getElementById('nav-recommendations-btn');
    const createReviewBtn = document.getElementById('create-review-btn');
    const LikeBtn = document.getElementById('like-btn');

    console.log(navSigninBtn, navSignupBtn, navSignoutBtn, navProfileBtn, navRecommendationsBtn, createReviewBtn, LikeBtn);

    if (!token.accessToken) {
        // 토큰이 없는 경우
        if (navSigninBtn) navSigninBtn.style.display = 'block';
        if (navSignupBtn) navSignupBtn.style.display = 'block';
        if (navSignoutBtn) navSignoutBtn.style.display = 'none';
        if (navProfileBtn) navProfileBtn.style.display = 'none';
        if (navRecommendationsBtn) navRecommendationsBtn.style.display = 'none';
        if (createReviewBtn) createReviewBtn.style.display = 'none';
        if (LikeBtn) LikeBtn.style.display = 'none';
        return;
    }
    // JWT 토큰을 Authorization 헤더에 추가하여 API 요청
    fetch('/api/performances/api/user/status/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token.accessToken}`,
        }
    })
        .then(response => {
            if (response.ok) {
                if (navSigninBtn) navSigninBtn.style.display = 'none';
                if (navSignupBtn) navSignupBtn.style.display = 'none';
                if (navSignoutBtn) navSignoutBtn.style.display = 'block';
                if (navProfileBtn) navProfileBtn.style.display = 'block';
                if (navRecommendationsBtn) navRecommendationsBtn.style.display = 'block';
                if (createReviewBtn) createReviewBtn.style.display = 'block';
                if (LikeBtn) LikeBtn.style.display = 'block';
            } else {
                if (navSigninBtn) navSigninBtn.style.display = 'block';
                if (navSignupBtn) navSignupBtn.style.display = 'block';
                if (navSignoutBtn) navSignoutBtn.style.display = 'none';
                if (navProfileBtn) navProfileBtn.style.display = 'none';
                if (navRecommendationsBtn) navRecommendationsBtn.style.display = 'none';
                if (createReviewBtn) createReviewBtn.style.display = 'none';
                if (LikeBtn) LikeBtn.style.display = 'none';
            }
        })
        .catch(error => console.error('Error fetching user status:', error));
}

// 페이지가 로드될 때 사용자 인증 상태 확인
window.onload = checkUserAuthentication;


function signout() {
    const token = getJwtTokens(); // 토큰을 가져옵니다.

    fetch('/api/accounts/signout/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token.accessToken}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ refresh: token.refreshToken })
    })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`Logout failed: ${response.status} - ${text}`);
                });
            }
            // 로그아웃 성공 시
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = 'main.html';
        })
        .catch(error => {
            console.error('Error during sign out:', error);
        });
}
