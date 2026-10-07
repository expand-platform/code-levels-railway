const root = document.querySelector(".user-dash");
const toggle = document.querySelector("[data-user-dash-toggle]");
const backdrop = document.querySelector("[data-user-dash-backdrop]");

function setSidebarOpen(open) {
    if (!root || !toggle) {
        return;
    }
    root.classList.toggle("is-sidebar-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (backdrop) {
        backdrop.hidden = !open;
    }
}

if (toggle) {
    toggle.addEventListener("click", () => {
        setSidebarOpen(!root.classList.contains("is-sidebar-open"));
    });
}

if (backdrop) {
    backdrop.addEventListener("click", () => setSidebarOpen(false));
}

root?.querySelectorAll(".user-dash__sidebar a").forEach((link) => {
    link.addEventListener("click", () => setSidebarOpen(false));
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        setSidebarOpen(false);
    }
});

window.addEventListener("resize", () => {
    if (window.innerWidth > 768) {
        setSidebarOpen(false);
    }
});
