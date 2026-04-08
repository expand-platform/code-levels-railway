document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('.objectives input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        const label = document.querySelector(`label[for="${checkbox.id}"]`);
        if (!label) return;

        // Set initial state
        if (checkbox.checked) {
            label.classList.add('text-decoration-line-through', 'text-muted');
        }

        // Listen to changes
        checkbox.addEventListener('change', function () {
            if (this.checked) {
                label.classList.add('text-decoration-line-through', 'text-muted');
            } else {
                label.classList.remove('text-decoration-line-through', 'text-muted');
            }
        });
    });
});