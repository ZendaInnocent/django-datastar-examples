/**
 * Header functionality - Search modal trigger and keyboard shortcuts
 * Story 3-4: Sticky Header with Search
 * Updated Story 4-1: Search Modal UI - Added result click handling
 * Updated Story 4-3: Search Keyboard Navigation - Added arrow key navigation
 * Updated Story 4-4: Recent Searches - Added recent searches functionality
 */

(function() {
  'use strict';

  /**
   * Recent Searches Class - Story 4-4
   * Manages recent searches storage and display
   */
  class RecentSearches {
    constructor() {
      this.storageKey = 'datastar-recent-searches';
      this.maxItems = 10;
      this.recentSearches = this.load();
    }

    load() {
      try {
        const stored = localStorage.getItem(this.storageKey);
        return stored ? JSON.parse(stored) : [];
      } catch (e) {
        console.warn('localStorage not available');
        return [];
      }
    }

    save() {
      try {
        localStorage.setItem(this.storageKey, JSON.stringify(this.recentSearches));
      } catch (e) {
        console.warn('Could not save recent searches');
      }
    }

    add(query, url, title) {
      // Trim and validate
      query = query.trim();
      if (!query) return;

      // Remove duplicate if exists
      this.recentSearches = this.recentSearches.filter(
        item => item.query.toLowerCase() !== query.toLowerCase()
      );

      // Add to front
      this.recentSearches.unshift({
        query: query,
        url: url,
        title: title || query,
        timestamp: Date.now()
      });

      // Limit to maxItems
      if (this.recentSearches.length > this.maxItems) {
        this.recentSearches = this.recentSearches.slice(0, this.maxItems);
      }

      this.save();
    }

    remove(query) {
      this.recentSearches = this.recentSearches.filter(
        item => item.query.toLowerCase() !== query.toLowerCase()
      );
      this.save();
    }

    clear() {
      this.recentSearches = [];
      this.save();
    }

    getAll() {
      return this.recentSearches;
    }
  }

  // Create global instance
  const recentSearches = new RecentSearches();

  /**
   * Render recent searches in the modal
   */
  function renderRecentSearches() {
    const container = document.getElementById('recent-searches');
    const resultsContainer = document.getElementById('search-results');
    const searchInput = document.getElementById('search-input');

    if (!container) return;

    const recent = recentSearches.getAll();
    const query = searchInput ? searchInput.value.trim() : '';

    // Show recent searches only when input is empty and there are recent searches
    if (query || recent.length === 0) {
      container.classList.add('d-none');
      return;
    }

    container.classList.remove('d-none');

    container.innerHTML = `
      <div class="recent-searches-header">
        <small class="text-muted">Recent Searches</small>
        <button type="button" class="btn btn-link btn-sm p-0" onclick="clearAllRecentSearches()">
          Clear all
        </button>
      </div>
      ${recent.map(item => `
        <div class="recent-search-item" onclick="runRecentSearch('${escapeHtml(item.query)}')">
          <i class="bi bi-clock-history search-icon"></i>
          <span class="recent-query">${escapeHtml(item.query)}</span>
          <button type="button" class="btn btn-link remove-btn p-0"
                  onclick="event.stopPropagation(); removeRecentSearch('${escapeHtml(item.query)}')">
            <i class="bi bi-x"></i>
          </button>
        </div>
      `).join('')}
    `;

    // Hide search results when showing recent searches
    if (resultsContainer) {
      resultsContainer.classList.add('d-none');
    }
  }

  /**
   * Escape HTML to prevent XSS
   */
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  /**
   * Run a search from recent searches
   */
  function runRecentSearch(query) {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
      searchInput.value = query;
      // Trigger the search via Datastar
      searchInput.dispatchEvent(new Event('input', { bubbles: true }));
    }
  }

  /**
   * Remove a single recent search
   */
  function removeRecentSearch(query) {
    recentSearches.remove(query);
    renderRecentSearches();
  }

  /**
   * Clear all recent searches
   */
  function clearAllRecentSearches() {
    recentSearches.clear();
    renderRecentSearches();
  }

  /**
   * Save search to recent searches when a result is clicked
   */
  function saveRecentSearch(query, url, title) {
    if (query && query.trim()) {
      recentSearches.add(query.trim(), url, title);
      renderRecentSearches();
    }
  }

  // Make functions globally accessible for onclick handlers
  window.runRecentSearch = runRecentSearch;
  window.removeRecentSearch = removeRecentSearch;
  window.clearAllRecentSearches = clearAllRecentSearches;
  window.saveRecentSearch = saveRecentSearch;

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

  /**
   * Search Keyboard Navigation - Story 4-3
   * Tracks selected index for keyboard navigation
   */
  let searchSelectedIndex = -1;
  let searchResultItems = [];

  /**
   * Get all search result items from the results container
   */
  function getSearchResultItems() {
    const resultsContainer = document.getElementById('search-results');
    if (!resultsContainer) return [];
    return resultsContainer.querySelectorAll('.search-result-item');
  }

  /**
   * Update visual selection state for keyboard navigation
   */
  function updateSearchSelection() {
    searchResultItems = getSearchResultItems();

    // Remove active class and aria-selected from all items
    searchResultItems.forEach((item) => {
      item.classList.remove('active');
      item.setAttribute('aria-selected', 'false');
      item.style.outline = 'none';
    });

    // Add active class and aria-selected to current selection
    if (searchSelectedIndex >= 0 && searchSelectedIndex < searchResultItems.length) {
      const selected = searchResultItems[searchSelectedIndex];
      selected.classList.add('active');
      selected.setAttribute('aria-selected', 'true');
      selected.style.outline = '2px solid #6B46C1';
      selected.style.outlineOffset = '-2px';

      // Scroll into view if needed
      selected.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }

  /**
   * Navigate to the selected result
   */
  function navigateToSelectedResult() {
    if (searchSelectedIndex >= 0 && searchSelectedIndex < searchResultItems.length) {
      const selected = searchResultItems[searchSelectedIndex];
      const url = selected.getAttribute('data-result-url') ||
                  selected.getAttribute('href');
      const title = selected.querySelector('.search-result-title')?.textContent || '';
      const searchInput = document.getElementById('search-input');
      const query = searchInput ? searchInput.value.trim() : '';

      if (url) {
        // Save to recent searches before navigating - Story 4-4
        if (query) {
          recentSearches.add(query, url, title);
        }

        // Close modal first
        const searchModal = document.getElementById('search-modal');
        if (searchModal) {
          const modal = bootstrap.Modal.getInstance(searchModal);
          if (modal) {
            modal.hide();
          }
        }
        // Navigate to the URL
        window.location.href = url;
      }
    }
  }

  /**
   * Handle keyboard navigation in search modal
   */
  function handleSearchKeyboardNavigation(event) {
    const searchModal = document.getElementById('search-modal');
    if (!searchModal || !searchModal.classList.contains('show')) {
      return;
    }

    searchResultItems = getSearchResultItems();
    if (searchResultItems.length === 0) {
      return;
    }

    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault();
        searchSelectedIndex++;
        if (searchSelectedIndex >= searchResultItems.length) {
          searchSelectedIndex = 0; // Wrap to first
        }
        updateSearchSelection();
        break;

      case 'ArrowUp':
        event.preventDefault();
        searchSelectedIndex--;
        if (searchSelectedIndex < 0) {
          searchSelectedIndex = searchResultItems.length - 1; // Wrap to last
        }
        updateSearchSelection();
        break;

      case 'Enter':
        event.preventDefault();
        if (searchSelectedIndex >= 0) {
          navigateToSelectedResult();
        }
        break;

      case 'Home':
        if (event.ctrlKey || event.metaKey) {
          event.preventDefault();
          searchSelectedIndex = 0;
          updateSearchSelection();
        }
        break;

      case 'End':
        if (event.ctrlKey || event.metaKey) {
          event.preventDefault();
          searchSelectedIndex = searchResultItems.length - 1;
          updateSearchSelection();
        }
        break;
    }
  }

  /**
   * Reset search selection when results change
   */
  function resetSearchSelection() {
    searchSelectedIndex = -1;
    searchResultItems = getSearchResultItems();
    searchResultItems.forEach((item) => {
      item.classList.remove('active');
      item.setAttribute('aria-selected', 'false');
      item.style.outline = 'none';
    });
  }

  // Initialize when DOM is ready
  document.addEventListener('DOMContentLoaded', function() {
    initSearchTrigger();
    initKeyboardShortcuts();
    initSearchResults();
    initSearchKeyboardNavigation();
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
        // Render recent searches when modal opens - Story 4-4
        renderRecentSearches();
      }, { once: true });
    }
  }

  /**
   * Initialize search results click handling
   */
  function initSearchResults() {
    // Use event delegation for dynamically loaded search results
    document.addEventListener('click', function(event) {
      const resultItem = event.target.closest('.search-result-item');
      if (resultItem) {
        const url = resultItem.getAttribute('data-result-url') || resultItem.getAttribute('href');
        const title = resultItem.querySelector('.search-result-title')?.textContent || '';
        const searchInput = document.getElementById('search-input');
        const query = searchInput ? searchInput.value.trim() : '';

        if (url) {
          // Save to recent searches before navigating - Story 4-4
          if (query) {
            recentSearches.add(query, url, title);
          }

          // Close modal first
          const searchModal = document.getElementById('search-modal');
          if (searchModal) {
            const modal = bootstrap.Modal.getInstance(searchModal);
            if (modal) {
              modal.hide();
            }
          }
          // Navigate to the URL
          window.location.href = url;
        }
      }
    });
  }

  /**
   * Initialize keyboard navigation for search results - Story 4-3
   */
  function initSearchKeyboardNavigation() {
    // Listen for arrow keys and Enter when modal is open
    document.addEventListener('keydown', handleSearchKeyboardNavigation);

    // Listen for Datastar updates to reset selection when results change
    const resultsContainer = document.getElementById('search-results');
    if (resultsContainer) {
      // Use MutationObserver to detect when results change
      const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
          if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            // Results changed, reset selection
            resetSearchSelection();
          }
        });
      });

      observer.observe(resultsContainer, { childList: true, subtree: true });
    }

    // Also reset selection when modal is opened
    const searchModal = document.getElementById('search-modal');
    if (searchModal) {
      searchModal.addEventListener('shown.bs.modal', function() {
        resetSearchSelection();
      });

      // Reset when input changes (new search)
      const searchInput = document.getElementById('search-input');
      if (searchInput) {
        searchInput.addEventListener('input', function() {
          resetSearchSelection();
          // Show/hide recent searches based on input - Story 4-4
          renderRecentSearches();
        });
      }
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
