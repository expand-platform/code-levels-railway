document.addEventListener('DOMContentLoaded', function () {
  const select = document.getElementById('projects-toggle-select');
  if (select) {
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
  }

  // Drag-and-drop sorting for both language and course grids
  document.querySelectorAll('.projects-grid').forEach(function (grid) {
    const languageId = grid.getAttribute('data-language-id');
    const courseId = grid.getAttribute('data-course-id');
    const saveOrderBtn = document.getElementById('save-grid-order-btn-' + (languageId || courseId));
    const isAdmin = !!saveOrderBtn;

    if (grid && isAdmin) {
      const sortable = new Sortable(grid, {
        animation: 150,
        ghostClass: 'sortable-ghost',
        dragClass: 'sortable-drag',
        chosenClass: 'sortable-chosen',
        onEnd: function () {
          saveOrderBtn.style.display = 'inline-block';
        },
      });

      saveOrderBtn.addEventListener('click', function (e) {
        e.preventDefault();
        const order = Array.from(grid.children).map((el, idx) => ({
          id: el.getAttribute('data-id'),
          order: idx + 1,
        }));
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
        let url = '';
        if (languageId) {
          url = `/api/language/${languageId}/reorder_projects/`;
        } else if (courseId) {
          url = `/api/course/${courseId}/reorder_projects/`;
        }
        if (!url) return;
        fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {}),
          },
          body: JSON.stringify({order}),
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.success) {
              saveOrderBtn.style.display = 'none';
              location.reload();
            } else {
              alert('Failed to save order.');
            }
          })
          .catch(() => alert('Error saving order.'));
      });
    }
  });
});
