// Bên trong file load-navbar.js
fetch('navbar.html') // Đường dẫn tới file HTML của bạn
    .then(response => response.text())
    .then(data => {
        // Nhúng HTML vào thẻ div#navbar
        document.getElementById('navbar').innerHTML = data;
        
        setActiveNav(); 
    })
    .catch(error => console.error('Lỗi khi tải navbar:', error));

function setActiveNav() {
    // 1. Lấy đường dẫn hiện tại của trình duyệt (Ví dụ: "/about", "/contact")
    let currentPath = window.location.pathname;

    // Nếu người dùng vào thẳng trang chủ (chỉ có "/"), gán mặc định là "/index"
    if (currentPath === '/' || currentPath === '') {
        currentPath = '/index';
    }

    // 2. Lấy tất cả các thẻ nav__item
    const navItems = document.querySelectorAll('.nav__item');

    // 3. Xóa class 'active' ở tất cả các thẻ đi (để reset)
    navItems.forEach(item => {
        item.classList.remove('active');
    });

    // 4. Tìm thẻ <a> có href trùng khớp với đường dẫn hiện tại
    const activeLink = document.querySelector(`.nav__item a[href="${currentPath}"]`);

    const line = document.querySelector('.nav__line')

    line.style.left = activeLink.offsetLeft + 'px';
    line.style.width = activeLink.offsetWidth + 'px';

    // 5. Nếu tìm thấy, thêm class 'active' vào thẻ cha (.nav__item) chứa nó
    if (activeLink) {
        activeLink.parentElement.classList.add('active');
    }
}