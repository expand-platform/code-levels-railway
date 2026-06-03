const sidebarBurgerButton = document.querySelector('.dashboard-nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar') || document.querySelector('.sidebar');
const logo = document.querySelector('#sidebar .brand .text');
const dashboardNav = document.querySelector('.dashboard .dashboard-nav');

const SUBMENU_MAX_HEIGHT = 450;

function addScrollbarToSubmenus() {
    const submenus = document.querySelectorAll('#sidebar .side-menu .submenu');

    submenus.forEach(submenu => {
        if (submenu.scrollHeight > SUBMENU_MAX_HEIGHT) {
            submenu.style.maxHeight = `${SUBMENU_MAX_HEIGHT}px`;
            submenu.style.overflowY = 'auto';
            submenu.style.scrollbarWidth = 'thin';
        }
    });
}


if (sidebarBurgerButton && sidebar && dashboardNav) {
    sidebarBurgerButton.onclick = function () {
        let isHidden = sidebar.clientWidth == 0;

        if (window.innerWidth <= 768) {
            if (isHidden) {
                sidebar.classList.add('visible');
                dashboardNav.classList.remove('start-0', 'opened');
            }
            else {
                sidebar.classList.remove('visible');
                dashboardNav.classList.add('start-0', 'opened');
            }
        }
        else {
            if (isHidden) {
                sidebar.classList.remove('hide');
                dashboardNav.classList.remove('start-0', 'opened');
            }
            else {
                sidebar.classList.add('hide');
                dashboardNav.classList.add('start-0', 'opened');
            }
        }

    };
}


document.addEventListener("DOMContentLoaded", function () {
    const sideMenuLinks = document.querySelectorAll('#sidebar .side-menu li a');
    const pathname = window.location.pathname;
    const search = window.location.search;

    // decide active route without relying on visible text (i18n-safe)
    let activeRoute = null;
    if (search.includes('is_video_course=true') || search.includes('is_video_course')) {
        activeRoute = 'courses';
    }
    else if (search.includes('type=topic') || pathname.includes('/topic') || pathname.includes('/topics')) {
        activeRoute = 'topics';
    } else if (pathname.includes('/settings') || pathname.includes('/account')) {
        activeRoute = 'settings';
    } else if (pathname.includes('/projects')) {
        activeRoute = 'projects';
    } else if (pathname.includes('/admin')) {
        activeRoute = 'admin';
    }

    sideMenuLinks.forEach(link => {
        const route = link.dataset.route;
        if (route && activeRoute) {
            if (route === activeRoute) link.parentElement.classList.add('active');
            return;
        }

        // fallback: match by href path
        try {
            const linkUrl = new URL(link.getAttribute('href'), window.location.origin);
            if (linkUrl.pathname === pathname || pathname.startsWith(linkUrl.pathname)) {
                link.parentElement.classList.add('active');
            }
        } catch (e) {
            // ignore invalid URLs
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    addScrollbarToSubmenus();
});

document.addEventListener('shown.bs.collapse', function (event) {
    if (event.target && event.target.matches('#sidebar .submenu-collapse')) {
        addScrollbarToSubmenus();
    }
});

window.addEventListener('resize', addScrollbarToSubmenus);
