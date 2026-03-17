import { saveToLocalStorage, loadFromLocalStorage } from "./../../helpers/localStorage.js";

const sidebarBurgerButton = document.querySelector('.dashboard-nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar') || document.querySelector('.sidebar');
const logo = document.querySelector('#sidebar .brand .text');
const dashboardNav = document.querySelector('.dashboard .dashboard-nav');

const sidebarStateKey = 'isDashboardSidebarHidden';

// false - visible, true - hidden, but save to localStorage as inversed value
sidebarBurgerButton.addEventListener('click', function () {
    let isSidebarHidden = sidebar.classList.contains('hide');

    if (isSidebarHidden) {
        displayElements(true);
    }
    else {
        displayElements(false);
    }

    saveToLocalStorage(sidebarStateKey, !isSidebarHidden);
});

export function loadSidebarState() {
    let isSidebarHidden = loadFromLocalStorage(sidebarStateKey);

    if (isSidebarHidden) {
        displayElements(false);
    } else {
        displayElements(true);
    }
}

function displayElements(show) {
    if (show) {
        sidebar.classList.remove('hide');
        logo.classList.remove('visually-hidden');
        dashboardNav.classList.remove('start-0', 'opened')
    }
    else {
        sidebar.classList.add('hide');
        logo.classList.add('visually-hidden');
        dashboardNav.classList.add('start-0', 'opened')
    }
}
