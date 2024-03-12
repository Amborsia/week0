document.addEventListener('DOMContentLoaded', function () {
  var swiper = new Swiper('.swiper-container', {
    slidesPerView: 1, // 한 번에 하나의 슬라이드만 보입니다.
    spaceBetween: 0, // 슬라이드 사이의 간격을 없앱니다.
    loop: true, // 무한 루프를 활성화합니다.
    pagination: {
      el: '.swiper-pagination',
      clickable: true
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev'
    },
    effect: 'fade', // 슬라이드 전환 효과를 'fade'로 설정합니다.
    autoHeight: true, // 슬라이더의 높이를 슬라이드 내용에 맞춰 자동으로 조정합니다.
    centeredSlides: true // 슬라이드를 가운데에 배치합니다.
  })
})
