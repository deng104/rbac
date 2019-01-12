$(document).ready(
    $('.multi-menu .title').on('click', function () {
        $(this).next('.body').toggleClass('hide');
        $(this).parent().siblings('.item').find('.body').addClass('hide');
    })
);