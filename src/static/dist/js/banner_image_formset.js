const FormsetManager = {
    reindexAll: function(element) {
        // Знаходимо спільний батьківський блок для всього формсету
        const section = element.closest('.formset-section');
        const managementForm = section.querySelector('input[id$="-TOTAL_FORMS"]');
        if (!managementForm) return;

        const prefix = managementForm.id.replace('id_', '').replace('-TOTAL_FORMS', '');

        // Знаходимо абсолютно ВСІ форми в цій секції (і Лого, і Галерею)
        const allForms = section.querySelectorAll('.gallery-form:not(.template)');

        allForms.forEach((form, index) => {
            const regex = new RegExp(`${prefix}-(\\d+|__prefix__)-`, 'g');
            const replacement = `${prefix}-${index}-`;

            form.querySelectorAll('input, select, textarea, label, img').forEach(el => {
                ['name', 'id', 'for', 'src'].forEach(attr => {
                    const val = el.getAttribute(attr);
                    if (val) { el.setAttribute(attr, val.replace(regex, replacement)); }
                });
            });
        });

        // Оновлюємо TOTAL_FORMS загальною кількістю
        managementForm.value = allForms.length;
    }
};

document.addEventListener('click', (e) => {
    // ДОДАВАННЯ
    const addBtn = e.target.closest('.add-form-btn');
    if (addBtn) {
        e.preventDefault();
        const container = document.getElementById(addBtn.dataset.container);
        const template = document.getElementById(addBtn.dataset.template);

        if (container && template) {
            const newForm = template.firstElementChild.cloneNode(true);
            newForm.classList.remove('template');
            newForm.style.display = 'block';

            container.appendChild(newForm);
            // Перераховуємо все в межах секції
            FormsetManager.reindexAll(container);
        }
    }

    // ВИДАЛЕННЯ
    const deleteBtn = e.target.closest('.delete-form-button');
    if (deleteBtn) {
        e.preventDefault();
        const formRow = deleteBtn.closest('.gallery-form');
        const idField = formRow.querySelector('input[name$="-id"]');

        if (idField && idField.value) {
            // Для існуючих в БД: ставимо галочку DELETE і ховаємо
            const deleteCheckbox = formRow.querySelector('input[type="checkbox"][name$="-DELETE"]');
            if (deleteCheckbox) deleteCheckbox.checked = true;
            formRow.style.display = 'none';
        } else {
            // Для нових: просто видаляємо
            formRow.remove();
        }
        // Перераховуємо після видалення
        FormsetManager.reindexAll(deleteBtn.closest('.formset-section'));
    }
});

// Обробка прев'ю
document.addEventListener('change', (e) => {
    if (e.target.type === 'file' && e.target.name.includes('image')) {
        const file = e.target.files[0];
        const container = e.target.closest('.gallery-form');
        if (file && container) {
            let img = container.querySelector('.preview-img');
            if (img) {
                img.src = URL.createObjectURL(file);
                img.style.display = 'block';
                const placeholder = container.querySelector('.upload-placeholder');
                if (placeholder) placeholder.style.display = 'none';
            }
        }
    }
});