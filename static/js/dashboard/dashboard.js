import { loadColorScheme, saveColorScheme } from "../ui/colorScheme.js";
import { loadSidebarState } from "./parts/sidebar.js";

function onLoad() {
    loadColorScheme();
    loadSidebarState();
}

onLoad();

const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

allSideMenu.forEach(item => {
    const li = item.parentElement;

    item.addEventListener('click', function () {
        allSideMenu.forEach(i => {
            i.parentElement.classList.remove('active');
        })
        li.classList.add('active');
    })
});


// Arama butonunu toggle etme
const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
    if (window.innerWidth < 768) {
        e.preventDefault();
        searchForm.classList.toggle('show');
        if (searchForm.classList.contains('show')) {
            searchButtonIcon.classList.replace('bx-search', 'bx-x');
        } else {
            searchButtonIcon.classList.replace('bx-x', 'bx-search');
        }
    }
})

// Dark Mode Switch
const switchMode = document.getElementById('switch-mode');

switchMode.onchange = () => {
    console.log('- switchMode.checked -', switchMode.checked);

    saveColorScheme(switchMode.checked);
}

// Notification Menu Toggle
document.querySelector('.notification').addEventListener('click', function () {
    document.querySelector('.notification-menu').classList.toggle('show');
    document.querySelector('.profile-menu').classList.remove('show'); // Close profile menu if open
});

// Profile Menu Toggle
document.querySelector('.profile').addEventListener('click', function () {
    document.querySelector('.profile-menu').classList.toggle('show');
    document.querySelector('.notification-menu').classList.remove('show'); // Close notification menu if open
});

// Close menus if clicked outside
window.addEventListener('click', function (e) {
    if (!e.target.closest('.notification') && !e.target.closest('.profile')) {
        document.querySelector('.notification-menu').classList.remove('show');
        document.querySelector('.profile-menu').classList.remove('show');
    }
});

// Menülerin açılıp kapanması için fonksiyon
function toggleMenu(menuId) {
    var menu = document.getElementById(menuId);
    var allMenus = document.querySelectorAll('.menu');

    // Diğer tüm menüleri kapat
    allMenus.forEach(function (m) {
        if (m !== menu) {
            m.style.display = 'none';
        }
    });

    // Tıklanan menü varsa aç, yoksa kapat
    if (menu.style.display === 'none' || menu.style.display === '') {
        menu.style.display = 'block';
    } else {
        menu.style.display = 'none';
    }
}

// Başlangıçta tüm menüleri kapalı tut
document.addEventListener("DOMContentLoaded", function () {
    var allMenus = document.querySelectorAll('.menu');
    allMenus.forEach(function (menu) {
        menu.style.display = 'none';
    });
});