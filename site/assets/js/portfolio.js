// Jung Jiwoong portfolio — mobile navigation, language hash preservation,
// staggered text entrance and layered screen-over-screen panels.
(() => {
  const root = document.documentElement;
  root.classList.add('js');

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
  // Layered tracks overlap the next one, so the later (topmost) section wins.
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
      const current = [...targets.keys()].filter(el => visible.has(el)).pop();
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

  // Motion preference: the system reduced-motion setting always wins.
  const KEY = 'pf-panel-motion';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  let pref = null;
  try { pref = localStorage.getItem(KEY); } catch {}
  const wanted = () => !reduce.matches && pref !== 'off';
  let motion = false;

  // Text entrance: finite WAAPI rises; content stays visible when scripts or WAAPI are unavailable.
  const canAnimate = typeof Element.prototype.animate === 'function';
  const anims = new Map();
  const seen = new WeakSet();

  const rise = (el, delay) => {
    if (!canAnimate) return;
    const a = el.animate(
      [{ opacity: 0, transform: 'translateY(20px)' }, { opacity: 1, transform: 'none' }],
      { duration: 640, delay, easing: 'cubic-bezier(.2, .65, .25, 1)', fill: 'backwards' }
    );
    const done = () => { if (anims.get(el) === a) anims.delete(el); };
    a.addEventListener('finish', done);
    a.addEventListener('cancel', done);
    anims.set(el, a);
  };

  const settle = scope => anims.forEach((a, el) => {
    if (scope.contains(el) || el.contains(scope)) a.finish();
  });

  // Deep-link and in-page jump destinations are shown at once, never left waiting on an entrance.
  const reach = el => {
    const scope = el.closest('[data-pf-section]') || el;
    if (scope.matches('[data-pf-reveal]')) seen.add(scope);
    scope.querySelectorAll('[data-pf-reveal]').forEach(b => seen.add(b));
    settle(scope);
  };

  const byId = raw => {
    let id = raw.slice(1);
    try { id = decodeURIComponent(id); } catch { return null; }
    return id ? document.getElementById(id) : null;
  };

  const deep = byId(location.hash);
  if (deep) reach(deep);

  document.addEventListener('click', e => {
    const a = e.target instanceof Element && e.target.closest('a[href*="#"]');
    if (!a || a.origin !== location.origin || a.pathname !== location.pathname) return;
    const el = byId(a.hash);
    if (el) reach(el);
  }, true);
  addEventListener('hashchange', () => {
    const el = byId(location.hash);
    if (el) reach(el);
  });

  // Layered panels.
  const header = document.querySelector('.site-header');
  const tracks = [...document.querySelectorAll('[data-pf-panel-track]')];
  const panels = tracks.map(t => t.querySelector('[data-pf-panel]'));
  const clips = tracks.map(t => document.getElementById('pf-clip-' + t.id));
  const paths = clips.map(c => c && c.querySelector('path'));
  const n = tracks.length;
  const canLayer = n > 1 && panels.every(Boolean) && 'ResizeObserver' in window &&
    !!(window.CSS && CSS.supports('position', 'sticky'));
  const narrow = matchMedia('(max-width: 860px)');

  let layout = null;
  let anchor = null;
  let resized = false;
  let width = innerWidth;
  let shown = [];

  const clamp = v => Math.min(1, Math.max(0, v));
  const headerHeight = () => (header ? header.getBoundingClientRect().height : 0);

  // Broad leading edge in objectBoundingBox units; every point stays within `a` of the panel top.
  const edge = (a, p) => {
    const ph = p * 2.4;
    const w = k => a * (0.5 + 0.5 * Math.sin(ph + k));
    const y0 = w(0.4), y1 = w(1.6), y2 = w(2.7), y3 = w(4.1), y4 = w(5.6);
    const f = v => v.toFixed(5);
    return `M0 ${f(y0)}C.18 ${f(y1)} .34 ${f(y2)} .5 ${f((y2 + y3) / 2)}S.82 ${f(y4)} 1 ${f(y4)}V1H0Z`;
  };

  const resetShown = () => { shown = panels.map(() => ({ p: -1, clip: false, under: -1 })); };

  function render() {
    sraf = 0;
    if (!layout) return;
    const { hh, hs, tops, overs, amp } = layout;
    const y = scrollY;

    // Cover progress of each incoming panel: 0 when the previous one starts holding, 1 when it is fully covered.
    const prog = tops.map((top, j) => {
      if (!j) return 1;
      const v = overs[j - 1];
      return v > 0 ? clamp((hh + v - (top - y)) / v) : 1;
    });

    if (!resized) {
      let i = 0;
      tops.forEach((top, k) => { if (top - y <= hh + 1) i = k; });
      anchor = { i, ratio: clamp((y + hh - tops[i]) / hs[i]) };
    }

    panels.forEach((panel, j) => {
      const p = prog[j];
      const s = shown[j];
      const active = p > 0 && p < 1;
      if (p !== s.p) {
        panel.dataset.progress = String(+p.toFixed(3));
        panel.dataset.state = active ? 'active' : 'idle';
        s.p = p;
      }
      const clip = active && !!paths[j];
      if (clip) {
        // Never deeper than the overlap so far, so the dip always shows the older panel beneath.
        const a = Math.min(amp * Math.sin((1 - p) * Math.PI / 2), p * overs[j - 1]);
        paths[j].setAttribute('d', edge(a / hs[j], p));
      }
      if (clip !== s.clip) {
        panel.style.clipPath = clip ? `url(#${clips[j].id})` : '';
        s.clip = clip;
      }
      const under = j < n - 1 ? Math.round(prog[j + 1] * 16) / 100 : 0;
      if (under !== s.under) {
        panel.style.setProperty('--pf-under', String(under));
        s.under = under;
      }
    });
  }

  function unlayer() {
    layout = null;
    root.style.removeProperty('--pf-hh');
    tracks.forEach(t => {
      t.removeAttribute('data-pf-ready');
      t.style.removeProperty('--pf-h');
      t.style.removeProperty('--pf-z');
    });
    panels.forEach(panel => {
      panel.style.clipPath = '';
      panel.style.removeProperty('--pf-under');
      panel.dataset.progress = '1';
      panel.dataset.state = 'idle';
    });
    resetShown();
  }

  function measure() {
    mraf = 0;
    if (!motion || !canLayer) { resized = false; return; }
    const hh = headerHeight();
    const hs = panels.map(p => p.getBoundingClientRect().height);
    if (!hs.every(h => h > 0) || !(innerHeight > hh)) { resized = false; unlayer(); return; }

    root.style.setProperty('--pf-hh', hh + 'px');
    tracks.forEach((t, i) => {
      t.style.setProperty('--pf-h', hs[i] + 'px');
      t.style.setProperty('--pf-z', String(i + 1));
      t.setAttribute('data-pf-ready', '');
    });

    const y = scrollY;
    const tops = tracks.map(t => t.getBoundingClientRect().top + y);
    const overs = tracks.map(t => Math.max(0, -parseFloat(getComputedStyle(t).marginBottom) || 0));
    layout = { hh, hs, tops, overs, amp: narrow.matches ? 28 : 50 };

    // After a width change, keep the section being read at the same relative point.
    if (resized && anchor && anchor.i < n) {
      const target = tops[anchor.i] + anchor.ratio * hs[anchor.i] - hh;
      if (Math.abs(target - y) > 2) scrollTo(0, target);
    }
    resized = false;
    render();
  }

  let sraf = 0;
  let mraf = 0;
  const queueRender = () => { if (layout && !sraf) sraf = requestAnimationFrame(render); };
  const queueMeasure = () => { if (!mraf) mraf = requestAnimationFrame(measure); };
  const ro = canLayer ? new ResizeObserver(queueMeasure) : null;

  if (panels.every(Boolean)) {
    resetShown();
    panels.forEach(panel => { panel.dataset.progress = '1'; panel.dataset.state = 'idle'; });
  }

  // Reading position in normal-flow terms, used to keep text in place across a mode switch.
  const capture = () => {
    const hh = headerHeight();
    let hit = null;
    tracks.forEach((t, i) => {
      const top = t.getBoundingClientRect().top;
      if (top <= hh + 1) hit = { i, off: hh - top };
    });
    return hit;
  };
  const restore = a => {
    const d = tracks[a.i].getBoundingClientRect().top + a.off - headerHeight();
    if (Math.abs(d) > 1) scrollBy(0, d);
  };

  // A focused control inside a covered panel is brought to where that panel is uncovered.
  const uncover = t => {
    if (!layout || document.activeElement !== t) return;
    const i = panels.findIndex(p => p.contains(t));
    if (i < 0 || i === n - 1) return;
    const r = t.getBoundingClientRect();
    const next = panels[i + 1].getBoundingClientRect();
    if (next.top >= r.bottom || next.bottom <= r.top) return;
    const y = r.top - panels[i].getBoundingClientRect().top;
    const stick = parseFloat(getComputedStyle(panels[i]).top);
    const trackTop = Math.max(Number.isNaN(stick) ? layout.hh : stick, layout.hh + 24 - y);
    scrollTo(0, layout.tops[i] - trackTop);
  };

  document.addEventListener('focusin', e => {
    const t = e.target;
    if (!(t instanceof Element)) return;
    const block = t.closest('[data-pf-reveal]');
    if (block) seen.add(block);
    settle(t);
    if (layout) requestAnimationFrame(() => uncover(t));
  });

  // Footer control.
  const toggle = document.querySelector('[data-pf-motion-toggle]');
  const status = document.querySelector('[data-pf-motion-status]');
  const control = toggle && toggle.closest('[data-pf-motion-control]');

  const sync = () => {
    if (!toggle) return;
    if (control) control.hidden = false;
    toggle.setAttribute('aria-pressed', String(motion));
    if (reduce.matches) toggle.setAttribute('aria-disabled', 'true');
    else toggle.removeAttribute('aria-disabled');
    if (status) {
      const d = status.dataset;
      status.textContent = reduce.matches ? d.reducedLabel : motion ? d.enabledLabel : d.disabledLabel;
    }
  };

  const apply = initial => {
    const on = wanted();
    if (initial || on !== motion) {
      const keep = !initial && canLayer ? capture() : null;
      motion = on;
      root.dataset.pfMotion = on ? 'on' : 'off';
      if (on) {
        resized = false;
        if (ro) {
          if (header) ro.observe(header);
          panels.forEach(p => ro.observe(p));
          measure();
        }
      } else {
        anims.forEach(a => a.cancel());
        if (ro) ro.disconnect();
        if (canLayer) unlayer();
      }
      if (keep) restore(keep);
    }
    sync();
  };

  if (toggle) {
    toggle.addEventListener('click', () => {
      if (reduce.matches) return;
      pref = motion ? 'off' : 'on';
      try { localStorage.setItem(KEY, pref); } catch {}
      apply(false);
    });
  }

  if (reduce.addEventListener) reduce.addEventListener('change', () => apply(false));
  else if (reduce.addListener) reduce.addListener(() => apply(false));

  addEventListener('scroll', queueRender, { passive: true });
  addEventListener('resize', () => {
    if (innerWidth !== width) { width = innerWidth; resized = true; }
    if (motion) queueMeasure();
  }, { passive: true });

  apply(true);

  // First entry: hero heading lines and intro arrive one by one.
  const heroBlocks = n ? [...tracks[0].querySelectorAll('[data-pf-reveal]')] : [];
  const heroPending = heroBlocks.filter(el => !seen.has(el));
  heroBlocks.forEach(el => seen.add(el));
  if (motion && !deep) heroPending.forEach((el, i) => rise(el, 80 + i * 80));

  // Later headings and paragraph groups enter once, as they are first reached.
  if ('IntersectionObserver' in window) {
    const rio = new IntersectionObserver(entries => {
      let k = 0;
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        rio.unobserve(e.target);
        if (seen.has(e.target)) return;
        seen.add(e.target);
        if (motion) rise(e.target, Math.min(k++, 3) * 90);
      });
    }, { rootMargin: '0px 0px 6% 0px' });
    document.querySelectorAll('[data-pf-reveal]').forEach(el => { if (!seen.has(el)) rio.observe(el); });
  }
})();
