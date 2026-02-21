/**
 * Code Blocks JavaScript
 * Handles Prism.js initialization, copy-to-clipboard, and theme toggle functionality
 */

// Global code block theme preference (can be overridden per block)
const CODE_BLOCK_THEME_KEY = 'codeBlockTheme'

document.addEventListener('DOMContentLoaded', function () {
  // Initialize copy buttons for existing code blocks
  initCopyButtons()

  // Initialize theme toggle buttons
  initThemeToggles()

  // Apply stored global theme to all code blocks
  applyGlobalCodeTheme()

  // Also initialize when offcanvas is shown (in case content wasn't in DOM)
  document.addEventListener('shown.bs.offcanvas', function () {
    // Re-apply theme to ensure all blocks are synced from localStorage
    applyGlobalCodeTheme()
    // Re-wrap any unwrapped code blocks (in case offcanvas has new content)
    initCopyButtons()
    // Re-ensure theme toggles are ready
    initThemeToggles()
  })
})

/**
 * Apply stored global code theme to all code blocks
 */
function applyGlobalCodeTheme() {
  const storedTheme = localStorage.getItem(CODE_BLOCK_THEME_KEY) || 'dark'

  document.querySelectorAll('.code-block-wrapper').forEach(function (wrapper) {
    wrapper.setAttribute('data-code-theme', storedTheme)
  })

  // Dispatch event for other scripts
  window.dispatchEvent(
    new CustomEvent('codeThemeApplied', { detail: { theme: storedTheme } }),
  )
}

// Listen for global code theme changes from navbar toggle
window.addEventListener('codeThemeChanged', function (e) {
  const theme = e.detail.theme
  document.querySelectorAll('.code-block-wrapper').forEach(function (wrapper) {
    wrapper.setAttribute('data-code-theme', theme)
  })
})

/**
 * Initialize copy buttons for all code blocks on the page
 */
function initCopyButtons() {
  // Find all code blocks that don't already have a copy button wrapper
  document
    .querySelectorAll('pre code[class*="language-"]')
    .forEach(function (block) {
      const pre = block.parentElement

      // Skip if already wrapped (check parent for wrapper)
      if (
        pre.parentElement &&
        pre.parentElement.classList.contains('code-block-wrapper')
      ) {
        return
      }

      // Generate unique ID if not present
      if (!block.id) {
        const language = block.className.match(/language-(\S+)/)
        const lang = language ? language[1] : 'code'
        const hash = Math.random().toString(36).substr(2, 9)
        block.id = `code-${lang}-${hash}`
      }

      // Wrap the code block
      wrapCodeBlock(pre, block.id)
    })
}

// Track if delegated listener is already added
let delegatedListenerAdded = false

/**
 * Initialize theme toggle buttons for all code blocks
 * Uses event delegation for better compatibility
 */
function initThemeToggles() {
  // Only add the delegated listener once
  if (!delegatedListenerAdded) {
    document.addEventListener('click', handleThemeToggleClick)
    delegatedListenerAdded = true
  }
}

// Separate handler function for event delegation
function handleThemeToggleClick(event) {
  const button = event.target.closest('.theme-toggle-button')
  if (!button) return

  // Prevent default and stop propagation
  event.preventDefault()
  event.stopPropagation()

  const codeId = button.getAttribute('data-code-id')
  toggleCodeBlockTheme(codeId)
}

/**
 * Toggle theme for ALL code blocks (global toggle)
 */
function toggleCodeBlockTheme(codeId) {
  // Get current theme from localStorage or default to dark
  const currentTheme = localStorage.getItem(CODE_BLOCK_THEME_KEY) || 'dark'
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark'

  // Update ALL code block wrappers on the page
  document.querySelectorAll('.code-block-wrapper').forEach(function (wrapper) {
    wrapper.setAttribute('data-code-theme', newTheme)

    // Find the code element and re-highlight
    const codeElement = wrapper.querySelector('code')
    if (codeElement) {
      rehighlightCode(codeElement, newTheme)
    }
  })

  // Store preference in localStorage
  localStorage.setItem(CODE_BLOCK_THEME_KEY, newTheme)

  // Dispatch event so navbar toggle can sync
  window.dispatchEvent(
    new CustomEvent('codeThemeChanged', { detail: { theme: newTheme } }),
  )
}

/**
 * Re-highlight code with the appropriate theme
 */
