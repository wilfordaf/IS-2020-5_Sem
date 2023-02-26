// execute function on window load
window.addEventListener('load', () => {
    // create Swiper object instance
    const swiper = new Swiper('.swiper-container', {
        // set direction of swiper
        direction: 'horizontal',
        // set speed of swiper
        speed: 500,
        // set amount of slides visible
        slidesPerView: 1,
        // enable infinite swiper
        loop: true,

        // set swiper visual effect to cube
        effect: "cube",
        // enable user to see grap cursor when hover on
        grabCursor: true,
        // add pretty shadow effect beneath the cube
        cubeEffect: {
          shadow: true,
          slideShadows: true,
          shadowOffset: 20,
          shadowScale: 0.94,
        },

        // add pagination panel in the bottom of a slide
        pagination: {
          el: ".swiper-pagination",
        },

        // enable auto swipe each 5 seconds
        autoplay: {
          delay: 5000,
        },
      });
});