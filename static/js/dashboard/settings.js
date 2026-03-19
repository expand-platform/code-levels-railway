document.addEventListener("DOMContentLoaded", function () {
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

    const popoverWrapper = document.querySelector('.popover-wrapper');
    const tokenInput = document.getElementById("telegram_token");
    const copyBtn = document.getElementById("copy-telegram-token-btn");


    if (tokenInput) {
        // Ensure popover is initialized on the input
        const popover = bootstrap.Popover.getOrCreateInstance(popoverWrapper);
        function copyToken() {
            navigator.clipboard.writeText(tokenInput.value);
            popover.show();
            setTimeout(() => {
                popover.hide();
            }, 2000);
        }
        tokenInput.addEventListener("click", copyToken);
        if (copyBtn) {
            copyBtn.addEventListener("click", copyToken);
        }
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const usernameInput = document.getElementById("username");

    if (!form || !usernameInput) return;

    form.addEventListener("submit", function (e) {
        const username = usernameInput.value.trim();
        let error = "";
        console.log("Validating username:", username);

        if (!username) {
            error = "Username cannot be empty.";
        } else if (username.length < 3 || username.length > 30) {
            error = "Username must be 3-30 characters long.";
        } else if (!/^[a-zA-Z0-9_]+$/.test(username)) {
            error = "Username must contain only letters, numbers, and underscores.";
        } else if (/^\d+$/.test(username)) {
            error = "Username cannot be numbers only.";
        } else if (/__/.test(username)) {
            error = "Username cannot contain consecutive underscores.";
        } else if (username.startsWith("_") || username.endsWith("_")) {
            error = "Username cannot start or end with an underscore.";
        } else if (/&[a-zA-Z0-9#]+;/.test(username)) {
            error = "Username cannot contain HTML entities.";
        } else if (/\\u[0-9A-Fa-f]{4}|\\x[0-9A-Fa-f]{2}/.test(username)) {
            error = "Username cannot contain unicode escape sequences.";
        }

        if (error) {
            e.preventDefault();
            showSettingsError(error);
            usernameInput.focus();
        }
    });
});

function showSettingsError(message) {
    let container = document.querySelector(".settings-messages");
    if (!container) {
        container = document.createElement("div");
        container.className = "settings-messages";
        const section = document.querySelector(".settings-section-card");
        if (section) section.insertBefore(container, section.firstChild);
    }
    const alert = document.createElement("div");
    alert.className = "alert alert-danger alert-dismissible fade show";
    alert.setAttribute("role", "alert");
    alert.innerHTML = `${message} <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>`;
    container.appendChild(alert);
}
