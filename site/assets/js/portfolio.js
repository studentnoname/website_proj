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

  // Mark the menu link of the section crossing the middle of the viewport.
  const links = [...document.querySelectorAll('[data-pf-nav-link]')];
  const targets = new Map();
  links.forEach(a => {
    const href = a.getAttribute('href') || '';
    const i = href.indexOf('#');
    const el = i >= 0 && document.getElementById(href.slice(i + 1));
    if (el && el.hasAttribute('data-pf-section')) targets.set(el, a);
  });

  if ('IntersectionObserver' in window && targets.size) {
    const visible = new Set();
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => (e.isIntersecting ? visible.add(e.target) : visible.delete(e.target)));
      const current = [...targets.keys()].find(el => visible.has(el));
      links.forEach(a => a.removeAttribute('aria-current'));
      if (current) targets.get(current).setAttribute('aria-current', 'location');
    }, { rootMargin: '-45% 0px -50% 0px' });
    targets.forEach((_, el) => io.observe(el));
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
