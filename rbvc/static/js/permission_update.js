$(document).ready(function () {
    $('.menu-btn').on('click', function () {
        $(this).find('i').toggleClass('fa-rotate-180').parent().parent().next('.panel-body').slideToggle();
    })
});