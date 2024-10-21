function getQueryParameter(param) {
    let urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

document.addEventListener("DOMContentLoaded", async () => {
    const checkboxes = document.querySelectorAll('.tag-checkbox');
    const recommendationBtn = document.querySelector('recommendation-btn');
    const recommendationsContainer = document.getElementById('recommendations-container');

    try {
        // user ID 받아오기
        const userId = await fetchCurrentUserId();

        if (!userId) {
            console.error('User ID not found.');
            return;
        }

        recommendationBtn.addEventListener('click', async (event) => {
            event.preventDefault();

            const selectedTags = Array.from(checkboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.labels[0].textContent);

            const userData = {
                tags: selectedTags
            };

            try {
                // 추천 공연 받아오기
                const token = getJwtToken();

                const response = await fetch(`/api/performances/recommend/${userId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    body: JSON.stringify(userData)
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                generateRecommendations(data.recommendations);
            } catch (error) {
                console.error('Error generating recommendations:', error);
            }
        });
    } catch (error) {
        console.error('Error fetching user ID:', error);
    }

    function generateRecommendations(recommendations) {
        recommendationsContainer.innerHTML = '';

        recommendations.forEach(performance => {
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

