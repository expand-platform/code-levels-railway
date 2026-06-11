// Dark Mode Switch
const switchMode = document.getElementById('switch-mode');

window.addEventListener('DOMContentLoaded', () => {
    let theme = localStorage.getItem('theme') || 'light';
    document.documentElement.dataset.theme = theme;
    switchMode.checked = theme === 'dark';
})

switchMode.onchange = () => {
    let themeColor = switchMode.checked ? 'dark' : 'light';

    document.documentElement.dataset.theme = themeColor;
    localStorage.setItem('theme', themeColor);
}