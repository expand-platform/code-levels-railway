const REORDER_URL = {
  skill: (id) => `/api/skill/${id}/reorder_projects/`,
  language: (id) => `/api/language/${id}/reorder_projects/`,
  course: (id) => `/api/course/${id}/reorder_projects/`,
}

function getGridScope(grid) {
  const skillId = grid.getAttribute('data-skill-id')
  if (skillId) {
    return { type: 'skill', id: skillId }
  }
  const languageId = grid.getAttribute('data-language-id')
  if (languageId) {
    return { type: 'language', id: languageId }
  }
  const courseId = grid.getAttribute('data-course-id')
  if (courseId) {
    return { type: 'course', id: courseId }
  }
  return null
}

function getReorderUrl(scope) {
  return scope ? REORDER_URL[scope.type](scope.id) : ''
}

function isReorderEnabled(grid, scope) {
  if (!scope) return false
  if (scope.type === 'language') return true
  return grid.getAttribute('data-reorder-enabled') === 'true'
}

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.projects-grid').forEach(function (grid) {
    const scope = getGridScope(grid);
    const saveOrderBtn = document.getElementById(
      'save-grid-order-btn-' + (scope && scope.id)
    );
    const canReorder = !!saveOrderBtn && isReorderEnabled(grid, scope);

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

      const url = getReorderUrl(scope);
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
