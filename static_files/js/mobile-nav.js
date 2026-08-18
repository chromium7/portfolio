(() => {
  const menuButton = document.querySelector('.app-header__menu-button');
  const mobileNav = document.querySelector('.mobile-nav');

  if (!menuButton || !mobileNav) return;

  const closeButton = mobileNav.querySelector('.mobile-nav__close');
  const backdrop = mobileNav.querySelector('.mobile-nav__backdrop');
  const firstLink = mobileNav.querySelector('.mobile-nav__link');

  const setOpen = (isOpen) => {
    mobileNav.classList.toggle('is-open', isOpen);
    mobileNav.setAttribute('aria-hidden', String(!isOpen));
    menuButton.setAttribute('aria-expanded', String(isOpen));
    menuButton.setAttribute('aria-label', isOpen ? 'Close navigation menu' : 'Open navigation menu');
    document.body.classList.toggle('is-nav-open', isOpen);

    if (isOpen) {
      firstLink?.focus();
    } else {
      menuButton.focus();
    }
  };

  menuButton.addEventListener('click', () => {
    setOpen(menuButton.getAttribute('aria-expanded') !== 'true');
  });
  closeButton?.addEventListener('click', () => setOpen(false));
  backdrop?.addEventListener('click', () => setOpen(false));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && mobileNav.classList.contains('is-open')) setOpen(false);
  });
  window.addEventListener('resize', () => {
    if (window.innerWidth >= 768 && mobileNav.classList.contains('is-open')) setOpen(false);
  });
})();
