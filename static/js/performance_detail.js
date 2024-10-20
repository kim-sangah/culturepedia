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

// 공연 리뷰 받아오고 render, 인증 상태에 따라 각 리뷰 안에 수정, 삭제 버튼 추가
// 리뷰마다 수정/삭제 버튼에 고유 아이디 부여하고 버튼 클릭되면 리뷰 수정/리뷰 삭제 함수 호출
function fetchReviews(currentUserId) {
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
                // 버튼으로 수정
                    <button class="btn btn-primary edit-review-btn" id="edit-review-btn-${review.id}" data-review-id="${review.id}">리뷰 수정</button>
                    <button class="btn btn-danger delete-review-btn" id="delete-review-btn-${review.id}" data-review-id="${review.id}">리뷰 삭제</button>
                    </div>
                </div>
                `;
            } else {
                reviewHtml += `</div></div>`;
            }

            reviewContainer.innerHTML += reviewHtml;
        });

        // 리뷰 렌더링 된 후 리뷰 수정/삭제 버튼에 event listener 추가하기
        document.querySelectorAll('edit-review-btn').forEach(btn => {
            const reviewId = btn.getAttribute('data-review-id');
            btn.addEventListener('click', (event) => {
                event.preventDefault();
                handleReviewEdit(reviewId);
            });
        });

        document.querySelectorAll('delete-review-btn').forEach(btn => {
            const reviewId = btn.getAttribute('data-review-id');
            btn.addEventListener('click', (event) => {
                event.preventDefault();
                handleReviewDelete(reviewId);
            });
        });
    })
    .catch(error => console.error('Error fetching performance details:', error));
}

// 리뷰 작성 버튼에 event listener추가, 리뷰 작성 폼에서 데이터 입력받기
function handleReviewCreate() {
    const reviewContainer = document.getElementById('review');

    reviewContainer.innerHTML = '';
    reviewContainer.innerHTML += `
        <div class="card mb-4">
            <div class="card-body">
                <h5 class="card-title">리뷰 작성</h5>
                <form id="create-review-form">
                    <div class="mb-3">
                        <label for="create-review-title" class="form-label">리뷰 제목</label>
                        <input type="text" class="form-control" id="create-review-title" placeholder="리뷰 제목을 입력하세요" required>
                    </div>
                    <div class="mb-3">
                        <label for="create-review-content" class="form-label">리뷰 내용</label>
                        <textarea class="form-control" id="create-review-content" rows="4" placeholder="리뷰 내용을 입력하세요" required></textarea>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">별점</label>
                        <div id="rating" class="rating">
                            <input type="radio" id="star5" name="rating" value="5"><label for="star5">5점</label>
                            <input type="radio" id="star4" name="rating" value="4"><label for="star4">4점</label>
                            <input type="radio" id="star3" name="rating" value="3"><label for="star3">3점</label>
                            <input type="radio" id="star2" name="rating" value="2"><label for="star2">2점</label>
                            <input type="radio" id="star1" name="rating" value="1"><label for="star1">1점</label>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary" id="submit-review-btn">리뷰 제출</button>
                </form>
            </div>
        </div>
    `

    const submitReviewBtn = document.getElementById('submit-review-btn');
    submitReviewBtn.addEventListener('click', (event) => {
        event.preventDefault();

        const title = document.getElementById('create-review-title').value;
        const content = document.getElementById('create-review-content').value;
        const rating = document.querySelector('input[name="rating"]:checked').value;

        if (title && content && rating) {
            handleReviewSubmit(currentUserId, title, content, rating);
        } else {
            alert('모든 필드를 입력하세요.');
        }
    });
}

// 리뷰 업로드 기능
function handleReviewSubmit(currentUserId, title, content, rating) {
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
    .then(response => {
        if (!response.ok) {
            throw new Error('Review submission failed');
        }
        return response.json();
    })
    .then(data => {
        console.log('리뷰 업로드 완료: ', data);
        fetchReviews(currentUserId); // 업로드된 리뷰 포함해 다시 공연 리뷰 조회
    })
    .catch(error => console.error('Error submitting review:', error));
}

// 리뷰 수정 기능
function handleReviewEdit(reviewId) {
    fetch(`/api/performances/detail/review/${reviewId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getJwtToken()}`,
        }
    })
    .then(response => response.json())
    .then(data => {
        // 수정 전 리뷰 데이터를 modal에 넣기
        document.getElementById('edit-review-title').value = data.title;
        document.getElementById('edit-review-rating').value = data.rating;
        document.getElementById('edit-review-content').value = data.content;

        // Bootstrap JS함수로 modal 보여주기
        $('#editReviewModal').modal('show');

        // 수정 완료 버튼 눌렸을 때
        const saveChangesBtn = document.getElementById('save-edit-btn');
        saveChangesBtn.addEventListener('click', (event) => {
            event.preventDefault();

            // 수정된 리뷰 데이터 받기
            const editedReviewData = {
                title: document.getElementById('edit-review-title').value,
                rating: document.getElementById('edit-review-rating').value,
                content: document.getElementById('edit-review-content').value,
            };

            // put request 보내 리뷰 수정
            fetch(`/api/performances/detail/review/${reviewId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getJwtToken()}`,
                },
                body: JSON.stringify(editedReviewData)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Review updated: ', data);
                // 리뷰 수정 후 다시 공연 리뷰 조회
                fetchReviews(getJwtToken());

                // 수정 완료 후 모달 숨기기
                $('#editReviewModal').modal('hide');
            })
            .catch(error => console.error('Error updating review:', error));
        });
    })
    .catch(error => console.error('Error fetching review details:', error));
}


// 리뷰 삭제 기능
function handleReviewDelete(reviewId) {
    console.log(`Delete review with ID: ${reviewId}`);

    // Bootstrap JS함수로 리뷰 삭제 modal 보여주기
    $('#deleteReviewModal').modal('show');

    const deleteReviewConfirmBtn = document.getElementById('delete-review-cofirm-btn');
    // 이전에 설정해놓은 eventListener 없애서 한 번만 eventListener 추가되게함
    deleteReviewConfirmBtn.removeEventListener('click', handleDeleteConfirm); 
    deleteReviewConfirmBtn.addEventListener('click', handleDeleteConfirm);

    function handleDeleteConfirm(event) {
        event.preventDefault();

        // 리뷰 삭제
        fetch(`/api/performances/detail/review/${reviewId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${getJwtToken()}`,
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Review deletion failed');
            }
            return response.json();
        })
        .then(data => {
            console.log('Review deleted: ', data);
            // 리뷰 삭제 후 다시 공연 리뷰 조회
            fetchReviews(getJwtToken());

            // 리뷰 삭제 후 모달 숨기기
            $('#deleteReviewModal').modal('hide');
        })
        .catch(error => console.error('Error deleting review:', error));
    }
}

// 공연 찜하기 기능
function handlePerformanceLike(currentUserId) {
    // user_id가 null이면 로그인이 되지 않은 상태
    if (!currentUserId) {
        alert('로그인이 필요한 기능입니다.');
        return;
    }

    fetch(`/api/performances/detail/${performance_id}/like/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${getJwtToken()}`,
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
        console.log('공연 찜하기 성공: ', data);
        // 공연 찜하기 성공시 UI 업데이트
        const performanceLikeBtn = document.getElementById('performance-like-btn');
        heartIcon.style.color = 'red'; // 하트 아이콘 빨간색으로 변경
    })
}


// 페이지가 로드될 때 사용자 인증 상태 확인
window.onload = checkUserAuthentication;

const performance_id = getQueryParameter('performance_id');

window.onload = function () {
    // 공연 상세 정보 조회
    fetch(`/api/performances/detail/${performance_id}`, {
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

    // 리뷰 작성 버튼에 event listener 추가
    const createReviewBtn = document.getElementById('create-review-btn');
    createReviewBtn.addEventListener('click', (event) => {
        event.preventDefault();
        handleReviewCreate();
    });

    // 리뷰 조회, 리뷰 업로드 핸들링
    fetchCurrentUserId().then(currentUserId => {
        if (currentUserId) {
            checkUserAuthentication();
            fetchReviews(currentUserId);
            handleReviewSubmit(currentUserId);
        } else {
            console.error('User is not authenticated');
        }
    });

    // 찜하기 버튼에 event listener 추가
    const performanceLikeBtn = document.getElementById('performance-like-btn');
    performanceLikeBtn.addEventListener('click', (event) => {
        event.preventDefault();
        fetchCurrentUserId().then(currentUserId => {
            handlePerformanceLike(currentUserId);
        });
    });
};
