import { saveToLocalStorage, loadFromLocalStorage } from "./../../helpers/localStorage.js";

const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');
const logo = document.querySelector('#sidebar .brand .text');
const dashboardNav = document.querySelector('.dashboard .dashboard-nav');

const sidebarStateKey = 'isDashboardSidebarHidden';

menuBar.addEventListener('click', function () {
    let isSidebarHidden = sidebar.classList.contains('hide');
    console.log("🚀 ~ isSidebarHidden (after click):", isSidebarHidden)

    if (isSidebarHidden) {
        displayElements(true);
    }
    else {
        displayElements(false);
    }

    saveToLocalStorage(sidebarStateKey, isSidebarHidden);
});

export function loadSidebarState() {
    let isSidebarHidden = loadFromLocalStorage(sidebarStateKey);
    /* ! after page loaded, class is added, animation is toggled (bad) */

    if (isSidebarHidden) {
        console.log('- if -');
       displayElements(false);
    } else {
        console.log('- else -');
        displayElements(true);
    }

    console.log('- sidebar is set to:', isSidebarHidden);
}

function displayElements(show) {
    if (show) {
        sidebar.classList.remove('hide');
        logo.classList.remove('visually-hidden');
        // dashboardNav.remove('hide')
    }
    else {
        sidebar.classList.add('hide');
        logo.classList.add('visually-hidden');
        // dashboardNav.classList.add('hide')
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