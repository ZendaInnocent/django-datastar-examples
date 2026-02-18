/**
 * Code Blocks JavaScript
 * Handles Prism.js initialization, copy-to-clipboard, and theme toggle functionality
 */

// Global code block theme preference (can be overridden per block)
const CODE_BLOCK_THEME_KEY = 'codeBlockTheme';

document.addEventListener('DOMContentLoaded', function() {
  // Initialize copy buttons for existing code blocks
  initCopyButtons();

  // Initialize theme toggle buttons
  initThemeToggles();
});

/**
 * Initialize copy buttons for all code blocks on the page
 */
function initCopyButtons() {
  // Find all code blocks that don't already have a copy button wrapper
  document.querySelectorAll('pre code[class*="language-"]').forEach(function(block) {
    const pre = block.parentElement;

    // Skip if already wrapped (check parent for wrapper)
    if (pre.parentElement && pre.parentElement.classList.contains('code-block-wrapper')) {
      return;
    }

    // Generate unique ID if not present
    if (!block.id) {
      const language = block.className.match(/language-(\S+)/);
      const lang = language ? language[1] : 'code';
      const hash = Math.random().toString(36).substr(2, 9);
      block.id = `code-${lang}-${hash}`;
    }

    // Wrap the code block
    wrapCodeBlock(pre, block.id);
  });
}

/**
 * Initialize theme toggle buttons for all code blocks
 */
function initThemeToggles() {
  document.querySelectorAll('.theme-toggle-button').forEach(function(button) {
    button.addEventListener('click', function() {
      const codeId = button.getAttribute('data-code-id');
      toggleCodeBlockTheme(codeId);
    });
  });
}

/**
 * Toggle theme for a specific code block
 */
function toggleCodeBlockTheme(codeId) {
  const codeElement = document.getElementById(codeId);
  if (!codeElement) return;

  const wrapper = codeElement.closest('.code-block-wrapper');
  if (!wrapper) return;

  const currentTheme = wrapper.getAttribute('data-code-theme') || 'dark';
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

  // Update the wrapper's theme attribute
  wrapper.setAttribute('data-code-theme', newTheme);

  // Re-highlight the code with the new theme
  rehighlightCode(codeElement, newTheme);

  // Store preference in localStorage (global for all code blocks)
  localStorage.setItem(CODE_BLOCK_THEME_KEY, newTheme);
}

/**
 * Re-highlight code with the appropriate theme
 */
function rehighlightCode(codeElement, theme) {
  // Store the raw code content
  const rawCode = codeElement.textContent;

  // Get the language class
  const languageClass = Array.from(codeElement.classList).find(cls => cls.startsWith('language-'));
  const language = languageClass ? languageClass.replace('language-', '') : 'plaintext';

  // Clear and re-set the content to trigger re-highlighting
  codeElement.textContent = rawCode;

  // Re-apply Prism highlighting
  if (window.Prism) {
    Prism.highlightElement(codeElement);
  }
}

/**
 * Wrap a code block with action buttons (theme toggle and copy)
 */
function wrapCodeBlock(pre, codeId) {
  // Get stored theme preference or default to dark
  const storedTheme = localStorage.getItem(CODE_BLOCK_THEME_KEY) || 'dark';

  // Create wrapper div
  const wrapper = document.createElement('div');
  wrapper.className = 'code-block-wrapper';
  wrapper.setAttribute('data-code-theme', storedTheme);

  // Insert wrapper before pre
  pre.parentNode.insertBefore(wrapper, pre);

  // Move pre into wrapper
  wrapper.appendChild(pre);

  // Create actions container
  const actionsDiv = document.createElement('div');
  actionsDiv.className = 'code-block-actions';

  // Create theme toggle button
  const themeBtn = document.createElement('button');
  themeBtn.className = 'theme-toggle-button';
  themeBtn.setAttribute('type', 'button');
  themeBtn.setAttribute('aria-label', 'Toggle code block theme');
  themeBtn.setAttribute('data-code-id', codeId);
  themeBtn.innerHTML = `
    <span class="theme-icon theme-icon-dark">
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
        <path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z"/>
      </svg>
    </span>
    <span class="theme-icon theme-icon-light">
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
        <path d="M6 .278a.768.768 0 0 1 .08.858 7.208 7.208 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277.527 0 1.04-.055 1.533-.16a.787.787 0 0 1 .81.316.733.733 0 0 1-.031.893A8.349 8.349 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.752.752 0 0 1 6 .278z"/>
      </svg>
    </span>
  `;

  // Add click handler for theme toggle
  themeBtn.addEventListener('click', function() {
    toggleCodeBlockTheme(codeId);
  });

  // Create copy button
  const copyBtn = document.createElement('button');
  copyBtn.className = 'copy-button';
  copyBtn.setAttribute('type', 'button');
  copyBtn.setAttribute('aria-label', 'Copy code to clipboard');
  copyBtn.setAttribute('data-code-id', codeId);
  copyBtn.innerHTML = `
    <span class="copy-icon">
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
        <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
        <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/>
      </svg>
    </span>
    <span class="check-icon" style="display: none;">
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
        <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/>
      </svg>
    </span>
  `;

  // Add click handler for copy
  copyBtn.addEventListener('click', function() {
    copyToClipboard(codeId, copyBtn);
  });

  // Add buttons to actions container
  actionsDiv.appendChild(themeBtn);
  actionsDiv.appendChild(copyBtn);

  // Insert actions at start of wrapper
  wrapper.insertBefore(actionsDiv, pre);
}

/**
 * Copy code to clipboard
 */
async function copyToClipboard(codeId, button) {
  const codeElement = document.getElementById(codeId);

  if (!codeElement) {
    showToast('Code element not found', 'error');
    return;
  }

  const codeText = codeElement.textContent;

  try {
    // Check clipboard API availability
    if (!navigator.clipboard || !navigator.clipboard.writeText) {
      throw new Error('Clipboard API not supported');
    }

    // Copy to clipboard
    await navigator.clipboard.writeText(codeText);

    // Show success state
    button.classList.add('copied');
    button.querySelector('.copy-icon').style.display = 'none';
    button.querySelector('.check-icon').style.display = 'inline';
    showToast('Copied!', 'success');

    // Reset after 2 seconds
    setTimeout(function() {
      button.classList.remove('copied');
      button.querySelector('.copy-icon').style.display = 'inline';
      button.querySelector('.check-icon').style.display = 'none';
    }, 2000);

  } catch (error) {
    // Handle errors gracefully
    console.warn('Copy failed:', error.message);
    showToast('Failed to copy - please use Ctrl+C', 'error');
  }
}

/**
 * Show a toast notification
 * This is a simple implementation until Story 6.3 (Toast Notifications) is complete
 */
function showToast(message, type) {
  // Create toast container if it doesn't exist
  let container = document.querySelector('.toast-container');

  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  // Create toast element
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;

  // Add to container
  container.appendChild(toast);

  // Auto-dismiss after 3 seconds
  setTimeout(function() {
    toast.classList.add('hiding');

    // Remove after animation
    setTimeout(function() {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }, 3000);
}

// Expose showToast globally for other scripts to use
window.showToast = showToast;
