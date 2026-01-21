export function saveToLocalStorage(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}


export function loadFromLocalStorage(key) {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : null;
}