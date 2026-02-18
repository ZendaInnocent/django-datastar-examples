/**
 * Header functionality - Search modal trigger and keyboard shortcuts
 * Story 3-4: Sticky Header with Search
 */

(function() {
  'use strict';

  /**
   * Detect if user is on Mac (without deprecated navigator.platform)
   */
  function isMac() {
    // Check for Mac via platform hints - modern approach
    const platform = navigator.platform?.toLowerCase() ?? '';
    const userAgent = navigator.userAgent?.toLowerCase() ?? '';

    return platform.includes('mac') ||
           userAgent.includes('mac') ||
           (navigator?.mediaDevices !== undefined &&
            navigator.maxTouchPoints > 0 &&
            userAgent.includes('iphone'));
  }

  /**
   * Get the appropriate keyboard shortcut display text
   */
  function getKeyboardShortcut() {
    return isMac() ? 'Cmd+K' : 'Ctrl+K';
  }

  // Initialize when DOM is ready
  document.addEventListener('DOMContentLoaded', function() {
    initSearchTrigger();
    initKeyboardShortcuts();
    updateKeyboardShortcutDisplay();
  });

  /**
   * Update the keyboard shortcut badge based on OS
   */
  function updateKeyboardShortcutDisplay() {
    const kbdElement = document.querySelector('[data-kbd-display]');
    const searchTrigger = document.getElementById('search-trigger');

    if (kbdElement) {
      kbdElement.textContent = getKeyboardShortcut();
    }

    // Also update aria-label on the button
    if (searchTrigger) {
      const shortcut = getKeyboardShortcut();
      searchTrigger.setAttribute('aria-label', `Search (${shortcut})`);
    }
  }

  /**
   * Initialize search trigger button
   */
  function initSearchTrigger() {
    const searchTrigger = document.getElementById('search-trigger');
    const searchModal = document.getElementById('search-modal');

    if (searchTrigger && searchModal) {
      searchTrigger.addEventListener('click', function() {
        openSearchModal();
      });
    }
  }

  /**
   * Open search modal and focus input
   */
  function openSearchModal() {
    const searchModalElement = document.getElementById('search-modal');
    const searchInput = document.getElementById('search-input');

    if (searchModalElement && searchInput) {
      // Use Bootstrap modal API
      const modal = bootstrap.Modal.getOrCreateInstance(searchModalElement);
      modal.show();

      // Focus input when modal is shown
      searchModalElement.addEventListener('shown.bs.modal', function() {
        searchInput.focus();
      }, { once: true });
    }
  }

  /**
   * Initialize keyboard shortcuts (Cmd+K / Ctrl+K)
   */
  function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(event) {
      // Check for Cmd+K (Mac) or Ctrl+K (Windows/Linux)
      // Use event.metaKey for Mac, event.ctrlKey for Windows/Linux
      const isModifierPressed = event.metaKey || event.ctrlKey;
      const isKPressed = event.key === 'k' || event.key === 'K';

      // Ignore if modifier + K is pressed
      if (isModifierPressed && isKPressed) {
        event.preventDefault();

        // Don't open search modal when typing in input fields
        const target = event.target;
        const isInputField = target.tagName === 'INPUT' ||
                           target.tagName === 'TEXTAREA' ||
                           target.tagName === 'SELECT' ||
                           target.isContentEditable;

        if (!isInputField) {
          openSearchModal();
        }
      }

      // Escape key to close modal (handled by Bootstrap, but backup)
      if (event.key === 'Escape') {
        const searchModal = document.getElementById('search-modal');
        if (searchModal && searchModal.classList.contains('show')) {
          const modal = bootstrap.Modal.getInstance(searchModal);
          if (modal) {
            modal.hide();
          }
        }
      }
    });
  }

  // Export for potential external use
  window.HeaderUtils = {
    openSearchModal: openSearchModal,
    isMac: isMac,
    getKeyboardShortcut: getKeyboardShortcut
  };
})();
