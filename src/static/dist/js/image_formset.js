const FormsetManager = {
    getPrefix: () => {
        const totalFormsInput = document.querySelector('input[id$="-TOTAL_FORMS"]');
        return totalFormsInput ? totalFormsInput.id.replace('id_', '').replace('-TOTAL_FORMS', '') : 'form';
    },

    reindexAll: function() {
        const prefix = this.getPrefix();
        const allForms = document.querySelectorAll('.gallery-form:not(#empty-formset)');
        const totalForms = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
        
        allForms.forEach((form, index) => {
            const regex = new RegExp(`${prefix}-(\\d+|__prefix__)-`, 'g');
            const replacement = `${prefix}-${index}-`;


            form.querySelectorAll('input, select, textarea, label, img').forEach(el => {
                ['name', 'id', 'for', 'src'].forEach(attr => {
                    const val = el.getAttribute(attr);
                    if (val) el.setAttribute(attr, val.replace(regex, replacement));
                });
            });
        });

        if (totalForms) totalForms.value = allForms.length;
    }
};



const addButton = document.getElementById('add-form');

if (addButton) {
    addButton.addEventListener('click', (e) => {
        e.preventDefault();

        const container = document.getElementById('forms-container-gallery');
        const emptyTemplate = document.getElementById('empty-formset');

        if (container && emptyTemplate) {
            const newForm = emptyTemplate.cloneNode(true);
            newForm.classList.add('gallery-form');
            newForm.removeAttribute('id');
            newForm.style.display = 'block';

            container.appendChild(newForm);
            FormsetManager.reindexAll();
        }
    });
}


document.addEventListener('click', (e) => {
    const deleteBtn = e.target.closest('.delete-form-button');
    if (deleteBtn) {
        e.preventDefault();
        const formRow = deleteBtn.closest('.gallery-form');
        const idField = formRow.querySelector('input[name$="-id"]');

        if (idField && idField.value) {


            const deleteCheckbox = formRow.querySelector('input[type="checkbox"][name$="-DELETE"]');
            if (deleteCheckbox) deleteCheckbox.checked = true;
            formRow.style.display = 'none';
        } else {

            formRow.remove();
            FormsetManager.reindexAll();
        }
    }
});

function initPreview() {
    document.addEventListener('change', function(e) {
        if (e.target.type === 'file' && e.target.name.includes('image')) {
            const file = e.target.files[0];
            const container = e.target.closest('.gallery-form') || e.target.closest('.custom-upload');

            if (file && container) {
                let img = container.querySelector('.preview-img');

                if (!img) {
                    img = document.createElement('img');
                    img.classList.add('preview-img');
                    container.appendChild(img);
                }

                img.src = URL.createObjectURL(file);
                img.style.display = 'block';

            }
        }
    });
}



initPreview();


function showFields(lang){
    const sectionUk = document.getElementById('section-ua')
    const sectionRu = document.getElementById('section-ru')

    const BtnUk = document.getElementById('btn-uk')
    const BtnRu = document.getElementById('btn-ru')

    if (lang == 'uk_ua') {
        sectionUk.style.display = 'block'
        sectionRu.style.display = 'none'

        btnUk.className = 'btn btn-primary'
        btnRU.className = 'btn btn-outline-primary'

    } else {

        sectionUk.style.display = 'none'
        sectionRu.style.display = 'block'

        btnUk.className = 'btn btn-outline-primary'
        btnRU.className = 'btn btn-primary'

    }
}