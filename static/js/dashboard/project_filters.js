document.addEventListener('DOMContentLoaded', function () {
    let searchIcon = document.getElementById('search-icon');
    let searchInput = document.getElementById('project-search-input');
    let resetButton = document.querySelector('.reset-button');

    searchIcon.onclick = function () {
        console.log('search icon clicked');
        if (!searchIcon.classList.contains('hidden')) {
            console.log('showing search input');
            searchInput.classList.remove('hidden');
            resetButton.classList.remove('hidden');
            searchIcon.classList.add('hidden');
            searchInput.focus();
        } else {
            console.log('hiding search input');
            searchInput.classList.add('hidden');
            searchIcon.classList.remove('hidden');
            resetButton.classList.add('hidden');
        }
    };

    searchInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            searchInput.form.submit();
        }
        if (e.key === 'Escape') {
            e.preventDefault();
            searchInput.classList.add('hidden');
            searchIcon.classList.remove('hidden');
            resetButton.classList.add('hidden');
        }
    });

    resetButton.onclick = function () {
        searchInput.value = '';
        searchInput.form.submit();
    };

    // Close input when clicking outside
    document.addEventListener('mousedown', function (e) {
        if (
            !searchInput.classList.contains('hidden') &&
            !searchInput.contains(e.target) &&
            !searchIcon.contains(e.target) &&
            !resetButton.contains(e.target)
        ) {
            searchInput.classList.add('hidden');
            searchIcon.classList.remove('hidden');
            resetButton.classList.add('hidden');
        }
    });
});