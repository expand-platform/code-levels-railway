document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelectorAll('pre').forEach((pre) => {
        pre.classList.add('position-relative', 'p-1', 'overflow-hidden');
        hljs.highlightElement(pre);

        const copyBtn = document.createElement('button');
        copyBtn.className = 'btn copy-btn position-absolute top-0 end-0 p-0 m-1';
        copyBtn.innerHTML = '<i class="bi bi-clipboard text-black "></i>';
        copyBtn.title = 'Copy code';
        pre.appendChild(copyBtn);

        copyBtn.addEventListener('click', () => {
            const code = pre.innerText;
            navigator.clipboard.writeText(code).then(() => {
                copyBtn.innerHTML = '<i class="bi bi-clipboard-check"></i>';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="bi bi-clipboard"></i>';
                }, 2000);
            });
        });
    });
})