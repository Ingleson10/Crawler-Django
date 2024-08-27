window.addEventListener('load', function() {
    fixFooterPosition();
});

function fixFooterPosition() {
    const footer = document.querySelector('footer');
    const content = document.querySelector('body');

    if (content.offsetHeight < window.innerHeight) {
        footer.style.position = 'absolute';
        footer.style.bottom = 0;
        footer.style.width = '100%';
    } else {
        footer.style.position = 'static';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log("Página de contato carregada com sucesso");

    // Função para adicionar o listener ao botão de edição
    function addEditButtonListener() {
        const editButton = document.getElementById('edit-button');
        if (editButton) {
            editButton.addEventListener('click', function() {
                const projectId = document.getElementById('project-form').getAttribute('data-project-id');
                if (projectId) {
                    window.location.href = `/projects/project/${projectId}/edit/`;
                } else {
                    alert("Project ID is missing.");
                }
            });
        }
    }

    // Adiciona o listener ao botão de edição ao carregar o DOM
    // addEditButtonListener();

    // Adiciona o listener aos links dos projetos
    document.querySelectorAll('.project-link').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            var projectId = this.getAttribute('data-id');
            fetch(`/projects/project/${projectId}/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                document.getElementById('project-detail-content').innerHTML = html;
                history.pushState(null, '', `/projects/project/${projectId}/`);
                // Reatribui o listener ao botão de edição após atualizar o conteúdo
                addEditButtonListener();
                fixFooterPosition();
    
                // Remove o botão "Voltar aos Projetos" se carregado via AJAX
                var backButton = document.querySelector('.back-to-list-btn');
                if (backButton) {
                    backButton.style.display = 'none';
                }
            })
            .catch(error => console.error('Error:', error));
            fixFooterPosition();
        });
    });
    
    // const addUrlButton = document.getElementById('add-url');
    // const urlFormsDiv = document.getElementById('url-forms');

    // Função para obter o token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Verifica se o cookie começa com o nome que queremos
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // if (addUrlButton) {
    //     addUrlButton.addEventListener('click', function() {
    //         const formIndex = new Date().getTime();
    //         const newFormHtml = `
    //             <div class="form-group url-group" id="url-form-${formIndex}">
    //                 <p>
    //                     <label for="url-${formIndex}-url">URL:</label>
    //                     <input type="text" name="url" class="form-control" required id="url-${formIndex}-url">
    //                 </p>
    //                 <p>
    //                     <label for="url-${formIndex}-status">Status:</label>
    //                     <select name="url-${formIndex}-status" class="form-control" required id="url-${formIndex}-status">
    //                         <option value="" selected>---------</option>
    //                         <option value="valid">Válida</option>
    //                         <option value="invalid">Inválida</option>
    //                     </select>
    //                 </p>
    //                 <p>
    //                     <label for="url-${formIndex}-selector">Seletor:</label>
    //                     <input type="text" name="url-${formIndex}-selector" class="form-control" required id="url-${formIndex}-selector">
    //                 </p>
    //                 <p>
    //                     <label for="url-${formIndex}-type">Tipo:</label>
    //                     <select name="url-${formIndex}-type" class="form-control" required id="url-${formIndex}-type">
    //                         <option value="" selected>---------</option>
    //                         <option value="CSS">CSS</option>
    //                         <option value="XPath">XPath</option>
    //                     </select>
    //                 </p>
    //                 <button type="button" class="btn btn-danger btn-sm remove-url-form" data-id="new">
    //                     <i class="fas fa-trash-alt"></i>
    //                 </button>
    //             </div>
    //         `;
    //         urlFormsDiv.insertAdjacentHTML('beforeend', newFormHtml);

    //         document.querySelector(`#url-form-${formIndex} .remove-url-form`).addEventListener('click', function() {
    //             if (confirm('Tem certeza que deseja deletar esta URL?')) {
    //                 this.closest('.url-group').remove();
    //             }
    //         });
    //     });
    // }

    const addUrlButton = document.getElementById('add-url');
    const addScheduleButton = document.getElementById('add-schedule');
    const urlFormsDiv = document.getElementById('url-forms');
    const scheduleFormsDiv = document.getElementById('schedule-forms');

    function updateFormIndex(formsDiv, prefix) {
        const forms = formsDiv.querySelectorAll('.form-group');
        forms.forEach((form, index) => {
            form.querySelectorAll('input, select, textarea').forEach(input => {
                input.name = input.name.replace(/-\d+-/, `-${index}-`);
                input.id = input.id.replace(/-\d+-/, `-${index}-`);
            });
        });
        formsDiv.querySelector(`#id_${prefix}-TOTAL_FORMS`).value = forms.length;
    }

    if (addUrlButton) {
        addUrlButton.addEventListener('click', function() {
            const newForm = urlFormsDiv.querySelector('.url-group').cloneNode(true);
            newForm.querySelectorAll('input, select').forEach(input => input.value = '');
            newForm.setAttribute('data-id', 'new');
            urlFormsDiv.appendChild(newForm);
            updateFormIndex(urlFormsDiv, 'url');
            const removeButton = newForm.querySelector('.remove-url-form');
            removeButton.setAttribute('data-id', 'new');
            newForm.querySelector('.remove-url-form').addEventListener('click', function() {
                newForm.remove();
                updateFormIndex(urlFormsDiv, 'url');
            });
        });
    }

    document.querySelectorAll('.remove-url-form').forEach(function(button) {
        button.addEventListener('click', function() {
            const urlGroups = urlFormsDiv.querySelectorAll('.url-group');
            if (urlGroups.length > 1){
            
                const urlId = this.getAttribute('data-id');
                if (urlId === 'new') {
                    this.closest('.url-group').remove();
                    updateFormIndex(urlFormsDiv, 'url');
                } else {
                    if (confirm('Tem certeza que deseja deletar esta URL?')) {
                        fetch(`/projects/project/delete-url/${urlId}/`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrftoken,
                            },
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === 'success') {
                                this.closest('.url-group').remove();
                                updateFormIndex(urlFormsDiv, 'url');
                            } else {
                                alert('Erro ao deletar a URL.');
                            }
                        });
                    }
                }
            }
            else{
                alert('O projeto deve conter pelo menos uma URL.');
            }
        });
        
    });

    // Função para validar e exibir mensagem de sucesso no formulário de contato
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();
            // Aqui você pode adicionar validação adicional se necessário
            const successMessage = document.getElementById('success-message');
            successMessage.style.display = 'block';
            contactForm.reset();
        });
    }


});