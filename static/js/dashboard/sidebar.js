const sidebarBurgerButton = document.querySelector('.dashboard-nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar') || document.querySelector('.sidebar');
const logo = document.querySelector('#sidebar .brand .text');
const dashboardNav = document.querySelector('.dashboard .dashboard-nav');


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


document.addEventListener("DOMContentLoaded", function () {
    const sideMenuLinks = document.querySelectorAll('#sidebar .side-menu li a');
    const pathname = window.location.pathname;
    const search = window.location.search;

    // decide active route without relying on visible text (i18n-safe)
    let activeRoute = null;
    if (search.includes('is_video_course=true') || search.includes('is_video_course')) {
        activeRoute = 'courses';
    }
    else if (search.includes('type=topic') || search.includes('filter=course') || pathname.includes('/topic') || pathname.includes('/topics')) {
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
