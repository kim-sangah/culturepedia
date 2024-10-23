window.onload = function () {

    fetch('/api/performances/', {
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
                <div class="card mb-4" style="height: 300px;">
                    <div class="row g-0">
                        <div class="col-md-4">
                            <div style="float:left">${item.순위}&nbsp&nbsp&nbsp</div>
                            <div>${item.포스터 ? `<img src="http://www.kopis.or.kr/${item.포스터}" class="img-fluid rounded-start" alt="${item.공연명}" style="height: 280px">` : '이미지 없음'}</div>
                        </div>
                        <div class="col-md-8">
                            <div class="card-body">
                                <h5 class="card-title">${item.공연명}</h5>
                                <p class="card-text">${item.공연기간}</p>
                                <p class="card-text"><small class="text-body-secondary">${item.장르}</small></p>
                            </div>
                        </div>
                    </div>
                </div>
                `
            });
            checkUserAuthentication();
        })
        .catch(error => {
            console.error('Error: ', error);
        });
};