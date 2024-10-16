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
    const checkboxes = document.querySelectorAll('.tag-checkbox');
    const recommendationBtn = document.querySelector('recommendation-btn');
    const recommendationsContainer = document.getElementById('recommendations-container');

    // 공연 추천 endpoint에 필요한 유저 아이디 받아오기



    function generateRecommendations(selectedTags) {
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
    };

    recommendationBtn.addEventListener('click', (event) => {
        event.preventDefault();

        // 유저가 선택한 해시태그 받기
        const selectedTags = Array.from(checkboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.labels[0].textContent);

        const userData = {
            tags: selectedTags
        }

        fetch('/api/performances/recommend/${userId}/', {
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
            generateRecommendations(data.recommendedPerformances);
        })
        .catch(error => console.error('Error:', error));
    });
});
