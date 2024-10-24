function getQueryParameter(param) {
    let urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}


// 회원 탈퇴 기능
function handleAccountDelete() {
    // Bootstrap JS함수로 회원 탈퇴 modal 보여주기
    $('#deleteAccountModal').modal('show');

    const closeModalBtn = document.querySelectorAll('.modal-header > .close');
    closeModalBtn.forEach(btn => btn.addEventListener('click', () => {
        $('#deleteAccountModal').modal('hide');
    }));

    const token = getJwtTokens();
    const userId = token.user_id;


    const deleteAccountConfirmBtn = document.getElementById('delete-account-confirm-btn');
    deleteAccountConfirmBtn.addEventListener('click', handleAccountDeleteConfirm);

    const deleteAccountCancelBtn = document.getElementById('delete-account-cancel-btn');
    deleteAccountCancelBtn.addEventListener('click', () => {
        $('#deleteAccountModal').modal('hide');
    });

    function handleAccountDeleteConfirm(event) {
        event.preventDefault();

        // 비밀번호 확인 modal 띄우기
        $('#checkPasswordModal').modal('show');

        const checkPasswordBtn = document.getElementById('password-check-btn');
        checkPasswordBtn.addEventListener('click', handlePasswordCheck);

    }

    function handlePasswordCheck(event) {
        event.preventDefault();

        const passwordInput = document.getElementById('password-check-input').value;
        fetch(`/api/accounts/profile/password-check/${userId}/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token.accessToken}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                password: passwordInput,
            }),
        })
            .then(response => {
                const contentType = response.headers.get('Content-Type');
                if (!response.ok) {
                    // If the response isn't OK, attempt to parse JSON error if possible
                    if (contentType && contentType.includes('application/json')) {
                        return response.json().then(errorData => {
                            alert(errorData.message);
                        });
                    } else {
                        // If not JSON, handle it as text (likely an HTML error page)
                        return response.text().then(errorText => {
                            console.error('Error (non-JSON):', errorText);
                            alert('An error occurred. Please try again.여기서 나는 에러');
                        });
                    }
                }
                return response.json(); // Parse valid JSON response
            })
            .then(data => {
                if (data.success) {
                    deleteAccount();
                } else {
                    alert('비밀번호가 올바르지 않습니다.');
                }
            })
            .catch(error => console.error('Error:', error));
    }

    function deleteAccount() {
        fetch(`/api/accounts/profile/${userId}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token.accessToken}`,
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                if (response.ok) {
                    // 회원 탈퇴 완료 modal 띄우기
                    $('#deleteAccountCompleteModal').modal('show');

                    const deleteAccountCompleteBtn = document.getElementById('delete-account-complete-btn');
                    deleteAccountCompleteBtn.addEventListener('click', function () {
                        window.location.href = 'main.html';
                    });
                } else {
                    alert('계정 삭제에 실패했습니다.');
                }
            })
            .catch(error => console.error('Error:', error));
    }
}

// 리뷰 수정 기능
function handleReviewEdit(reviewId) {
    editedReviewData = {
        title: document.getElementById(`review-title-${reviewId}`).value,
        content: document.getElementById(`review-content-${reviewId}`).value,
        rating: document.querySelector('input[name="rating"]:checked').value,
    }

    console.log(reviewId)
    // put request 보내 리뷰 수정
    fetch(`/api/performances/detail/review/${reviewId}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getJwtTokens().accessToken}`,
        },
        body: JSON.stringify(editedReviewData)
    })
        .then(response => response.json())
        .then(data => {
            location.reload()
        })
        .catch(error => console.error('Error updating review:', error));
}


// 리뷰 삭제 기능
function handleReviewDelete(reviewId) {
    // Bootstrap JS함수로 리뷰 삭제 modal 보여주기
    $('#deleteReviewModal').modal('show');

    const deleteReviewConfirmBtn = document.getElementById(`delete-review-btn-${reviewId}`);
    // 이전에 설정해놓은 eventListener 없애서 한 번만 eventListener 추가되게함
    deleteReviewConfirmBtn.removeEventListener('click', handleDeleteConfirm);
    deleteReviewConfirmBtn.addEventListener('click', handleDeleteConfirm);

    function handleDeleteConfirm(event) {
        event.preventDefault();

        // 리뷰 삭제
        fetch(`/api/performances/detail/review/${reviewId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${getJwtTokens().accessToken}`,
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
                location.reload()

            })
            .catch(error => console.error('Error deleting review:', error));
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    const userInfoContainer = document.getElementById('user-info-container');
    const userReviewsLikesContainer = document.getElementById('user-reviews-likes-container');
    const userReviewsContainer = document.getElementById('user-reviews-container');
    const userLikesContainer = document.getElementById('user-likes-container');

    try {
        const userId = await fetchCurrentUserId();

        if (!userId) {
            console.error('User ID not found.')
            return;
        }

        const token = getJwtTokens();

        const response = await fetch(`/api/accounts/profile/${userId}/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token.accessToken}`,
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('Failed to get user profile');
        }

        const data = await response.json();

        checkUserAuthentication();

        // 유저 기본 정보 (유저네임, 생일 etc... 표시)
        userInfoContainer.innerHTML = '';
        let userInfoHtml = `
        <div class="card" style="width: 18rem;">
            <div class="card-body">
                <p class="card-text">이메일: ${data.email}</p>
                <p class="card-text">유저네임: ${data.username}</p>
                <p class="card-text">성별: ${data.gender}</p>
                <p class="card-text">생년월일: ${data.birthday}</p>
                <button class="btn btn-primary" id="edit-user-info-btn">회원정보 수정</button>
                <button class="btn btn-danger" id="delete-account-btn">회원 탈퇴</button>
            </div>
        </div>
        `;

        userInfoContainer.innerHTML += userInfoHtml;

        // 회원정보 수정 버튼에 event listener 추가
        const editUserInfoBtn = document.getElementById('edit-user-info-btn');
        editUserInfoBtn.addEventListener('click', function () {
            window.location.href = 'profile_update.html';
        });

        // 회원 탈퇴 버튼에 event listener 추가
        const deleteAccountBtn = document.getElementById('delete-account-btn');
        deleteAccountBtn.addEventListener('click', (event) => {
            event.preventDefault();
            handleAccountDelete();
        });


        // 유저가 작성한 리뷰 표시
        userReviewsContainer.innerHTML = '';
        data.reviews.forEach(review => {
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
                    <div class="reviewed-performance-poster">
                        <img src="${review.performance.poster}">
                    </div>
                    <input type="text" class="form-control" id="review-title-${review.id}" value="${review.title}" placeholder="리뷰 제목">
                    <div id="rating" class="rating">
                        <input type="radio" id="star5" name="rating" value="5" ${review.rating === 5 ? 'checked' : ''}>
                        <label for="star5">5점</label>
                        <input type="radio" id="star4" name="rating" value="4" ${review.rating === 4 ? 'checked' : ''}>
                        <label for="star4">4점</label>
                        <input type="radio" id="star3" name="rating" value="3" ${review.rating === 3 ? 'checked' : ''}>
                        <label for="star3">3점</label>
                        <input type="radio" id="star2" name="rating" value="2" ${review.rating === 2 ? 'checked' : ''}>
                        <label for="star2">2점</label>
                        <input type="radio" id="star1" name="rating" value="1" ${review.rating === 1 ? 'checked' : ''}>
                        <label for="star1">1점</label>
                    </div>
                    <textarea class="form-control" id="review-content-${review.id}" rows="3" placeholder="리뷰 내용">${review.content}</textarea>
                    <button class="btn btn-primary edit-review-btn" id="edit-review-btn-${review.id}" data-review-id="${review.id}">리뷰 수정</button>
                    <button class="btn btn-danger delete-review-btn" id="delete-review-btn-${review.id}" data-review-id="${review.id}">리뷰 삭제</button>
                </div>
            </div>
            `;

            userReviewsContainer.innerHTML += reviewHtml;

            // 리뷰 수정 버튼에 이벤트 리스너 추가
            const editReviewBtn = document.getElementById(`edit-review-btn-${review.id}`);
            editReviewBtn.addEventListener('click', () => {
                handleReviewEdit(review.id);
            });

            // 리뷰 삭제 버튼에 이벤트 리스너 추가
            const deleteReviewBtn = document.getElementById(`delete-review-btn-${review.id}`);
            deleteReviewBtn.addEventListener('click', () => {
                handleReviewDelete(review.id);
            });
        });

        // 유저가 좋아요한 공연 표시
        userLikesContainer.innerHTML = '';
        data.likes.forEach(item => {
            let likedPerformanceHtml = `
                <div class="card mb-4" style="height: 300px;">
                    <div class="row g-0">
                        <div class="col-md-4">
                            <div>${item.poster ? `<img src="${item.poster}" class="img-fluid rounded-start" alt="${item.title}" style="height: 280px">` : '이미지 없음'}</div>
                        </div>
                        <div class="col-md-8">
                            <div class="card-body">
                                <h5 class="card-title"><a href="http://127.0.0.1:8000/static/performance_detail.html?performance_id=${item.kopis_id}">${item.title}</a></h5>
                                <p class="card-text">${item.start_date}~${item.end_date}</p>
                                <p class="card-text"><small class="text-body-secondary">${item.type}</small></p>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            userLikesContainer.innerHTML += likedPerformanceHtml;
        });
    } catch (error) {
        console.error('Error: ', error);
    }
});