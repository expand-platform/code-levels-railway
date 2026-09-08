const plus = document.getElementById('plus-button');

if (plus) {
  plus.addEventListener('click', function (event) {
    event.stopPropagation();
    if (event.target.closest('.plus__link')) {
      return;
    }
    plus.classList.toggle('plus--active');
  });

  document.addEventListener('click', function () {
    plus.classList.remove('plus--active');
  });
}
