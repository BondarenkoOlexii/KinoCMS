const AddMoreButton = document.getElementById("add-form")
const totalNewForms = document.getElementById("id_image-TOTAL_FORMS")

AddMoreButton.addEventListener('click', add_new_formset)

function add_new_formset(event) {

    const currentFormCount = document.querySelectorAll('.gallery-form').length

    const container = document.getElementById('forms-container-gallery')
    const emptyFormElement = document.getElementById('empty-formset')


    const copyEmptyForm = emptyFormElement.cloneNode(true)


    copyEmptyForm.setAttribute('class', 'gallery-form')
    copyEmptyForm.removeAttribute('id')
    copyEmptyForm.style.display = 'block'

    const regex = new RegExp('__prefix__', 'g')
    copyEmptyForm.innerHTML = copyEmptyForm.innerHTML.replace(regex, currentFormCount)

    const typeInput = copyEmptyForm.querySelector('input[name$="-image_type"]')
    if (typeInput) {
        typeInput.value = 'gallery'
    }

    totalNewForms.value = currentFormCount + 1

    container.append(copyEmptyForm)
}


// ---------------------------------------------------------------------------------------------------------------------

const formsContainers = document.querySelectorAll('#forms-container-gallery, #forms-container-logo')

formsContainers.forEach(container => {
    container.addEventListener('change', (event) => {
        const input = event.target;
        if (input.type === 'file'){
            const input = event.target
            const[file] = input.files;

            if (file){
                const label = input.closest('.custom-upload')
                const preview = label.querySelector('.preview-img')

                preview.src = URL.createObjectURL(file)
                preview.style.display = 'block'
            }
        }

    })

})

//------------------------------------------------------------------------------------------------------------------------------------

function deleteExistForm(button){
    const formRow = button.closest('.gallery-form');
    const deleteCheckbox = formRow.querySelector('input[type="checkbox"][name$="-DELETE"]');

    if (deleteCheckbox) {
        deleteCheckbox.checked = true;
        formRow.style.display = 'none';
    }
}

function deleteEmptyForm(button) {
    const formRow = button.closest('.gallery-form');
    const totalFormsInput = document.querySelector('#id_image-TOTAL_FORMS');

    if (formRow) {
        formRow.remove();

        const currentForms = document.querySelectorAll('#forms-container-gallery .gallery-form');
        totalFormsInput.value = currentForms.length;

        updateFormIndices();
    }
}


const formsContainer2 = document.querySelector("#forms-container-gallery");

if (formsContainer2) {
    formsContainer2.addEventListener('click', function(e) {

        const deleteBtn = e.target.closest('.delete-form-button');

        if (deleteBtn) {
            e.preventDefault();
            const formRow = deleteBtn.closest('.gallery-form');
            const idField = formRow.querySelector('input[name$="-id"]');

            if (idField && idField.value) {
                const deleteCheckbox = formRow.querySelector('input[type="checkbox"][name$="-DELETE"]');
                if (deleteCheckbox) {
                    deleteCheckbox.checked = true;
                    formRow.style.display = 'none';
                }
            } else {
                deleteEmptyForm(deleteBtn);
            }
        }
    });
}


function updateFormIndices() {
    const rows = document.querySelectorAll('#forms-container-gallery .gallery-form');
    rows.forEach((row, index) => {
        const regex = /image-\d+-/g;
        const replacement = `image-${index}-`;
        row.innerHTML = row.innerHTML.replace(regex, replacement);
    });
}
