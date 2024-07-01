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
                    window.location.href = `/projects/project/${projectId}/?edit=true`;
                } else {
                    alert("Project ID is missing.");
                }
            });
        }
    }

    // Adiciona o listener ao botão de edição ao carregar o DOM
    addEditButtonListener();

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
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Adiciona formulários de URL dinamicamente
    const addUrlButton = document.getElementById('add-url');
    if (addUrlButton) {
        addUrlButton.addEventListener('click', function() {
            const urlFormsDiv = document.getElementById('url-forms');
            const newFormHtml = `
                <div class="form-group">
                    <input type="text" name="url" class="form-control" placeholder="URL">
                    <select name="status" class="form-control">
                        <option value="valid">Válida</option>
                        <option value="invalid">Inválida</option>
                    </select>
                </div>
            `;
            urlFormsDiv.insertAdjacentHTML('beforeend', newFormHtml);
        });
    }

    // Adiciona formulários de agendamento dinamicamente
    const addScheduleButton = document.getElementById('add-schedule');
    if (addScheduleButton) {
        addScheduleButton.addEventListener('click', function() {
            const scheduleFormsDiv = document.getElementById('schedule-forms');
            const newFormHtml = `
                <div class="form-group">
                    <select name="frequency" class="form-control">
                        <option value="daily">Diária</option>
                        <option value="weekly">Semanalmente</option>
                        <option value="monthly">Mensalmente</option>
                    </select>
                    <input type="datetime-local" name="next_run" class="form-control">
                </div>
            `;
            scheduleFormsDiv.insertAdjacentHTML('beforeend', newFormHtml);
        });
    }

    // Adiciona formulários de regras de scraping dinamicamente
    const addRuleButton = document.getElementById('add-rule');
    if (addRuleButton) {
        addRuleButton.addEventListener('click', function() {
            const ruleFormsDiv = document.getElementById('rule-forms');
            const newFormHtml = `
                <div class="form-group">
                    <input type="text" name="selector" class="form-control" placeholder="Seletor">
                    <select name="type" class="form-control">
                        <option value="CSS">CSS</option>
                        <option value="XPath">XPath</option>
                    </select>
                </div>
            `;
            ruleFormsDiv.insertAdjacentHTML('beforeend', newFormHtml);
        });
    }

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