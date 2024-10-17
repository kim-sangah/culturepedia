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

    return fetch('/api/user/status/', {
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

    const signinBtn = document.getElementById('signin-btn');
    const signupBtn = document.getElementById('signup-btn');
    const signoutBtn = document.getElementById('signout-btn');
    const profileBtn = document.getElementById('profile-btn');
    const recommendationsBtn = document.getElementById('nav-recommendations-btn');
    const createReviewBtn = document.getElementById('create-review-btn');
    const LikeBtn = document.getElementById('like-btn');

    if (!token) {
        // 토큰이 없는 경우
        signinBtn.style.display = 'block';
        signupBtn.style.display = 'block';
        signoutBtn.style.display = 'none';
        profileBtn.display = 'none';
        recommendationsBtn.style.display = 'none';
        createReviewBtn.style.display = 'none';
        LikeBtn.style.display = 'none';
        return;
    }

    // JWT 토큰을 Authorization 헤더에 추가하여 API 요청
    fetch('/api/user/status/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`, 
        }
    })
    .then(response => {
        if (response.ok) {
            // 로그인된 경우 수정 및 삭제 버튼 보이기
            signinBtn.style.display = 'none';
            signupBtn.style.display = 'none';
            signoutBtn.style.display = 'block';
            profileBtn.display = 'block';
            recommendationsBtn.style.display = 'block';
            createReviewBtn.style.display = 'block';
            LikeBtn.style.display = 'block';
        } else {
            // 로그인하지 않은 경우 버튼 숨기기
            signinBtn.style.display = 'block';
            signupBtn.style.display = 'block';
            signoutBtn.style.display = 'none';
            profileBtn.display = 'none';
            recommendationsBtn.style.display = 'none';
            createReviewBtn.style.display = 'none';
            LikeBtn.style.display = 'none';
        }
    })
    .catch(error => console.error('Error fetching user status:', error));
}

// 공연 리뷰 받아오고 render
function fetchReviews(currrentUserId) {
    fetch(`http://127.0.0.1:8000/api/performances/detail/${performance_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json)
    .then(data => {
        const reviews = data.perform_reviews;
        const reviewContainer = document.getElementById('review');
        reviewContainer.innerHTML = '';

        reviews.forEach(review => {
            let starRatingHtml = '';
            for (let j = 1; j <= 5; j++) {
                if (j <= review.rating) {
                    starRatingHtml += `<i class="fas fa-star text-warning"></i>`;
                } else {
                    starRatingHtml += `<i class="far fa-star"></i>`;
                }
            }

            let reviewHtml = `
                <div class="card" style="width: 18rem;">
                    <div class="card-body">
                        <h5 class="card-title">${review.title}</h5>
                        <div class="rating">${starRatingHtml}</div>
                        <p class="card-text">${review.content}</p>
            `;

            if (review.author_id === currentUserId) {
                reviewHtml += `
                        <a href="#" class="btn btn-primary">리뷰 수정</a>
                        <a href="#" class="btn btn-danger">리뷰 삭제</a> 
                    </div>
                </div>
                `;
            } else {
                reviewHtml += `</div></div>`;
            }

            reviewContainer.innerHTML += reviewHtml;
        });
    })
    .catch(error => console.error('Error fetching performance details:', error));
}

// 리뷰 작성 버튼에 event listener 추가, 리뷰 업로드
function handleReviewSubmit(currentUserId) {
    const submitReviewBtn = document.getElementById('submit-review-btn');
    submitReviewBtn.addEventListener('click', (event) => {
        event.preventDefault();

        const title = document.getElementById('create-review-title').value;
        const rating = document.querySelector('input[name="rating"]:checked').value;
        const content = document.getElementById('create-review-content').value;

        const reviewData = {
            title,
            rating,
            content,
            author_id: currentUserId,
        };

        fetch(`/api/performances/detail/${performance_id}/review/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorzation': `Bearer ${getJwtToken()}`,
            },
            body: JSON.stringify(reviewData),
        })
        .then(response => response.json())
        .then(data => {
            console.log('리뷰 업로드 완료: ', data);
            // 작성된 리뷰 업로드 후 다시 리뷰 조회하기
            fetchReviews(currentUserId);
        })
        .catch(error => console.error('Error submitting review:', error));
    });
}


// 페이지가 로드될 때 사용자 인증 상태 확인
window.onload = checkUserAuthentication;

const performance_id = getQueryParameter('performance_id');

window.onload = function () {
    // 공연 상세 정보 조회
    fetch(`http://127.0.0.1:8000/api/performances/detail/${performance_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        var result = document.getElementById('result');
        result.innerHTML = '';  // 기존 내용을 비웁니다
        result.innerHTML += `
            <div class="card mb-4" style="height: 300px;">
                <div class="row g-0">
                    <div class="col-md-4">
                        <div><img src="${data.poster}" class="img-fluid rounded-start" alt="${data.title}" style="height: 280px"></div>
                    </div>
                    <div class="col-md-8 d-flex">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">${data.title}</h5>
                            <p class="card-text">${data.facility_name}</p>
                            <p class="card-text">${data.start_date} ~ ${data.end_date}</p>
                            <p class="card-text">${data.runtime}</p>
                            <div class="d-grid mt-auto">
                                <button class="btn btn-dark" type="button">Button</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            `
        var information = document.getElementById('information');
        var styurl = data.styurls.styurl
        information.innerHTML = '';
        if (Array.isArray(styurl)) {
            for (let i = 0; i < styurl.length; i++) {
                information.innerHTML += `
                    <img src="${styurl[i]}" class="img-fluid" alt="${data.title}">
                `;
            }
        } else {
            information.innerHTML += `
                <img src="${styurl}" class="img-fluid" alt="${data.title}">
            `;
        }
    });

    // 리뷰 조회
    fetchCurrentUserId().then(currentUserId => {
        if (currentUserId) {
            checkUserAuthentication();
            fetchReviews(currentUserId);
            handleReviewSubmit(currentUserId);
        } else {
            console.error('User is not authenticated');
        }
    });
};
