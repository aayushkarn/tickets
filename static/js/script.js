// document.getElementById('nav-toggle').addEventListener('click', function() {
//     var menu = document.getElementById('collapse-navbar');
//     if (menu.style.display === 'none') {
//        menu.style.display = 'block';
//     } else {
//        menu.style.display = 'none';
//     }
//    });

document.querySelector('.nav-toggle').addEventListener('click', function() {
    var navItems = document.querySelector('.collapse-navbar');
    navItems.classList.toggle('show');
});

// carousel
let slides = document.querySelectorAll('.slide');
let currentSlide = 0;

function changeSlide() {
    slides[currentSlide].style.display = 'none';
    currentSlide = (currentSlide + 1) % slides.length;
    slides[currentSlide].style.display = 'block';
}

setInterval(changeSlide, 10000);
