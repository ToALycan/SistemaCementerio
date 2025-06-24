// Navbar toggle mobile
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');

navToggle.addEventListener('click', () => {
  const expanded = navToggle.getAttribute('aria-expanded') === 'true' || false;
  navToggle.setAttribute('aria-expanded', !expanded);
  navMenu.classList.toggle('show');
});

// Mostrar modal
function mostrarModal(id) {
  const modal = document.getElementById(id);
  modal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden'; // Bloquea scroll cuando modal abierto
  modal.querySelector('.modal-close').focus();
}

// Cerrar modal
function cerrarModal(id) {
  const modal = document.getElementById(id);
  modal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = 'auto'; // Rehabilita scroll
}

// Cerrar modal con tecla ESC
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal[aria-hidden="false"]').forEach(modal => {
      cerrarModal(modal.id);
    });
  }
});
