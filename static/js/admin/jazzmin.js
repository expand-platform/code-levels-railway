document.addEventListener("DOMContentLoaded", function () {
    const jazzyTabs = document.querySelector("#jazzy-tabs")
    if (!jazzyTabs) return

    const tabs = jazzyTabs.querySelectorAll("li a")
    const contentBlocks = document.querySelectorAll("[role='tabpanel']")

    function showTab(index) {
        const tab = tabs[index]
        const panel = contentBlocks[index]
        if (!tab || !panel) return

        tabs.forEach((item) => item.classList.remove("active"))
        tab.classList.add("active")
        contentBlocks.forEach((content) => {
            content.style.display = "none"
        })
        panel.style.display = "block"
        panel.style.opacity = "1"
    }

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", (event) => {
            event.preventDefault()
            showTab(index)
        })
    })

    if (!window.location.hash) return
    const hashIndex = Array.from(tabs).findIndex(
        (tab) => tab.getAttribute("href") === window.location.hash
    )
    if (hashIndex === -1) return
    showTab(hashIndex)
    window.scrollTo({ top: 0, behavior: "smooth" })
});
