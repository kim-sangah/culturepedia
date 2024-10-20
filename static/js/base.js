function getSearchValue() {
    var keyword = document.getElementById('searchInput').value;

    window.location.href = `category_list.html?keyword=${keyword}`;
}

function handleKeyPress(event) {
    if (event.keyCode === 13) { // Enter key
        event.preventDefault();
        getSearchValue();
    }
}

fetch('./base.html')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text(); // 응답을 텍스트로 변환
    })
    .then(data => {
        document.getElementById('navbar').innerHTML = data; // 내용을 div에 삽입
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });