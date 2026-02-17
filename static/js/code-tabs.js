/**
 * Code Tabs JavaScript
 *
 * Provides tab switching functionality for code blocks.
 * Uses Bootstrap 5 tab API for instant switching.
 * Ensures Prism.js highlighting works in all tabs.
 */

(function() {
  'use strict';

  /**
   * Initialize code tabs functionality
   */
  function initCodeTabs() {
    // Handle tab shown event to re-run Prism highlighting
    document.addEventListener('shown.bs.tab', function(event) {
      const targetPane = event.target.getAttribute('data-bs-target');
      if (!targetPane) return;

      const pane = document.querySelector(targetPane);
      if (!pane) return;

      // Re-run Prism highlighting for the newly visible tab content
      if (window.Prism) {
        Prism.highlightAllUnder(pane);
      }

      // Update ARIA attributes for accessibility
      updateAriaAttributes(event.target, targetPane);
    });

    // Handle tab show event for pre-transition actions
    document.addEventListener('show.bs.tab', function(event) {
      const previousActive = document.querySelector('.code-tabs .nav-link.active');
      if (previousActive) {
        previousActive.setAttribute('aria-selected', 'false');
      }
    });

    // Initialize Prism for any pre-rendered code
    if (window.Prism) {
      Prism.highlightAll();
    }
  }

  /**
   * Update ARIA attributes for accessibility
   */
  function updateAriaAttributes(activeTab, targetId) {
    const targetPane = document.querySelector(targetId);
    if (!targetPane) return;

    // Update aria-selected on tabs
    document.querySelectorAll('.code-tabs .nav-link').forEach(function(tab) {
      const tabTarget = tab.getAttribute('data-bs-target');
      if (tabTarget === targetId) {
        tab.setAttribute('aria-selected', 'true');
      } else {
        tab.setAttribute('aria-selected', 'false');
      }
    });
  }

  /**
   * Get the currently active tab in a specific tab container
   * @param {string} containerId - The ID of the code-tabs-container
   * @returns {string|null} - The active tab name (html, python, or response) or null
   */
  function getActiveTab(containerId) {
    const container = document.getElementById('code-tabs-' + containerId);
    if (!container) return null;

    const activeTab = container.querySelector('.nav-link.active');
    if (!activeTab) return null;

    const target = activeTab.getAttribute('data-bs-target');
    if (!target) return null;

    // Extract tab name from target (e.g., "content-html-default" -> "html")
    const match = target.match(/content-(\w+)-/);
    return match ? match[1] : null;
  }

  /**
   * Programmatically switch to a specific tab
   * @param {string} containerId - The ID of the code-tabs-container
   * @param {string} tabName - The tab name (html, python, or response)
   */
  function switchToTab(containerId, tabName) {
    const container = document.getElementById('code-tabs-' + containerId);
    if (!container) return;

    const tabButton = container.querySelector('[data-bs-target="#content-' + tabName + '-' + containerId + '"]');
    if (!tabButton) return;

    // Use Bootstrap's tab API to switch
    const tabInstance = new bootstrap.Tab(tabButton);
    tabInstance.show();
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCodeTabs);
  } else {
    initCodeTabs();
  }

  // Expose public API
  window.CodeTabs = {
    getActiveTab: getActiveTab,
    switchToTab: switchToTab
  };

})();
