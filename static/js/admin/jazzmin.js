document.addEventListener("DOMContentLoaded", function () {
    let jazzyTabs = document.querySelector("#jazzy-tabs")

    if (jazzyTabs) {
        let tabs = jazzyTabs.querySelectorAll("li a")
        let contentBlocks = document.querySelectorAll("[role='tabpanel']")
        tabs.forEach((tab, index) => {

            tab.addEventListener("click", (e) => {
                e.preventDefault();
                tabs.forEach((tab) => {
                    tab.classList.remove("active")
                })
                tab.classList.add("active")

                contentBlocks.forEach((content) => {
                    content.style.display = "none"
                })
                contentBlocks[index].style.display = "block"
                contentBlocks[index].style.opacity = "1"
                console.log('- contentBlocks -', contentBlocks[index]);
            })
        })
    }
});
