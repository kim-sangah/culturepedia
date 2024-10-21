function getQueryParameter(param) {
    let urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// 회원 탈퇴 기능
function handleAccountDelete() {


    // Bootstrap JS함수로 회원 탈퇴 modal 보여주기
    $('#deleteAccountModal').modal('show');

    const token = getJwtTokens();

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
                'Authorization': `Bearer ${token}.accessToken`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                password: passwordInput,
            }),
        })
        .then(response => response.json())
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
                deleteAccountCompleteBtn.addEventListener('click', function() {
                    window.location.href = '/main.html';
                });
            } else {
                alert('계정 삭제에 실패했습니다.');
            }
        })
        .catch(error => console.error('Error:', error));
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

        const token = getJwtTokens().accessToken;

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
        editUserInfoBtn.addEventListener('click', function() {
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
            let starRatingHtml = ''
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
                    <h5 class="card-title">${review.title}</h5>
                    <div class="rating">${starRatingHtml}</div>
                    <p class="card-text">${review.content}</p>
                    <button class="btn btn-primary edit-review-btn" id="edit-review-btn-${review.id}" data-review-id="${review.id}">리뷰 수정</button>
                    <button class="btn btn-danger delete-review-btn" id="delete-review-btn-${review.id}" data-review-id="${review.id}">리뷰 삭제</button>
                </div>
            </div>
            `;

            userReviewsContainer.innerHTML += reviewHtml;
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