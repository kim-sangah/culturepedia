function getQueryParameter(param) {
    let urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
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
