document.addEventListener('DOMContentLoaded', function () {
  const searchIcon = document.getElementById('search-icon');
  const searchInput = document.getElementById('project-search-input');
  const resetButton = document.querySelector('.reset-button');
  const showWorkoutsToggle = document.getElementById('show-workouts-toggle');
  const workoutsSwitchLabel = document.querySelector('.workouts-switch-label');
  const filterForm = document.querySelector('.projects-filters-form');

  if (!searchIcon || !searchInput || !resetButton) {
    return;
  }

  function setSearchOpen(isOpen) {
    searchInput.classList.toggle('hidden', !isOpen);
    resetButton.classList.toggle('hidden', !isOpen);
    searchIcon.classList.toggle('hidden', isOpen);
  }

  searchIcon.addEventListener('click', function () {
    const opening = searchIcon.classList.contains('hidden') === false;
    setSearchOpen(opening);
    if (opening) {
      searchInput.focus();
    }
  });

  searchInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      searchInput.form.submit();
    }
    if (e.key === 'Escape') {
      e.preventDefault();
      setSearchOpen(false);
    }
  });

  resetButton.addEventListener('click', function () {
    searchInput.value = '';
    searchInput.form.submit();
  });

  if (showWorkoutsToggle && filterForm) {
    showWorkoutsToggle.addEventListener('change', function () {
      filterForm.submit();
    });
  }

  document.addEventListener('mousedown', function (e) {
    if (searchInput.classList.contains('hidden')) {
      return;
    }
    const clickedInsideSearch =
      searchInput.contains(e.target) ||
      searchIcon.contains(e.target) ||
      resetButton.contains(e.target) ||
      (showWorkoutsToggle && showWorkoutsToggle.contains(e.target)) ||
      (workoutsSwitchLabel && workoutsSwitchLabel.contains(e.target));
    if (!clickedInsideSearch) {
      setSearchOpen(false);
    }
  });
});
