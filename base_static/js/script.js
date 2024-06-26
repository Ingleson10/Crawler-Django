window.addEventListener('load', function() {
    fixFooterPosition();
  });

  function fixFooterPosition() {
      const footer = document.querySelector('footer');
      const content = document.querySelector('.container'); // Selecione o container do conteúdo
    
      if (content.offsetHeight < window.innerHeight) {
      
        footer.style.position = 'absolute';
        footer.style.bottom = 0;
        footer.style.width = '100%';
      } else {
        footer.style.position = 'static'; // Remova a posição absoluta
      }
    }

    document.addEventListener('DOMContentLoaded', function() {
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
              })
              .catch(error => console.error('Error:', error));
          });
      });
  });