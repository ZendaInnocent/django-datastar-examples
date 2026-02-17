/**
 * Code Blocks JavaScript
 * Handles Prism.js initialization and copy-to-clipboard functionality
 */

document.addEventListener('DOMContentLoaded', function() {
  // Initialize copy buttons for existing code blocks
  initCopyButtons();
});

/**
 * Initialize copy buttons for all code blocks on the page
 */
function initCopyButtons() {
  // Find all code blocks that don't already have a copy button wrapper
  document.querySelectorAll('pre code[class*="language-"]').forEach(function(block) {
    const pre = block.parentElement;

    // Skip if already wrapped
    if (pre.classList.contains('code-block-wrapper')) {
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
 * Wrap a code block with a copy button
 */
function wrapCodeBlock(pre, codeId) {
  // Create wrapper div
  const wrapper = document.createElement('div');
  wrapper.className = 'code-block-wrapper';

  // Insert wrapper before pre
  pre.parentNode.insertBefore(wrapper, pre);

  // Move pre into wrapper
  wrapper.appendChild(pre);

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

  // Add click handler
  copyBtn.addEventListener('click', function() {
    copyToClipboard(codeId, copyBtn);
  });

  // Insert button at start of wrapper
  wrapper.insertBefore(copyBtn, pre);
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
