// Dark Mode Switch
const switchMode = document.getElementById('switch-mode');

window.addEventListener('DOMContentLoaded', () => {
    let theme = localStorage.getItem('theme') || 'light';
    document.documentElement.dataset.theme = theme;
    switchMode.checked = theme === 'dark';
})

window.onkeydown = (event) => enableKeyboardShortcut(event);

function enableKeyboardShortcut(event) {
    if (event.which === 81 && (event.ctrlKey && event.shiftKey)) {
        switchMode.checked = !switchMode.checked;
        switchTheme();
    }
}

function switchTheme() {
    let themeColor = switchMode.checked ? 'dark' : 'light';

    document.documentElement.dataset.theme = themeColor;
    localStorage.setItem('theme', themeColor);
}

switchMode.onchange = switchTheme;