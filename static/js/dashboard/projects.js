document.addEventListener('DOMContentLoaded', function () {
  const select = document.getElementById('projects-toggle-select');
  if (!select) return;
  select.addEventListener('change', function () {
    const filter = select.value;
    const url = new URL(window.location.href);
    url.searchParams.set('filter', filter);
    fetch(url, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
      .then(response => response.text())
      .then(html => {
        // Parse the returned HTML and update the project section only
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newSection = doc.querySelector('.projects > div');
        const projectsSection = document.querySelector('.projects > div');
        if (newSection && projectsSection) {
          projectsSection.replaceWith(newSection);
        }
      });
  });
});
