/**
 * Split View JavaScript - Story 2.4
 * Provides draggable divider functionality for desktop
 * and tab switching for mobile view
 */
(function() {
  'use strict';

  // ========================================
  // Desktop: Draggable Divider
  // ========================================

  const container = document.querySelector('[data-split-view]');
  const divider = document.getElementById('split-divider');
  const codePanel = document.getElementById('split-code-panel');

  // Minimum and maximum widths for the code panel
  const MIN_WIDTH = 300;

  // Initialize split view only on desktop
  function initDesktopSplitView() {
    if (!container || !divider || !codePanel) return;

    // Check if we're on desktop (width >= 1024px)
    if (window.innerWidth < 1024) {
      initMobileTabs();
      return;
    }

    let isDragging = false;

    // Mouse down on divider
    divider.addEventListener('mousedown', function(e) {
      isDragging = true;
      container.classList.add('dragging');
      document.body.style.cursor = 'col-resize';
      e.preventDefault();
    });

    // Mouse move - calculate new width
    document.addEventListener('mousemove', function(e) {
      if (!isDragging) return;

      const containerRect = container.getBoundingClientRect();
      const newWidth = e.clientX - containerRect.left;
      const maxWidth = containerRect.width - MIN_WIDTH;

      if (newWidth >= MIN_WIDTH && newWidth <= maxWidth) {
        codePanel.style.width = newWidth + 'px';

        // Save preference to localStorage
        const ratio = newWidth / containerRect.width;
        localStorage.setItem('split-view-ratio', ratio.toString());
      }
    });

    // Mouse up - stop dragging
    document.addEventListener('mouseup', function() {
      if (isDragging) {
        isDragging = false;
        container.classList.remove('dragging');
        document.body.style.cursor = '';
      }
    });

    // Touch events for mobile/tablet support
    divider.addEventListener('touchstart', function(e) {
      isDragging = true;
      container.classList.add('dragging');
      e.preventDefault();
    }, { passive: false });

    document.addEventListener('touchmove', function(e) {
      if (!isDragging) return;

      const touch = e.touches[0];
      const containerRect = container.getBoundingClientRect();
      const newWidth = touch.clientX - containerRect.left;
      const maxWidth = containerRect.width - MIN_WIDTH;

      if (newWidth >= MIN_WIDTH && newWidth <= maxWidth) {
        codePanel.style.width = newWidth + 'px';

        // Save preference to localStorage
        const ratio = newWidth / containerRect.width;
        localStorage.setItem('split-view-ratio', ratio.toString());
      }
    }, { passive: true });

    document.addEventListener('touchend', function() {
      if (isDragging) {
        isDragging = false;
        container.classList.remove('dragging');
      }
    });

    // Keyboard accessibility for divider
    divider.addEventListener('keydown', function(e) {
      const step = 20;
      const containerRect = container.getBoundingClientRect();
      const currentWidth = codePanel.offsetWidth;
      const maxWidth = containerRect.width - MIN_WIDTH;

      let newWidth = currentWidth;

      if (e.key === 'ArrowLeft') {
        newWidth = Math.max(MIN_WIDTH, currentWidth - step);
        e.preventDefault();
      } else if (e.key === 'ArrowRight') {
        newWidth = Math.min(maxWidth, currentWidth + step);
        e.preventDefault();
      } else {
        return; // Ignore other keys
      }

      codePanel.style.width = newWidth + 'px';

      // Save preference
      const ratio = newWidth / containerRect.width;
      localStorage.setItem('split-view-ratio', ratio.toString());
    });

    // Restore saved preference
    restoreSplitRatio();
  }

  // Restore split ratio from localStorage
  function restoreSplitRatio() {
    const savedRatio = localStorage.getItem('split-view-ratio');
    if (savedRatio && codePanel && container) {
      const ratio = parseFloat(savedRatio);
      if (!isNaN(ratio) && ratio > 0 && ratio < 1) {
        const containerWidth = container.offsetWidth;
        codePanel.style.width = (containerWidth * ratio) + 'px';
      }
    }
  }

  // ========================================
  // Mobile: Demo/Code Tab Switching
  // ========================================

  function initMobileTabs() {
    const mobileTabs = document.querySelector('.mobile-view-tabs');
    if (!mobileTabs) return;

    const demoTab = mobileTabs.querySelector('[data-bs-target="#mobile-demo"]');
    const codeTab = mobileTabs.querySelector('[data-bs-target="#mobile-code"]');
    const demoPanel = document.getElementById('mobile-demo');
    const codePanelMobile = document.getElementById('mobile-code');

    // If using Bootstrap tabs, the tabs will handle the switching
    // But we need to sync with our custom split-view panels
    if (demoTab && codeTab) {
      demoTab.addEventListener('shown.bs.tab', function() {
        // Show demo panel, hide code panel
        document.getElementById('split-demo-panel').classList.add('active');
        document.getElementById('split-code-panel').classList.remove('active');
      });

      codeTab.addEventListener('shown.bs.tab', function() {
        // Show code panel, hide demo panel
        document.getElementById('split-code-panel').classList.add('active');
        document.getElementById('split-demo-panel').classList.remove('active');
      });
    }
  }

  // Initialize on page load
  document.addEventListener('DOMContentLoaded', function() {
    initDesktopSplitView();
  });

  // Re-initialize on window resize
  let resizeTimeout;
  window.addEventListener('resize', function() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(function() {
      // Reset to default 50/50 on resize
      if (codePanel && container && window.innerWidth >= 1024) {
        codePanel.style.width = '50%';
      }

      // Re-init for mobile/desktop switch
      initDesktopSplitView();
    }, 250);
  });

  // Re-run Prism highlight when code tab becomes visible
  document.addEventListener('shown.bs.tab', function(e) {
    const targetId = e.target.getAttribute('data-bs-target');
    if (targetId === '#mobile-code' || targetId === '#content-python' || targetId === '#content-html') {
      // Re-highlight code in the newly visible tab
      if (window.Prism) {
        const targetPanel = document.querySelector(targetId);
        if (targetPanel) {
          Prism.highlightAllUnder(targetPanel);
        }
      }
    }
  });

})();
