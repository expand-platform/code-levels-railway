document.addEventListener('DOMContentLoaded', function () {
    let searchIcon = document.getElementById('search-icon');
    let searchInput = document.getElementById('project-search-input');
    let resetButton = document.querySelector('.reset-button');

    searchIcon.onclick = function () {
        if (searchInput.style.display == 'none') {
            searchInput.style.display = 'block';
            resetButton.style.display = 'block';
            searchIcon.style.display = 'none';
            searchInput.focus();
        } else {
            searchInput.style.display = 'none';
            searchIcon.style.display = 'block';
        }
    };

    searchInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            searchInput.form.submit();
        }
        if (e.key === 'Escape') {
            e.preventDefault();
            searchInput.style.display = 'none';
            searchIcon.style.display = 'block';
            resetButton.style.display = 'none';
        }
    });

    resetButton.onclick = function () {
        searchInput.value = '';
        searchInput.form.submit();
    };

    // Close input when clicking outside
    document.addEventListener('mousedown', function (e) {
        if (
            searchInput.style.display === 'block' &&
            !searchInput.contains(e.target) &&
            !searchIcon.contains(e.target) &&
            !resetButton.contains(e.target)
        ) {
            searchInput.style.display = 'none';
            searchIcon.style.display = 'block';
            resetButton.style.display = 'none';
        }
    });
});