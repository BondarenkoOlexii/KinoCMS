const AddMoreButton = document.getElementById("add-form")
const totalNewForms = document.getElementById("id_image-TOTAL_FORMS")

AddMoreButton.addEventListener('click', add_new_formset)

function add_new_formset(event){
    console.log(event)
    if (event){
        event.preventDefault()
    }
    const currentFormCount = document.querySelectorAll('.gallery-form').length
    const container = document.getElementById('forms-container')
    const formCopyTarget = document.getElementById('forms-container')
    const copyEmptyForm = document.getElementById('empty-formset').cloneNode(true)

    copyEmptyForm.setAttribute('class', 'gallery-form')
    copyEmptyForm.setAttribute('id', `form-${currentFormCount}`)
    const regex = new RegExp('__prefix__', 'g')

    copyEmptyForm.style.display = 'block'

    copyEmptyForm.innerHTML = copyEmptyForm.innerHTML.replace(regex, currentFormCount)
    totalNewForms.setAttribute('value', currentFormCount + 1)

    formCopyTarget.append(copyEmptyForm)
}


// ---------------------------------------------------------------------------------------------------------------------

const formsContainer = document.getElementById('forms-container')

formsContainer.addEventListener('change', (event) => {
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