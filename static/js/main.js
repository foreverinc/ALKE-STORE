$(document).ready(function () {
    $(".owl-carousel").owlCarousel({
        loop: true,
        margin: 10,
        responsiveClass: true,
        lazyLoad: true,
        nav: true,
        loop:true,
        navText: ['<i class="fa-solid fa-angles-left  text-success"></i>', '<i class="fa-solid fa-angles-right  text-success"></i>'],
        responsive: {
            0: {
                items: 1,
            },
            600: {
                items: 3,
            },
            1000: {
                items: 5,
            },
        },
    });
});
