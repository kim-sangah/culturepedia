function getQueryParameter(param) {
    let urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

document.addEventListener('DOMContentLoaded', () => {
    const UserReviewsLikesContainer = document.getElementById('user-reviews-likes-container');
    const userReviewsContainer = document.getElementById('user-reviews-container');
    const userLikesContainer = document.getElementById('user-likes-container');

    fetchCurrentUserId.then((userId) => {
        if (!userId) {

        }
    })


})