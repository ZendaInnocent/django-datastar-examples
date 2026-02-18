/**
 * Sidebar mobile toggle functionality
 */
(function() {
  'use strict';

  const sidebar = document.getElementById('sidebar');
  const toggler = document.querySelector('.sidebar-toggler');

  if (!sidebar || !toggler) return;

  // Create backdrop
  const backdrop = document.createElement('div');
  backdrop.className = 'sidebar-backdrop';
  document.body.appendChild(backdrop);

  function openSidebar() {
    sidebar.classList.add('show');
    backdrop.classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    sidebar.classList.remove('show');
    backdrop.classList.remove('show');
    document.body.style.overflow = '';
  }

  function toggleSidebar() {
    if (sidebar.classList.contains('show')) {
      closeSidebar();
    } else {
      openSidebar();
    }
  }

  // Toggle button click
  toggler.addEventListener('click', toggleSidebar);

  // Backdrop click
  backdrop.addEventListener('click', closeSidebar);

  // Close on escape
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && sidebar.classList.contains('show')) {
      closeSidebar();
    }
  });

  // Close when clicking nav link
  sidebar.querySelectorAll('.nav-link').forEach(function(link) {
    link.addEventListener('click', function() {
      // Only close on mobile
      if (window.innerWidth < 992) {
        closeSidebar();
      }
    });
  });
})();
