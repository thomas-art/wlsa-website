document.addEventListener('DOMContentLoaded', function () {
    const hoverElements = document.querySelectorAll('input, a, button, details, summary');
    const customCursor = document.getElementById('customCursor');
    const catchIco = document.getElementById('catchIco');

    hoverElements.forEach(function(element) {
        element.addEventListener('mouseenter', function(event) {
            catchIco.style.display = 'block';
            catchIcon.classList.remove('hide');
            catchIcon.classList.add('show');
        });
        element.addEventListener('mouseleave', function() {
            catchIcon.classList.add('hide');
            catchIcon.classList.remove('show');
        });
    });
    document.addEventListener('mousemove', function (event) {
        showCustomCursor();
        customCursor.style.top = event.clientY + 'px';
        customCursor.style.left = event.clientX - 10 + 'px';

        catchIcon.style.top = event.clientY - 13 + 'px';
        catchIcon.style.left = event.clientX - 20 + 'px';
    });
    window.addEventListener('mouseout', hideCustomCursor);
    function showCustomCursor() {
        customCursor.classList.remove('hide');
        customCursor.classList.add('show');
    }
    function hideCustomCursor() {
        customCursor.classList.add('hide');
        customCursor.classList.remove('show');
    }
});
