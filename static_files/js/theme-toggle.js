/**
 * theme-toggle.js
 * Persists and applies the light/dark theme chosen via the header switch.
 */

const themeToggleInput = document.querySelector('.theme-toggle__input');
if (themeToggleInput) {
  init(themeToggleInput);
}

/**
 * Wires up the theme switch and applies the stored/preferred theme on load.
 * @param {HTMLInputElement} toggleInput - The theme switch checkbox.
 */
function init(toggleInput) {
  toggleInput.addEventListener('change', (event) => applyTheme(event.target.checked ? 'dark' : 'light'));

  const storedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = storedTheme || (prefersDark ? 'dark' : null);

  if (theme) {
    document.documentElement.setAttribute('data-theme', theme);
    toggleInput.checked = theme === 'dark';
  }
}

/**
 * Applies and persists the given theme.
 * @param {'light'|'dark'} theme
 */
function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
}
