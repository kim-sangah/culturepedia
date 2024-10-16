const performance_id = getQueryParameter('performance_id');

const url = `http://127.0.0.1:8000/api/performances/detail/${performance_id}`

window.onload = function () {
    fetch(url, {
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

            data.forEach(item => {
                result.innerHTML += `
                
                `
            });
        })
        .catch(error => {
            console.error('Error: ', error);
        });
};
