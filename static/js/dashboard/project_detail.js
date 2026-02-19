function togglePartsNav() {
  const nav = document.getElementById('parts-navigation')
  const icon = document.getElementById('toggle-parts-nav-icon')
  if (!nav) return
  if (nav.style.display === 'none') {
    nav.style.display = ''
    icon.classList.remove('bi-chevron-right')
    icon.classList.add('bi-chevron-left')
  } else {
    nav.style.display = 'none'
    icon.classList.remove('bi-chevron-left')
    icon.classList.add('bi-chevron-right')
  }
}

function togglePartsList() {
  const list = document.getElementById('parts-list')
  const icon = document.getElementById('toggle-parts-icon')
  if (!list) return
  if (list.style.display === 'none') {
    list.style.display = ''
    icon.classList.remove('bi-chevron-right')
    icon.classList.add('bi-chevron-down')
  } else {
    list.style.display = 'none'
    icon.classList.remove('bi-chevron-down')
    icon.classList.add('bi-chevron-right')
  }
}

// Project Detail Page JS
function toggleStages() {
  const list = document.getElementById('stages-list');
  if (list.style.display === 'none') {
    list.style.display = 'block';
  } else {
    list.style.display = 'none';
  }
}


document.addEventListener('DOMContentLoaded', function () {
  const partsList = document.getElementById('parts-list');
  const saveOrderBtn = document.getElementById('save-order-btn');
  const isAdmin = !!saveOrderBtn;

  // Get project slug from a data attribute on the parts list or another element
  let projectSlug = null;
  if (partsList) {
    projectSlug = partsList.getAttribute('data-project-slug');
    // fallback: try from another element if needed
    if (!projectSlug) {
      const projectElem = document.getElementById('project-details');
      if (projectElem) projectSlug = projectElem.getAttribute('data-project-slug');
    }
  }

  if (partsList && isAdmin && projectSlug) {
    const sortable = new Sortable(partsList, {
      // handle: '.drag-handle',
      animation: 150,
      onEnd: function () {
        saveOrderBtn.style.display = 'inline-block';
      },
    });

    saveOrderBtn.addEventListener('click', function (e) {
      e.preventDefault();
      const order = Array.from(partsList.children).map((li, idx) => ({
        id: li.getAttribute('data-id'),
        order: idx + 1,
      }));
      const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
      fetch(`/api/project/${projectSlug}/reorder_lessons/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
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
  }
});
