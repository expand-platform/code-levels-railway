const CodepenHeight = 500;
const CodepenActiveTabs = "result";

document.addEventListener('DOMContentLoaded', function () {
    const content = document.querySelector('.lesson-details .content');
    let codepenParagraph = null;

    if (content) {
        const paragraphs = content.querySelectorAll('p');
        paragraphs.forEach(p => {
            if (p.textContent.includes('[[codepen]]') || p.textContent.includes('[[ codepen ]]')) {
                codepenParagraph = p;
            }
        });
    }

    if (codepenParagraph && window.lessonCodepenUrl) {
        console.log('codepen working');
        let urlHash = "";
        let title = "";
        let author = "";
        const codepenURLData = window.lessonCodepenUrl.match(/codepen\.io\/(.+)\/pen\/(.+)/);
        console.log("🚀 ~ match:", codepenURLData)
        if (codepenURLData) {
            author = codepenURLData[1];
            urlHash = codepenURLData[2];
            const wrapper = insertCodepen(urlHash, title, author);
            codepenParagraph.replaceWith(wrapper);

            insertCodepenScript();
        }
    }
});

function insertCodepenScript() {
    const script = document.createElement('script');
    script.id = 'codepen-embed-script';
    script.src = 'https://public.codepenassets.com/embed/index.js';
    script.async = true;
    document.body.appendChild(script);
}


function insertCodepen(urlHash, title, author) {
    const codepenWrapper = document.createElement("div");
    // codepenWrapper.className = "cp_embed_wrapper";
    codepenWrapper.innerHTML =
        `<p class="codepen" data-height="${CodepenHeight}" data-default-tab="${CodepenActiveTabs}" data-slug-hash="${urlHash}" data-pen-title="${title}" data-user="${author}" style="height: ${CodepenHeight}px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; border: 2px solid; margin: 1em 0; padding: 1em;">
        <span>See the Pen <a href="https://codepen.io/${author}/pen/${urlHash}">
        ${title}</a> by ${author} (<a href="https://codepen.io/${author}">@${author}</a>)
        on <a href="https://codepen.io">CodePen</a>.</span>
        </p>`;
    return codepenWrapper;
}































// let showCodeButton = document.querySelector(".show-code-switch");
// let coverLine = document.querySelector(".no-code-cover-line");
// let checkbox = document.querySelector(".show-code-switch input");

// // settings
// const CodepenHeight = 70;


// function setCoverLineWidth() {
//     let codepen_width = document.querySelector(".cp_embed_wrapper").clientWidth - 7;
//     coverLine.style.width = `${codepen_width}px`;
// }

// function moveSettings() {
//     let settings = document.querySelector(".settings");
//     let codepen_height = document.querySelector(".cp_embed_wrapper").clientHeight - 100;

//     // settings.style.top = `${codepen_height}px`;
// }

// function moveCoverLine() {
//     let codepen_wrapper = document.querySelector(".cp_embed_wrapper");
//     let wrapperRect = codepen_wrapper.getBoundingClientRect();
//     let parentRect = codepen_wrapper.offsetParent ? codepen_wrapper.offsetParent.getBoundingClientRect() : { left: 0, top: 0 };
//     let leftOffset = wrapperRect.left - parentRect.left;
//     let topOffset = wrapperRect.top - parentRect.top;
//     coverLine.style.left = `${leftOffset + 5}px`;
//     coverLine.style.top = `${topOffset+1}px`;

// }

// function toggleCodeButtons() {
//     let checkboxValue = checkbox.checked;
//     console.log('- showCode -', checkboxValue);
    
//     if (checkboxValue) {
//         coverLine.classList.add("visually-hidden")
//     }
//     else {
//         coverLine.classList.remove("visually-hidden")
//     }
// }

// showCodeButton.onclick = function () {
//     toggleCodeButtons();
// }


// /* set dynamic height for editor */
// window.onload = function () {
//     toggleCodeButtons();
//     setCoverLineWidth();
//     moveCoverLine();

//     let codepen_wrapper = document.querySelector(".cp_embed_wrapper");


//     if (codepen_wrapper) {
//         codepen_wrapper.style.height = `${CodepenHeight}vh`;
//     }
// }

// window.onresize = function () {
//     setCoverLineWidth();
//     moveCoverLine();
// }

