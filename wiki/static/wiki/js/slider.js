document.addEventListener('DOMContentLoaded', function () {
    const slider = document.querySelector('#slider');
    const btnLeft = document.querySelector('#btn-left');
    const btnRight = document.querySelector('#btn-right');
  
    if (!slider || !btnLeft || !btnRight) return;
  
    const sliderSections = slider.querySelectorAll('.slider__section');
    const totalSections = sliderSections.length;
    let index = 1;
  
    // Posición inicial
    slider.style.marginLeft = '-100%';
  
    function moveRight() {
      if (index >= totalSections - 1) return;
      index++;
      slider.style.transition = 'margin-left 0.5s';
      slider.style.marginLeft = `-${100 * index}%`;
    }
  
    function moveLeft() {
      if (index <= 0) return;
      index--;
      slider.style.transition = 'margin-left 0.5s';
      slider.style.marginLeft = `-${100 * index}%`;
    }
  
    btnRight.addEventListener('click', moveRight);
    btnLeft.addEventListener('click', moveLeft);
  });