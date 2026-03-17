// import { loadColorScheme, saveColorScheme } from "../ui/colorScheme.js";
import { loadSidebarState } from "./parts/sidebar.js";
import { saveToLocalStorage, loadFromLocalStorage } from "./../helpers/localStorage.js";

const sideMenuLinks = document.querySelectorAll('#sidebar .side-menu.top li a');
const activeSideMenuItemKey = "activeSideMenuLinkIndex";

function getDefaultProjectsIndex() {
    let defaultIndex = 0;
    sideMenuLinks.forEach((link, idx) => {
        if (link.textContent.trim() === 'Projects') {
            defaultIndex = idx;
        }
    });
    return defaultIndex;
}

function onLoad() {
    document.addEventListener('DOMContentLoaded', function () {
        loadSidebarState();
        setActiveSideMenuLink();
    });
}

onLoad();

sideMenuLinks.forEach((item, key) => {
    item.onclick = () => {
        if (key != 0) {
            saveToLocalStorage(activeSideMenuItemKey, key);
        }
    }
});


function setActiveSideMenuLink() {
    let savedIndex = parseInt(loadFromLocalStorage(activeSideMenuItemKey));

    if (isNaN(savedIndex)) {
        savedIndex = getDefaultProjectsIndex(); // default to 'Projects' link if no saved index
    }
    sideMenuLinks[savedIndex].parentElement.classList.add('active');
}

function toggleMenu(menuId) {
    var menu = document.getElementById(menuId);
    var allMenus = document.querySelectorAll('.menu');

    allMenus.forEach(function (m) {
        if (m !== menu) {
            m.style.display = 'none';
        }
    });

    if (menu.style.display === 'none' || menu.style.display === '') {
        menu.style.display = 'block';
    } else {
        menu.style.display = 'none';
    }
}

document.addEventListener("DOMContentLoaded", function () {
    var allMenus = document.querySelectorAll('.menu');
    allMenus.forEach(function (menu) {
        menu.style.display = 'none';
    });
});