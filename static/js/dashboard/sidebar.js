const sidebarBurgerButton = document.querySelector('.dashboard-nav .bi.bi-list');
const sidebar = document.getElementById('sidebar') || document.querySelector('.sidebar');
const dashboardNav = document.querySelector('.dashboard .dashboard-nav');

const PATH_ROUTES = [
    ['/account/login', 'login'],
    ['/account/signup', 'login'],
    ['/settings', 'settings'],
    ['/account', 'settings'],
    ['/dashboard', 'dashboard'],
    ['/courses', 'courses'],
    ['/games', 'games'],
    ['/roadmaps', 'roadmaps'],
    ['/projects', 'projects'],
    ['/job-tracks', 'job-tracks'],
    ['/admin', 'admin'],
];

function activeSidebarRoute() {
    const pathname = window.location.pathname;
    const params = new URLSearchParams(window.location.search);

    if (params.get('is_video_course') === 'true') return 'courses';
    if (params.get('type') === 'topic' || pathname.includes('/topic')) return 'topics';
    const match = PATH_ROUTES.find(([path]) => pathname.includes(path));
    return match ? match[1] : null;
}

function linkPath(link) {
    const href = link.getAttribute('href');
    if (!href) return '';
    try {
        return new URL(href, window.location.origin).pathname;
    } catch (e) {
        return '';
    }
}

function setSubmenuOpen(panel, toggle, open) {
    const Collapse = window.bootstrap?.Collapse;
    if (Collapse) {
        Collapse.getOrCreateInstance(panel, { toggle: false })[open ? 'show' : 'hide']();
    } else {
        panel.classList.toggle('show', open);
    }
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    const label = open ? sidebar?.dataset.submenuClose : sidebar?.dataset.submenuOpen;
    if (label) toggle.setAttribute('aria-label', label);
}

function bindSubmenuToggles() {
    const openLabel = sidebar?.dataset.submenuOpen || 'Open submenu';

    document.querySelectorAll('#sidebar .has-submenu').forEach((item) => {
        const panel = item.querySelector('.submenu-collapse');
        const row = item.querySelector('.menu-row');
        if (!panel || !row || row.querySelector('.submenu-toggle')) return;

        const toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.className = 'submenu-toggle';
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', openLabel);
        if (panel.id) toggle.setAttribute('aria-controls', panel.id);

        const icon = document.createElement('i');
        icon.className = 'bi bi-chevron-down';
        icon.setAttribute('aria-hidden', 'true');
        toggle.appendChild(icon);

        toggle.addEventListener('click', () => {
            setSubmenuOpen(panel, toggle, toggle.getAttribute('aria-expanded') !== 'true');
        });
        row.appendChild(toggle);
    });
}

function markActiveLinks(activeRoute, pathname) {
    document.querySelectorAll('#sidebar .side-menu li a').forEach((link) => {
        const route = link.dataset.route;
        const path = linkPath(link);
        const inSubmenu = Boolean(link.closest('.submenu'));

        if (!inSubmenu && route && activeRoute) {
            if (route === activeRoute) {
                const row = link.closest('.menu-row') || link.parentElement;
                row.classList.add('active');
            }
            return;
        }

        const matches = path === pathname || (
            !inSubmenu && path && path !== '/' && pathname.startsWith(path)
        );
        if (matches) link.parentElement.classList.add('active');
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
    const pathname = window.location.pathname;
    const activeRoute = activeSidebarRoute();

    bindSubmenuToggles();
    markActiveLinks(activeRoute, pathname);
});
