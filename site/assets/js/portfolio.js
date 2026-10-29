// Jung Jiwoong portfolio — mobile navigation and language hash preservation.
(() => {
  document.documentElement.classList.add('js');

  const nav = document.querySelector('[data-pf-nav]');
  const btn = document.querySelector('[data-pf-nav-toggle]');

  if (nav && btn) {
    const desk = matchMedia('(min-width: 1025px)');
    const isOpen = () => btn.getAttribute('aria-expanded') === 'true';
    const set = open => {
      btn.setAttribute('aria-expanded', String(open));
      nav.toggleAttribute('data-open', open);
    };

    btn.addEventListener('click', () => set(!isOpen()));
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && isOpen()) { set(false); btn.focus(); }
    });
    nav.querySelectorAll('[data-pf-nav-link]').forEach(a => a.addEventListener('click', () => set(false)));
    desk.addEventListener('change', e => { if (e.matches) set(false); });
  }

  const sectionHash = () => {
    let id = location.hash.slice(1);
    try { id = decodeURIComponent(id); } catch { return ''; }
    const el = id && document.getElementById(id);
    return el && el.hasAttribute('data-pf-section') ? '#' + id : '';
  };

  document.querySelectorAll('[data-pf-lang]').forEach(a => {
    const sync = () => { a.href = a.dataset.base + sectionHash(); };
    sync();
    addEventListener('hashchange', sync);
    a.addEventListener('click', sync);
  });
})();
