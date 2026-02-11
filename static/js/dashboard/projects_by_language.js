// Projects by Language Grid Sorting

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.projects-grid').forEach(function (grid) {
    const languageId = grid.getAttribute('data-language-id');
    const saveOrderBtn = document.getElementById('save-grid-order-btn-' + languageId);
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
        fetch(`/api/language/${languageId}/reorder_projects/`, {
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
