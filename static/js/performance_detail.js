function getQueryParameter(param) {
    let urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

const performance_id = getQueryParameter('performance_id');

window.onload = function () {
    fetch(`http://127.0.0.1:8000/api/performances/detail/${performance_id}`, {
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
            result.innerHTML += `
                <div class="card mb-4" style="height: 300px;">
                    <div class="row g-0">
                        <div class="col-md-4">
                            <div><img src="${data.poster}" class="img-fluid rounded-start" alt="${data.title}" style="height: 280px"></div>
                        </div>
                        <div class="col-md-8 d-flex">
                            <div class="card-body d-flex flex-column">
                                <h5 class="card-title">${data.title}</h5>
                                <p class="card-text">${data.facility_name}</p>
                                <p class="card-text">${data.start_date} ~ ${data.end_date}</p>
                                <p class="card-text">${data.runtime}</p>
                                <div class="d-grid mt-auto">
                                    <button class="btn btn-dark" type="button">Button</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                `
            var information = document.getElementById('information');
            var styurl = data.styurls.styurl
            information.innerHTML = '';
            if (Array.isArray(styurl)) {
                for (let i = 0; i < styurl.length; i++) {
                    information.innerHTML += `
                        <img src="${styurl[i]}" class="img-fluid" alt="${data.title}">
                    `;
                }
            } else {
                information.innerHTML += `
                    <img src="${styurl}" class="img-fluid" alt="${data.title}">
                `;
            }
        });
};
