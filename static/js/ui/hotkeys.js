import { openSearch } from '../helpers/projectSearch.js'

export class HotkeysManager {
    // list with hotkeys
    static OPEN_ADMIN_PANEL = "alt+a"
    static OPEN_SEARCH_BAR = "ctrl+i"

    setupKeys() {
        this.setupSearchBar()
        this.setupAdminPanelOpen()
    }

    setupSearchBar() {
        document.addEventListener('keydown', (event) => {
            if (event.repeat || event.shiftKey || event.altKey) return
            if (!(event.ctrlKey || event.metaKey) || event.key.toLowerCase() !== 'i') return
            event.preventDefault()
            openSearch()
        })
    }

    setupAdminPanelOpen() {
        document.addEventListener('keydown', (event) => {
            if (event.repeat || event.ctrlKey || event.metaKey || event.shiftKey) return
            if (!event.altKey || event.key.toLowerCase() !== 'a') return
            event.preventDefault()
            this.openAdminPanel()
        })
    }

    openAdminPanel() {
        window.location.href = '/cp/'
    }
}
