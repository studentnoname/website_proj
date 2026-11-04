// Jung Jiwoong portfolio — mobile navigation, language hash preservation and scroll-driven water waves.
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

  // Scroll-driven water waves: the contour phase follows the scroll position, and a short
  // lagging "slosh" ripple settles within 600ms. Rendering only happens on scroll/resize.
  const root = document.documentElement;
  const waves = [...document.querySelectorAll('[data-pf-water]')].map(el => ({
    el, paths: [...el.querySelectorAll('path')], top: 0, h: 0
  }));
  const toggle = document.querySelector('[data-pf-motion-toggle]');
  if (!waves.length) return;

  const W = 1440, H = 120, SEG = 16, TAU = Math.PI * 2, SETTLE = 600, KEY = 'pf-motion';
  const LAYERS = [
    { base: 50, rise: 12, amp: 20, k: 1.15, k2: 2.4, v: 1, off: 0, tilt: 18, max: 100 },
    { base: 70, rise: 10, amp: 16, k: 1.5, k2: 3.1, v: -1.3, off: 2.1, tilt: -14, max: 108 },
    { base: 90, rise: 8, amp: 11, k: 0.85, k2: 2.2, v: 0.75, off: 4.2, tilt: 10, max: 112 }
  ];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const r1 = v => Math.round(v * 10) / 10;

  let pref = 'on';
  try { if (localStorage.getItem(KEY) === 'off') pref = 'off'; } catch { /* storage unavailable */ }
  const enabled = () => pref === 'on' && !reduce.matches;

  let vh = innerHeight, lag = scrollY, raf = 0, last = 0, input = 0;

  const setState = s => waves.forEach(w => { if (w.el.dataset.state !== s) w.el.dataset.state = s; });

  const shape = (w, i, phase, swell, s) => {
    w.paths.forEach((path, j) => {
      const L = LAYERS[j];
      if (!L) return;
      const o = L.off + i * 1.7;
      const amp = L.amp * (0.55 + 0.45 * swell + 0.6 * Math.abs(s));
      const base = L.base - L.rise * swell;
      const ph = (phase + s * 0.9) * L.v;
      const xs = [], ys = [];
      for (let n = 0; n <= SEG; n++) {
        const u = n / SEG;
        const y = base + s * L.tilt * (u - 0.5) + amp * (
          0.65 * Math.sin(TAU * L.k * u + ph + o) +
          0.35 * Math.sin(TAU * L.k2 * u - ph * 0.7 + o * 1.7));
        xs.push(u * W);
        ys.push(clamp(y, 4, L.max));
      }
      let d = `M0 ${H}L0 ${r1(ys[0])}L${r1(xs[1] / 2)} ${r1((ys[0] + ys[1]) / 2)}`;
      for (let n = 1; n < SEG; n++) {
        d += `Q${r1(xs[n])} ${r1(ys[n])} ${r1((xs[n] + xs[n + 1]) / 2)} ${r1((ys[n] + ys[n + 1]) / 2)}`;
      }
      path.setAttribute('d', `${d}L${W} ${r1(ys[SEG])}L${W} ${H}Z`);
    });
  };

  // Uses cached offsets only; returns whether any wave is on screen.
  const draw = y => {
    const s = clamp((y - lag) / 240, -1, 1);
    let any = false;
    waves.forEach((w, i) => {
      if (w.top > y + vh || w.top + w.h < y) return;
      any = true;
      const p = clamp((y + vh - w.top) / (vh + w.h), 0, 1);
      shape(w, i, p * Math.PI * 2.5, Math.sin(p * Math.PI), s);
    });
    return any;
  };
  const drawStatic = () => waves.forEach((w, i) => shape(w, i, 1.2, 0.5, 0));

  const stop = () => {
    if (raf) cancelAnimationFrame(raf);
    raf = 0;
    last = 0;
    setState('idle');
  };

  const tick = now => {
    raf = 0;
    if (!enabled() || document.hidden) return stop();
    const y = scrollY;
    const dt = last ? Math.min(64, now - last) : 16;
    last = now;
    lag = clamp(lag + (y - lag) * (1 - Math.exp(-dt / 140)), y - 360, y + 360);
    const settled = now - input > SETTLE || Math.abs(y - lag) < 0.5;
    if (settled) lag = y;
    const drawn = draw(y);
    if (settled || !drawn) { lag = y; return stop(); }
    raf = requestAnimationFrame(tick);
  };

  const onScroll = () => {
    if (!enabled() || document.hidden) return;
    input = performance.now();
    if (raf) return;
    setState('active');
    raf = requestAnimationFrame(tick);
  };

  const measure = () => {
    vh = innerHeight;
    const y = scrollY;
    waves.forEach(w => {
      const r = w.el.getBoundingClientRect();
      w.top = r.top + y;
      w.h = r.height;
    });
  };

  const refresh = () => {
    measure();
    stop();
    lag = scrollY;
    if (enabled()) draw(lag); else drawStatic();
  };

  const stateText = toggle && toggle.querySelector('.motion-state');
  const apply = () => {
    const on = enabled();
    root.dataset.pfMotion = on ? 'on' : 'off';
    if (toggle) {
      const sys = reduce.matches;
      toggle.setAttribute('aria-pressed', String(on));
      toggle.setAttribute('aria-disabled', String(sys));
      if (stateText) stateText.textContent = sys ? toggle.dataset.system : on ? toggle.dataset.enabledLabel : toggle.dataset.off;
    }
    refresh();
  };

  if (toggle) {
    toggle.addEventListener('click', () => {
      if (reduce.matches) return;
      pref = pref === 'on' ? 'off' : 'on';
      try { localStorage.setItem(KEY, pref); } catch { /* preference lasts for this page only */ }
      apply();
    });
    toggle.hidden = false;
  }

  reduce.addEventListener('change', apply);
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', refresh, { passive: true });
  document.addEventListener('visibilitychange', () => (document.hidden ? stop() : refresh()));
  if ('ResizeObserver' in window) new ResizeObserver(refresh).observe(document.body);
  else addEventListener('load', refresh);

  apply();
})();
