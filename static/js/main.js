import { HotkeysManager } from './ui/hotkeys.js'

class App {
    constructor() {
        this.hotkeysManager = new HotkeysManager()
    }

    start() {
        // set up hotkeys
        this.hotkeysManager.setupKeys()
    }
}


new App().start()