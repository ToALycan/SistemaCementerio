document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('mainSidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const body = document.body;

    // Toggle sidebar
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            if (window.innerWidth >= 768) {
                // Desktop behavior
                sidebar.classList.toggle('collapsed');
                body.classList.toggle('sidebar-collapsed');
                localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
            } else {
                // Mobile behavior
                sidebar.classList.toggle('show');
            }
        });
    }

    // Load saved state
    if (localStorage.getItem('sidebarCollapsed') === 'true' && window.innerWidth >= 768) {
        sidebar.classList.add('collapsed');
        body.classList.add('sidebar-collapsed');
    }

    // Auto-close sidebar on mobile when clicking a link
    if (window.innerWidth < 768) {
        const navLinks = document.querySelectorAll('.sidebar .nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                sidebar.classList.remove('show');
            });
        });
    }
});