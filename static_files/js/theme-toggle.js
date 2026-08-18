/**
 * theme-toggle.js
 * Persists and applies the light/dark theme chosen via the header switch.
 */

const themeToggleInputs = document.querySelectorAll('.theme-toggle__input');
if (themeToggleInputs.length) {
  init(themeToggleInputs);
}

/**
 * Wires up the theme switch and applies the stored/preferred theme on load.
 * @param {NodeListOf<HTMLInputElement>} toggleInputs - Theme switch checkboxes.
 */
function init(toggleInputs) {
  const storedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = storedTheme || (prefersDark ? 'dark' : 'light');

  applyTheme(theme, toggleInputs);
  toggleInputs.forEach((toggleInput) => {
    toggleInput.addEventListener('change', (event) => {
      applyTheme(event.target.checked ? 'dark' : 'light', toggleInputs);
    });
  });
}

/**
 * Applies and persists the given theme.
 * @param {'light'|'dark'} theme
 * @param {NodeListOf<HTMLInputElement>} toggleInputs
 */
function applyTheme(theme, toggleInputs) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
  toggleInputs.forEach((toggleInput) => {
    toggleInput.checked = theme === 'dark';
  });
}
