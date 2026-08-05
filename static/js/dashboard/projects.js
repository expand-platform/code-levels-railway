document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.projects-grid').forEach(function (grid) {
    const languageId = grid.getAttribute('data-language-id');
    const courseId = grid.getAttribute('data-course-id');
    const saveOrderBtn = document.getElementById(
      'save-grid-order-btn-' + (languageId || courseId)
    );
    const reorderEnabled =
      !courseId || grid.getAttribute('data-reorder-enabled') === 'true';
    const canReorder = !!saveOrderBtn && reorderEnabled;

    if (!canReorder) {
      return;
    }

    new Sortable(grid, {
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
      const csrfToken =
        document.querySelector('input[name="csrfmiddlewaretoken"]')?.value ||
        document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

      const order = Array.from(grid.children).map((el, idx) => ({
        id: el.getAttribute('data-id'),
        order: idx + 1,
      }));

      let url = '';
      if (languageId) {
        url = `/api/language/${languageId}/reorder_projects/`;
      } else if (courseId) {
        url = `/api/course/${courseId}/reorder_projects/`;
      }
      if (!url) {
        return;
      }

      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {}),
        },
        body: JSON.stringify({ order }),
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
  });
});
