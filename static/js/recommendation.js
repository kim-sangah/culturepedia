function getQueryParameter(param) {
    let urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}


document.addEventListener("DOMContentLoaded", async () => {
    const checkboxes = document.querySelectorAll('.tag-checkbox');
    const recommendationBtn = document.querySelector('#recommendation-btn');
    const recommendationsContainer = document.getElementById('recommendations-container');

    try {
        // user ID 받아오기
        const userId = await fetchCurrentUserId();

        if (!userId) {
            console.error('User ID not found.');
            return;
        }

        // 유저가 태그 입력하기 전 페이지 처음 로드될 때 리뷰하거나 찜한 공연 바탕으로 추천 공연 리스트 미리 표시
        await fetchRecommendations(userId, []);

        // 유저가 태그 입력하고 공연 추천 받기 버튼 클릭하면 입력받은 태그로 공연 추천
        recommendationBtn.addEventListener('click', async (event) => {
            event.preventDefault();

            const selectedTags = Array.from(checkboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.labels[0].textContent);

            try {
                await fetchRecommendations(userId, selectedTags);
            } catch (error) {
                console.error('Error generating recommendations:', error);
            }
        });

    } catch (error) {
        console.error('Error fetching user ID:', error);
    }

    async function fetchRecommendations(userId, inputTags) {
        try {
            const token = getJwtTokens();

            const response = await fetch(`/api/performances/recommend/${userId}/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token.accessToken}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ input_tags: inputTags })
            });

            const data = await response.json();

            if (!response.ok) {
                displayErrorMessage(data.error);
                return;
            }

            generateRecommendations(data.recommendations);
        } catch (error) {
            console.error('Error fetching recommendations:', error);
        }
    }

    function displayErrorMessage(errorMessage) {
        const recommendationsContainer = document.getElementById('recommendations-container');
        recommendationsContainer.innerHTML = `
            <div class="error-message">
                <p>${errorMessage}</p>
            </div>
        `;
    }

    function generateRecommendations(recommendations) {
        recommendationsContainer.innerHTML = '';

        recommendations.forEach(performance => {
            const card = `
                <div class="card">
                    <img class="card-img-top" src="${performance.poster}" alt="${performance.title} 포스터">
                    <div class="card-body">
                        <h5 class="card-title"><a href="http://127.0.0.1:8000/static/performance_detail.html?performance_id=${performance.kopis_id}">${performance.title}</a></h5>
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



