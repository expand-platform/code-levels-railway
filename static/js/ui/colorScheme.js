import { loadFromLocalStorage, saveToLocalStorage } from './../helpers/localStorage.js';

const COLOR_SCHEME_KEY = 'isDarkModeEnabled';

export function loadColorScheme() {
    let body = document.body;
    let isDarkModeEnabled = loadFromLocalStorage(COLOR_SCHEME_KEY);

    if (isDarkModeEnabled === true) {
        body.classList.add('dark');
        saveToLocalStorage(COLOR_SCHEME_KEY, true);
        console.log('dark mode set!');
    } else {
        body.classList.remove('dark');
        saveToLocalStorage(COLOR_SCHEME_KEY, false);
        console.log('light mode set!');
    }
}

export function saveColorScheme(isDarkModeEnabled) {
    let body = document.body;

    if (isDarkModeEnabled) {
        body.classList.add('dark');
        saveToLocalStorage(COLOR_SCHEME_KEY, true);
    }
    else {
        body.classList.remove('dark');
        saveToLocalStorage(COLOR_SCHEME_KEY, false);
    }
}

