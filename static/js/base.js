fetch('./base.html') // sample.html 파일 경로
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