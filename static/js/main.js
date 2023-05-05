$(document).ready(function () {
    $(".owl-carousel").owlCarousel({
      loop: true,
      margin: 10,
      responsiveClass: true,
      lazyLoad: true,
      nav: true,
      loop: true,
      autoplay: true,
      autoplayTimeout: 7000,
      navText: [
        '<i class="fa-solid fa-angles-left  text-success"></i>',
        '<i class="fa-solid fa-angles-right  text-success"></i>',
      ],
      responsive: {
        0: {
          items: 2,
        },
        600: {
          items: 3,
        },
        1000: {
          items: 6,
        },
      },
    });
});


function toggleTab() {
  const tab = document.querySelector(".tab");
  tab.classList.toggle("active");
}


$(document).ready(function () {
  // Add hover behavior to dropdown menu
  $(".dropdown").hover(
    function () {
      $(this).find(".dropdown-menu").stop(true, true).delay(0).fadeIn(300);
    },
    function () {
      $(this).find(".dropdown-menu").stop(true, true).delay(0).fadeOut(300);
    }
  );
});

