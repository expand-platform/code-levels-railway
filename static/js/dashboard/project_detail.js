function togglePartsList() {
  const views = document.getElementById('parts-views')
  const icon = document.getElementById('toggle-parts-icon')
  if (!views) return
  if (views.style.display === 'none') {
    views.style.display = ''
    if (icon) {
      icon.classList.remove('bi-chevron-right')
      icon.classList.add('bi-chevron-down')
    }
  } else {
    views.style.display = 'none'
    if (icon) {
      icon.classList.remove('bi-chevron-down')
      icon.classList.add('bi-chevron-right')
    }
  }
}

function setLessonsView(view) {
  const roadmap = document.getElementById('lessons-roadmap')
  const listForm = document.getElementById('reorder-form')
  const showList = view === 'list'
  if (roadmap) {
    roadmap.hidden = showList
  }
  if (listForm) listForm.hidden = !showList
}

function toggleDescriptionSection() {
  const content = document.getElementById('description-content')
  const icon = document.getElementById('toggle-description-icon')
  if (!content) return
  if (content.style.display === 'none') {
    content.style.display = ''
    if (icon) {
      icon.classList.remove('bi-chevron-right')
      icon.classList.add('bi-chevron-down')
    }
  } else {
    content.style.display = 'none'
    if (icon) {
      icon.classList.remove('bi-chevron-down')
      icon.classList.add('bi-chevron-right')
    }
  }
}

// Delegate click handling so toggle works even if the button is re-rendered later.
document.addEventListener('click', function (event) {
  const toggleBtn = event.target.closest('#toggle-parts-btn');
  if (!toggleBtn) return;
  event.preventDefault();
  togglePartsList();
});

document.addEventListener('click', function (event) {
  const toggleBtn = event.target.closest('#toggle-description-btn')
  if (!toggleBtn) return
  event.preventDefault()
  toggleDescriptionSection()
});

document.querySelectorAll('input[name="lessons-view"]').forEach(function (toggle) {
  toggle.addEventListener('change', function () {
    if (toggle.checked) setLessonsView(toggle.value)
  })
})


document.addEventListener('DOMContentLoaded', function () {
  const partsList = document.getElementById('parts-list');
  const saveOrderBtn = document.getElementById('save-order-btn');
  const isAdmin = !!saveOrderBtn;

  const projectSlug = partsList ? partsList.getAttribute('data-project-slug') : null;

  if (partsList && isAdmin && projectSlug) {
    new Sortable(partsList, {
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
