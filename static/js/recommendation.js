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

document.addEventListener("DOMContentLoaded", () => {
    const checkboxes = document.querySelectorAll('.tag-checkbox');
    const recommendationBtn = document.querySelector('recommendation-btn');
    const recommendationsContainer = document.getElementById('recommendations-container');

    // User ID 받아오기
    fetchCurrentUserId().then(userId => {
        if (!userId) {
            console.error('User ID not found.')
            return;
        }

        recommendationBtn.addEventListener('click', (event) => {
            event.preventDefault();

            // 유저가 선택한 해시태그 받기
            const selectedTags = Array.from(checkboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.labels[0].textContent);

            const userData = {
                tags: selectedTags
            }

            // 유저 아이디로 공연 추천 받기 위해 API 요청
            fetch(`/api/performances/recommend/${userId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer <token>'
                },
                body: JSON.stringify(userData)
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    generateRecommendations(data.recommendations);
                })
                .catch(error => console.error('Error generating recommendations'));
        });
    });

    function generateRecommendations(recommendations) {
        // 추천 공연 리스트 영역 초기화
        recommendationsContainer.innerHTML = '';

        recommendedPerformances.forEach(performance => {
            const card = `
                <div class="card">
                    <a href="${performance.link}"><img class="card-img-top" src="${performance.image}" alt="${performance.title} 포스터"></a>
                    <div class="card-body">
                        <h5 class="card-title">${performance.title}</h5>
                        <p class="card-state">${performance.state}</p>
                        <p class="card-start-date">시작일자: ${performance.startDate}</p>
                        <p class="card-end-date">종료일자: ${performance.endDate}</p>
                        <p class="card-facility-name">${performance.facility}</p>
                        <p class="card-hashtags">해시태그: ${performance.hashtags.join(', ')}</p>
                    </div>
                </div>
            `;
            recommendationsContainer.innerHTML += card;
        });
    }
});
