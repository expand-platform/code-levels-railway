let showCodeButton = document.querySelector(".show-code-switch");
let coverLine = document.querySelector(".no-code-cover-line");
let checkbox = document.querySelector(".show-code-switch input");

// settings
const CodepenHeight = 70;


function setCoverLineWidth() {
    let codepen_width = document.querySelector(".cp_embed_wrapper").clientWidth - 7;
    coverLine.style.width = `${codepen_width}px`;
}

function moveSettings() {
    let settings = document.querySelector(".settings");
    let codepen_height = document.querySelector(".cp_embed_wrapper").clientHeight - 100;

    // settings.style.top = `${codepen_height}px`;
}

function moveCoverLine() {
    let codepen_wrapper = document.querySelector(".cp_embed_wrapper");
    let wrapperRect = codepen_wrapper.getBoundingClientRect();
    let parentRect = codepen_wrapper.offsetParent ? codepen_wrapper.offsetParent.getBoundingClientRect() : { left: 0, top: 0 };
    let leftOffset = wrapperRect.left - parentRect.left;
    let topOffset = wrapperRect.top - parentRect.top;
    coverLine.style.left = `${leftOffset + 5}px`;
    coverLine.style.top = `${topOffset+1}px`;

}

function toggleCodeButtons() {
    let checkboxValue = checkbox.checked;
    console.log('- showCode -', checkboxValue);
    
    if (checkboxValue) {
        coverLine.classList.add("visually-hidden")
    }
    else {
        coverLine.classList.remove("visually-hidden")
    }
}

showCodeButton.onclick = function () {
    toggleCodeButtons();
}


/* set dynamic height for editor */
window.onload = function () {
    toggleCodeButtons();
    setCoverLineWidth();
    moveCoverLine();

    let codepen_wrapper = document.querySelector(".cp_embed_wrapper");


    if (codepen_wrapper) {
        codepen_wrapper.style.height = `${CodepenHeight}vh`;
    }
}

window.onresize = function () {
    setCoverLineWidth();
    moveCoverLine();
}