function rehighlightCode(codeElement, theme) {
  // Store the raw code content
  const rawCode = codeElement.textContent

  // Get the language class
  const languageClass = Array.from(codeElement.classList).find((cls) =>
    cls.startsWith('language-'),
  )
  const language = languageClass
    ? languageClass.replace('language-', '')
    : 'plaintext'

  // Clear and re-set the content to trigger re-highlighting
  codeElement.textContent = rawCode

  // Re-apply Prism highlighting
  if (window.Prism) {
    Prism.highlightElement(codeElement)
  }
}

/**
 * Wrap a code block with action buttons (theme toggle and copy)
 */
function wrapCodeBlock(pre, codeId) {
  // Get stored theme preference or default to dark
  const storedTheme = localStorage.getItem(CODE_BLOCK_THEME_KEY) || 'dark'

  // Create wrapper div
  const wrapper = document.createElement('div')
  wrapper.className = 'code-block-wrapper'
  wrapper.setAttribute('data-code-theme', storedTheme)

  // Insert wrapper before pre
  pre.parentNode.insertBefore(wrapper, pre)

  // Move pre into wrapper
  wrapper.appendChild(pre)

  // Create actions container
  const actionsDiv = document.createElement('div')
  actionsDiv.className = 'code-block-actions'

  // Create theme toggle button
  const themeBtn = document.createElement('button')
  themeBtn.className = 'theme-toggle-button'
  themeBtn.setAttribute('type', 'button')
  themeBtn.setAttribute('aria-label', 'Toggle code block theme')
  themeBtn.setAttribute('data-code-id', codeId)
  themeBtn.innerHTML = `
    <span class="theme-icon theme-icon-dark">
      <i class="bi bi-moon-fill"></i>
    </span>
    <span class="theme-icon theme-icon-light">
      <i class="bi bi-sun-fill"></i>
    </span>
  `

  // Note: Theme toggle is handled by the delegated event listener in initThemeToggles()
  // This avoids double-firing when both direct and delegated handlers are attached

  // Create copy button
  const copyBtn = document.createElement('button')
  copyBtn.className = 'copy-button'
  copyBtn.setAttribute('type', 'button')
  copyBtn.setAttribute('aria-label', 'Copy code to clipboard')
  copyBtn.setAttribute('data-code-id', codeId)
  copyBtn.innerHTML = `
    <span class="copy-icon">
      <i class="bi bi-clipboard"></i>
    </span>
    <span class="check-icon" style="display: none;">
      <i class="bi bi-check-lg"></i>
    </span>
  `

  // Add click handler for copy
  copyBtn.addEventListener('click', function () {
    copyToClipboard(codeId, copyBtn)
  })

  // Add buttons to actions container
  actionsDiv.appendChild(themeBtn)
  actionsDiv.appendChild(copyBtn)

  // Insert actions at start of wrapper
  wrapper.insertBefore(actionsDiv, pre)
}

/**
 * Copy code to clipboard
 */
async function copyToClipboard(codeId, button) {
  const codeElement = document.getElementById(codeId)

  if (!codeElement) {
    showToast('Code element not found', 'error')
    return
  }

  const codeText = codeElement.textContent

  try {
    // Check clipboard API availability
    if (!navigator.clipboard || !navigator.clipboard.writeText) {
      throw new Error('Clipboard API not supported')
    }

    // Copy to clipboard
    await navigator.clipboard.writeText(codeText)

    // Show success state
    button.classList.add('copied')
    button.querySelector('.copy-icon').style.display = 'none'
    button.querySelector('.check-icon').style.display = 'inline'
    showToast('Copied!', 'success')

    // Reset after 2 seconds
    setTimeout(function () {
      button.classList.remove('copied')
      button.querySelector('.copy-icon').style.display = 'inline'
      button.querySelector('.check-icon').style.display = 'none'
    }, 2000)
  } catch (error) {
    // Handle errors gracefully
    console.warn('Copy failed:', error.message)
    showToast('Failed to copy - please use Ctrl+C', 'error')
  }
}

/**
 * Show a toast notification
 * This is a simple implementation until Story 6.3 (Toast Notifications) is complete
 */
function showToast(message, type) {
  // Create toast container if it doesn't exist
  let container = document.querySelector('.toast-container')

  if (!container) {
    container = document.createElement('div')
    container.className = 'toast-container'
    document.body.appendChild(container)
  }

  // Create toast element
  const toast = document.createElement('div')
  toast.className = `toast toast-${type}`
  toast.textContent = message

  // Add to container
  container.appendChild(toast)

  // Auto-dismiss after 3 seconds
  setTimeout(function () {
    toast.classList.add('hiding')

    // Remove after animation
    setTimeout(function () {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast)
      }
    }, 300)
  }, 3000)
}

// Expose showToast globally for other scripts to use
window.showToast = showToast
