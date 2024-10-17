function isLoggedIn() {
    return document.cookie.includes('user_id=');
}

// 로그인 상태에 따라 표시되는 버튼 바꾸기
window.onload = function() {
    const signinBtn = document.getElementById('signin-btn');
    const signupBtn = document.getElementById('signup-btn');
    const signoutBtn = document.getElementById('signout-btn');
    const profileBtn = document.getElementById('profile-btn');
    const recommendationsBtn = document.getElementById('nav-recommendations-btn');

    if (isLoggedIn()) {
        // If the user is logged in, show signout and profile buttons
        signinBtn.style.display = 'none';
        signupBtn.style.display = 'none';
        signoutBtn.style.display = 'block';
        profileBtn.style.display = 'block';
        recommendationsBtn.style.display = 'block';
    } else {
        // If the user is not logged in, show signin and signup buttons
        signinBtn.style.display = 'block';
        signupBtn.style.display = 'block';
        signoutBtn.style.display = 'none';
        profileBtn.style.display = 'none';
        recommendationsBtn.style.display = 'none';
    }
};

function getCookie(cookieName) {
    cookieName = `${cookieName}=`;
    let cookieData = document.cookie;

    let cookieValue = "";
    let start = cookieData.indexOf(cookieName);

    if (start !== -1) {
        start += cookieName.length;
        let end = cookieData.indexOf(";", start);
        if (end === -1) end = cookieData.length;
        cookieValue = cookieData.substring(start, end);
    }
    
    return unescape(cookieValue);
}

document.addEventListener("DOMContentLoaded", () => {
    const checkboxes = document.querySelectorAll('.tag-checkbox');
    const recommendationBtn = document.querySelector('recommendation-btn');
    const recommendationsContainer = document.getElementById('recommendations-container');

    // 공연 추천 endpoint에 필요한 유저 아이디 쿠키에서 읽어오기 위해 쿠키 받아오기
    function getCookie(name) {
        const cookieArr = document.cookie.split(";");
        for (let i = 0; i < cookieArr.length; i++) {
            let cookie = cookieArr[i].trim();
            if (cookie.startsWith(name + "=")) {
                return cookie.substring(name.length + 1);
            }
        }
        return null; // 쿠키를 찾지 못한 경우 return null 
    }

    const userId = getCookie('user_id'); // 쿠키에서 user_id 읽어오기

    if (!userId) {
        console.error('User ID not found in cookies.');
        return;
    }

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
        .catch(error => console.error('Error:', error));
    });
});
