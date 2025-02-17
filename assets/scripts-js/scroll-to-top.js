const scrollToTopButton = document.getElementById('scrollToTop');

window.addEventListener('scroll', function () {
    if (window.scrollY > 300) { // Кнопка появляется при прокрутке 300px
        scrollToTopButton.classList.add('visible'); // Показать кнопку с плавным переходом
    } else {
        scrollToTopButton.classList.remove('visible'); // Скрыть кнопку с плавным переходом
    }
});

scrollToTopButton.addEventListener('click', function () {
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // Плавный скролл наверх
    });
});
