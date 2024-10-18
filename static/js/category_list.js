function getQueryParameter(param) {
    let urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

let keyword = getQueryParameter('keyword');

if (keyword)
    query = `?keyword=${keyword}`
else
    query = ''

function displayPerformaces(category) {
    fetch(`/api/performances/search/${query}`, {
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
            const result = document.getElementById('result');

            result.innerHTML = '';  // 기존 내용을 비웁니다

            data.공연목록.forEach(item => {
                if (category === '전체' || category === '') {
                    result.innerHTML += `
                    <div class="card mb-4" style="height: 300px;">
                        <div class="row g-0">
                            <div class="col-md-4">
                                <div>${item.poster ? `<img src="${item.poster}" class="img-fluid rounded-start" alt="${item.title}" style="height: 280px">` : '이미지 없음'}</div>
                            </div>
                            <div class="col-md-8">
                                <div class="card-body">
                                    <h5 class="card-title"><a href="http://127.0.0.1:8000/static/performance_detail.html?performance_id=${item.kopis_id}">${item.title}</a></h5>
                                    <p class="card-text">${item.start_date}~${item.end_date}</p>
                                    <p class="card-text"><small class="text-body-secondary">${item.type}</small></p>
                                </div>
                            </div>
                        </div>
                    </div>
                    `
                } else if (category === '기타') {
                    if (item.type != '서커스/마술' & item.type != '뮤지컬' & item.type != '연극') {
                        result.innerHTML += `
                        <div class="card mb-4" style="height: 300px;">
                            <div class="row g-0">
                                <div class="col-md-4">
                                    <div>${item.poster ? `<img src="${item.poster}" class="img-fluid rounded-start" alt="${item.title}" style="height: 280px">` : '이미지 없음'}</div>
                                </div>
                                <div class="col-md-8">
                                    <div class="card-body">
                                        <h5 class="card-title"><a href="http://127.0.0.1:8000/static/performance_detail.html?performance_id=${item.kopis_id}">${item.title}</a></h5>
                                        <p class="card-text">${item.start_date}~${item.end_date}</p>
                                        <p class="card-text"><small class="text-body-secondary">${item.type}</small></p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        `
                    }
                } else if (item.type === category) {
                    result.innerHTML += `
                    <div class="card mb-4" style="height: 300px;">
                        <div class="row g-0">
                            <div class="col-md-4">
                                <div>${item.poster ? `<img src="${item.poster}" class="img-fluid rounded-start" alt="${item.title}" style="height: 280px">` : '이미지 없음'}</div>
                            </div>
                            <div class="col-md-8">
                                <div class="card-body">
                                    <h5 class="card-title"><a href="http://127.0.0.1:8000/static/performance_detail.html?performance_id=${item.kopis_id}">${item.title}</a></h5>
                                    <p class="card-text">${item.start_date}~${item.end_date}</p>
                                    <p class="card-text"><small class="text-body-secondary">${item.type}</small></p>
                                </div>
                            </div>
                        </div>
                    </div>
                    `
                }
            });
        })
        .catch(error => {
            console.error('Error: ', error);
        });
}

displayPerformaces('전체');

document.querySelectorAll("#pills-tab .nav-link").forEach(tab => {
    tab.addEventListener('click', () => {
        const activeTab = document.querySelector("#pills-tab .nav-link.active");
        const category = activeTab ? activeTab.textContent.trim() : '';
        displayPerformaces(category);
    });
});

// document.getElementById('searchButton').addEventListener('click', (event) => {
//     event.preventDefault();

//     const searchInput = document.getElementById('searchInput').value;
//     const params = new URLSearchParams();

//     // 검색어가 비어있지 않으면 쿼리 문자열에 추가
//     if (searchInput) {
//         params.append('search', searchInput);
//     }

//     const url = `/api/performances/search?${params.toString()}`; // 서버로 전달될 URL

//     fetch(url, {
//         method: 'GET',
//         headers: {
//             'Content-Type': 'application/json',
//         }
//     })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(data => {
//             const result = document.getElementById('result');

//             result.innerHTML = '';  // 기존 내용을 비웁니다

//             data.공연목록.forEach(item => {
//                 result.innerHTML += `
//                 <div class="card mb-4" style="height: 300px;">
//                     <div class="row g-0">
//                         <div class="col-md-4">
//                             <div>${item.poster ? `<img src="${item.poster}" class="img-fluid rounded-start" alt="${item.title}" style="height: 280px">` : '이미지 없음'}</div>
//                         </div>
//                         <div class="col-md-8">
//                             <div class="card-body">
//                                 <h5 class="card-title"><a href="http://127.0.0.1:8000/static/performance_detail.html?performance_id=${item.kopis_id}">${item.title}</a></h5>
//                                 <p class="card-text">${item.start_date}~${item.end_date}</p>
//                                 <p class="card-text"><small class="text-body-secondary">${item.type}</small></p>
//                             </div>
//                         </div>
//                     </div>
//                 </div>
//                 `
//             });
//         })
//         .catch(error => {
//             console.error('Error: ', error);
//         });
// });