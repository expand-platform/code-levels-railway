import { saveToLocalStorage, loadFromLocalStorage } from "./../../helpers/localStorage.js";

const sidebarBurgerButton = document.querySelector('.dashboard-nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar') || document.querySelector('.sidebar');
const logo = document.querySelector('#sidebar .brand .text');
const dashboardNav = document.querySelector('.dashboard .dashboard-nav');

const sidebarStateKey = 'isDashboardSidebarHidden';

sidebarBurgerButton.addEventListener('click', function () {
    // false - visible, true - hidden, but save to localStorage as inversed value
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
        console.log('- if hidden -');
        displayElements(false);
    } else {
        console.log('- else (visible) -');
        displayElements(true);
    }

    console.log('- sidebar is set to:', isSidebarHidden);
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

// function adjustSidebar() {
//     if (window.innerWidth <= 576) {
//         displayElements(false);
//     } else {
//         displayElements(true);
//     }
// }

// Sayfa yüklendiğinde ve pencere boyutu değiştiğinde sidebar durumunu ayarlama
// window.addEventListener('load', adjustSidebar);
// window.addEventListener('resize', adjustSidebar);