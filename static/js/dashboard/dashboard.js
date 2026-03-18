document.addEventListener("DOMContentLoaded", function () {

    const sideMenuLinks = document.querySelectorAll('#sidebar .side-menu.top li a');
    let activeText = null;

    if (window.location.href.includes("topic")) {
        activeText = "Topics";
    }

    else if (window.location.href.includes("projects")) {
        activeText = "Projects";
    }

    if (activeText) {
        sideMenuLinks.forEach(link => {
            if (link.innerText.trim() === activeText) {
                link.parentElement.classList.add("active");
            }
        });
    }
});
