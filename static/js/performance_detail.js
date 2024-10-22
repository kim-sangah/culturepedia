

function getQueryParameter(param) {
    let urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// 공연 리뷰 받아오고 render, 인증 상태에 따라 각 리뷰 안에 수정, 삭제 버튼 추가
// 리뷰마다 수정/삭제 버튼에 고유 아이디 부여하고 버튼 클릭되면 리뷰 수정/리뷰 삭제 함수 호출
function fetchReviews(currentUserId) {
    fetch(`/api/performances/detail/${performance_id}/`, {
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

        currentUserId = getJwtTokens().user_id;

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
            'Authorization': `Bearer ${getJwtTokens().accessToken}`,
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
            'Authorization': `Bearer ${getJwtTokens().accessToken}`,
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
                        'Authorization': `Bearer ${getJwtTokens().accessToken}`,
                    },
                    body: JSON.stringify(editedReviewData)
                })
                    .then(response => response.json())
                    .then(data => {
                        // 리뷰 수정 후 다시 공연 리뷰 조회
                        fetchReviews(getJwtTokens().user_id);

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
                // 리뷰 삭제 후 다시 공연 리뷰 조회
                fetchReviews(getJwtTokens().user_id);

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
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getJwtTokens().accessToken}`,
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch likes');
        }
        return response.json();
    })
    .then(data => {
        const liked = data.liked;
    
        if (liked) {
            heartIcon.style.color = 'red';
            // 사용자가 이미 좋아요를 눌렀다면 좋아요 해제
            fetch(`/api/performances/detail/${performance_id}/like/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getJwtTokens().accessToken}`,
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to remove like');
                }
                return response.json();
            })
            .then(data => {
                heartIcon.style.color = '' // 좋아요 버튼 스타일 변경
            })
            .catch(error => console.error('Error removing like:', error));
        } else {
            heartIcon.style.color = '';
            // 사용자가 좋아요를 누르지 않았다면 좋아요 추가
            fetch(`/api/performances/detail/${performance_id}/like/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getJwtTokens().accessToken}`,
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to add like');
                }
                return response.json();
            })
            .then(data => {
                heartIcon.style.color = 'red' // 좋아요 버튼 스타일 변경
            })
            .catch(error => console.error('Error adding like:', error));
        }
    })
    .catch(error => console.error('Error fetching likes:', error));
}

const performance_id = getQueryParameter('performance_id');

let heartIcon;
window.onload = function () {
    // 공연 상세 정보 조회
    fetchPerformanceDetails();

    // 리뷰 작성 버튼에 event listener 추가
    const createReviewBtn = document.getElementById('create-review-btn');
    createReviewBtn.addEventListener('click', (event) => {
        event.preventDefault();
        handleReviewCreate();
    });

    // 찜하기 버튼에 event listener 추가
    const performanceLikeBtn = document.getElementById('performance-like-btn');
    performanceLikeBtn.addEventListener('click', async (event) => {
        event.preventDefault();
        await toggleLikeStatus();
    });
};

async function fetchPerformanceDetails() {
    try {
        const response = await fetch(`/api/performances/detail/${performance_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        displayPerformanceDetails(data);
        checkUserAuthentication();
        await initializeLikeStatus();
    } catch (error) {
        console.error('Error fetching performance details:', error);
    }
}

function displayPerformanceDetails(data) {
    const result = document.getElementById('result');
    result.innerHTML = `
        <div class="card mb-4" style="height: 300px;">
            <div class="row g-0">
                <div class="col-md-4">
                    <img src="${data.poster}" class="img-fluid rounded-start" alt="${data.title}" style="height: 280px">
                </div>
                <div class="col-md-8 d-flex">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">${data.title}</h5>
                        <p class="card-text">${data.facility_name}</p>
                        <p class="card-text">${data.start_date} ~ ${data.end_date}</p>
                        <p class="card-text">${data.runtime}</p>
                        <p class="card-text">${data.dtguidance}</p>
                    </div>
                </div>
            </div>
        </div>
    `;

    const information = document.getElementById('information');
    const styurl = data.styurls.styurl;
    information.innerHTML = Array.isArray(styurl) ? styurl.map(url => `<img src="${url}" class="img-fluid" alt="${data.title}">`).join('') : `<img src="${styurl}" class="img-fluid" alt="${data.title}">`;
}

async function initializeLikeStatus() {
    heartIcon = document.getElementById('heart-icon');
    const likeStatus = await checkLikeStatus(performance_id);
    updateLikeButtonStyle(likeStatus.liked, heartIcon);
}

async function toggleLikeStatus() {

    try {
        const currentUserId = await fetchCurrentUserId();
        if (!currentUserId) {
            console.error('User is not authenticated');
            return;
        }

        const likeStatus = await checkLikeStatus(performance_id);

        let result;
        if (likeStatus.liked) {
            result = await handlePerformanceUnlike(performance_id);
        } else {
            result = await handlePerformanceLike(performance_id);
        }
        
        updateLikeButtonStyle(!likeStatus.liked, heartIcon); // 버튼 스타일 업데이트
    } catch (error) {
        console.error('Error during toggle like status:', error);
    }
}

async function checkLikeStatus(performanceId) {
    try {
        const response = await fetch(`/api/performances/detail/${performanceId}/like/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${getJwtTokens().accessToken}`,
            },
        });
        if (!response.ok) {
            throw new Error('Failed to fetch like status');
        }
        const data = await response.json();
        return data; // 좋아요 상태 반환 (예: { liked: true })
    } catch (error) {
        console.error('Error fetching like status:', error);
        throw error;
    }
}
// 좋아요 추가하는 함수
async function handlePerformanceLike(performanceId) {
    try {
        const response = await fetch(`/api/performances/detail/${performanceId}/like/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getJwtTokens().accessToken}`,
            },
        });
        if (!response.ok) {
            throw new Error('Failed to like the performance');
        }
        const data = await response.json();
        return data; // 결과 반환
    } catch (error) {
        console.error('Error liking performance:', error);
        throw error; // 에러 발생 시 상위로 전달
    }
}
// 좋아요 취소하는 함수
async function handlePerformanceUnlike(performanceId) {
    try {
        const response = await fetch(`/api/performances/detail/${performanceId}/like/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${getJwtTokens().accessToken}`,
            },
        });
        if (!response.ok) {
            throw new Error('Failed to unlike the performance');
        }
        const data = await response.json();
        return data; // 결과 반환
    } catch (error) {
        console.error('Error unliking performance:', error);
        throw error; // 에러 발생 시 상위로 전달
    }
}

// 좋아요 상태에 따라 버튼 스타일을 업데이트하는 함수
function updateLikeButtonStyle(isLiked) {
    if (isLiked) {
        heartIcon.style.color = 'red' ; // 좋아요가 눌린 경우
    } else {
        heartIcon.style.color = ''; // 기본 스타일로 되돌리기
    }
}














