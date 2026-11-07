// studentnoname portfolio — mobile navigation, language hash preservation,
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

  // Motion preference: follows the system reduced-motion setting unless the visitor explicitly opts in on this site.
  const KEY = 'pf-panel-motion';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  let pref = null;
  try { pref = localStorage.getItem(KEY); } catch {}
  // Explicit preview link (?motion=on): opts in once, then the parameter is consumed.
  try {
    const url = new URL(location.href);
    if (url.searchParams.get('motion') === 'on') {
      pref = 'on';
      try { localStorage.setItem(KEY, pref); } catch {}
      url.searchParams.delete('motion');
      history.replaceState(history.state, '', url);
    }
  } catch {}
  const wanted = () => pref === 'on' || (!reduce.matches && pref !== 'off');
  let motion = false;

  // Text entrance: finite WAAPI rises; content stays visible when scripts or WAAPI are unavailable.
  const canAnimate = typeof Element.prototype.animate === 'function';
  const anims = new Map();
  const seen = new WeakSet();

  const rise = (el, delay, duration = 640, dist = 20) => {
    if (!canAnimate) return;
    const prev = anims.get(el);
    if (prev) prev.cancel();
    const a = el.animate(
      [{ opacity: 0, transform: `translateY(${dist}px)` }, { opacity: 1, transform: 'none' }],
      { duration, delay, easing: 'cubic-bezier(.18, .72, .2, 1)', fill: 'backwards' }
    );
    const done = () => { if (anims.get(el) === a) anims.delete(el); };
    a.addEventListener('finish', done);
    a.addEventListener('cancel', done);
    anims.set(el, a);
  };

  const settle = scope => anims.forEach((a, el) => {
    if (scope.contains(el) || el.contains(scope)) a.finish();
  });

  // Liquid follow-through state: `sy` trails scrollY briefly after native scrolling. A snap makes the next
  // renders use the actual scroll so jumps (anchors, focus, resize, restore) never replay a fake scroll.
  let sy = null;
  let snapUntil = 0;
  let moved = 0;
  let tPrev = 0;
  function snap() { sy = null; snapUntil = performance.now() + 150; }

  // Deep-link and in-page jump destinations are shown at once, never left waiting on an entrance.
  const reach = el => {
    snap();
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
  const introDeep = !!deep && deep.id === 'intro';
  if (deep && !introDeep) reach(deep);

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

  // Single broad liquid swell in objectBoundingBox units: the crest leads at the top, the sides trail by up to `a`.
  const edge = (a, p) => {
    const s = Math.sin(p * Math.PI);
    const cx = 0.42 + 0.16 * p;
    const yl = a * (0.8 + 0.2 * s), yr = a * (1 - 0.25 * s);
    const f = v => v.toFixed(5);
    return `M0 ${f(yl)}C${f(cx * 0.45)} ${f(yl)} ${f(cx * 0.55)} 0 ${f(cx)} 0` +
      `S${f(1 - (1 - cx) * 0.45)} ${f(yr)} 1 ${f(yr)}V1H0Z`;
  };

  const resetShown = () => {
    shown = panels.map(() => ({ p: -1, clip: false, under: -1, drift: 0, op: 1 }));
  };
  const setFlow = v => { if (root.dataset.pfFlow !== v) root.dataset.pfFlow = v; };

  // Cover progress of each incoming panel at scroll `y`: 0 when the previous one starts holding, 1 when it is fully covered.
  const progressAt = y => layout.tops.map((top, j) => {
    if (!j) return 1;
    const v = layout.overs[j - 1];
    return v > 0 ? clamp((layout.hh + v - (top - y)) / v) : 1;
  });

  function render() {
    sraf = 0;
    if (!layout) return;
    const { hh, hs, tops, overs, amp, lag } = layout;
    const y = scrollY;
    const now = performance.now();
    const dt = Math.min(34, Math.max(0, now - tPrev));
    tPrev = now;

    // Actual progress drives state, opacity and the held panel; only drift and curve read the trailing value.
    const prog = progressAt(y);
    const live = prog.some(p => p > 0 && p < 1);
    if (sy === null || now < snapUntil || document.hidden || !motion) sy = y;
    else sy += (y - sy) * (1 - Math.exp(-dt / 60));
    if (!live || now - moved > 320 || Math.abs(y - sy) < 0.25) sy = y;
    const settling = sy !== y;
    const lagPx = Math.max(-lag, Math.min(lag, y - sy));
    const trail = settling ? progressAt(sy) : prog;

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
      // Follow-through lag, tapered to exactly 0 at both ends so a held or idle panel never moves.
      const drift = active ? Math.round(lagPx * clamp(p / 0.08) * clamp((1 - p) / 0.2) * 100) / 100 : 0;
      if (drift !== s.drift) {
        if (drift) panel.style.setProperty('--pf-drift', drift + 'px');
        else panel.style.removeProperty('--pf-drift');
        s.drift = drift;
      }
      // Briefly translucent while covering, fully opaque by 75% cover.
      const e = clamp(p / 0.75);
      const op = active ? Math.round((0.88 + 0.12 * e * e * (3 - 2 * e)) * 1000) / 1000 : 1;
      if (op !== s.op) {
        if (op < 1) panel.style.setProperty('--pf-opacity', String(op));
        else panel.style.removeProperty('--pf-opacity');
        s.op = op;
      }
      const clip = active && !!paths[j];
      if (clip) {
        // Never deeper than the visible overlap, so the dip always shows the older panel beneath.
        const t = trail[j];
        const a = Math.min(amp * Math.sin((1 - t) * Math.PI / 2), Math.max(0, p * overs[j - 1] - drift));
        paths[j].setAttribute('d', edge(a / hs[j], t));
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

    // Keep settling only while a real overlap is visible and the trailing value still differs.
    setFlow(settling ? 'settling' : 'idle');
    if (settling && motion && !document.hidden) sraf = requestAnimationFrame(render);
  }

  function unlayer() {
    layout = null;
    if (sraf) { cancelAnimationFrame(sraf); sraf = 0; }
    snap();
    setFlow('idle');
    root.style.removeProperty('--pf-hh');
    tracks.forEach(t => {
      t.removeAttribute('data-pf-ready');
      t.style.removeProperty('--pf-h');
      t.style.removeProperty('--pf-z');
    });
    panels.forEach(panel => {
      panel.style.clipPath = '';
      panel.style.removeProperty('--pf-under');
      panel.style.removeProperty('--pf-drift');
      panel.style.removeProperty('--pf-opacity');
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
    layout = { hh, hs, tops, overs, amp: narrow.matches ? 36 : 64, lag: narrow.matches ? 14 : 24 };

    // After a width change, keep the section being read at the same relative point.
    if (resized && anchor && anchor.i < n) {
      snap();
      const target = tops[anchor.i] + anchor.ratio * hs[anchor.i] - hh;
      if (Math.abs(target - y) > 2) scrollTo(0, target);
    }
    resized = false;
    // Height-only re-measures keep an ongoing settle (sy is a scroll value, unaffected by the new layout).
    if (sraf) { cancelAnimationFrame(sraf); sraf = 0; }
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
    snap();
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

  // Hero entrance: heading lines and intro arrive one by one. The focused element is never replayed.
  const heroBlocks = n ? [...tracks[0].querySelectorAll('[data-pf-reveal]')] : [];
  const heroEntrance = blocks => {
    const focus = document.activeElement;
    blocks.filter(el => !(focus && el.contains(focus)))
      .forEach((el, i) => rise(el, 80 + i * 120, 900, 32));
  };
  const nearTop = () => !!n && scrollY <= innerHeight * 0.25 &&
    tracks[0].getBoundingClientRect().bottom > headerHeight();

  // Motion controls (hero and footer), kept in sync.
  const toggles = [...document.querySelectorAll('[data-pf-motion-toggle]')];
  const statuses = [...document.querySelectorAll('[data-pf-motion-status]')];

  const sync = () => {
    toggles.forEach(t => {
      const control = t.closest('[data-pf-motion-control]');
      if (control) control.hidden = false;
      t.setAttribute('aria-pressed', String(motion));
      const label = motion ? t.dataset.enabledAction : t.dataset.disabledAction;
      if (label) t.textContent = label;
    });
    statuses.forEach(s => {
      const d = s.dataset;
      s.textContent = reduce.matches && pref === null ? d.reducedLabel
        : reduce.matches && motion ? d.chosenLabel
        : motion ? d.enabledLabel : d.disabledLabel;
    });
  };

  const apply = initial => {
    const on = wanted();
    if (initial || on !== motion) {
      const keep = !initial && canLayer ? capture() : null;
      motion = on;
      root.dataset.pfMotion = on ? 'on' : 'off';
      snap();
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

  toggles.forEach(t => t.addEventListener('click', () => {
    pref = motion ? 'off' : 'on';
    try { localStorage.setItem(KEY, pref); } catch {}
    apply(false);
    if (motion && nearTop()) heroEntrance(heroBlocks);
  }));

  // A live system change drops any site-level override and follows the system again.
  const onSystem = () => {
    pref = null;
    try { localStorage.removeItem(KEY); } catch {}
    apply(false);
  };
  if (reduce.addEventListener) reduce.addEventListener('change', onSystem);
  else if (reduce.addListener) reduce.addListener(onSystem);

  addEventListener('scroll', () => { moved = performance.now(); queueRender(); }, { passive: true });
  addEventListener('resize', () => {
    if (innerWidth !== width) { width = innerWidth; resized = true; snap(); }
    if (motion) queueMeasure();
  }, { passive: true });

  // Hidden tabs and restored pages land on the actual position; the next render clears any drift.
  document.addEventListener('visibilitychange', () => {
    if (sraf) { cancelAnimationFrame(sraf); sraf = 0; }
    snap();
    if (!document.hidden) queueRender();
  });
  addEventListener('pageshow', () => { snap(); queueRender(); });

  setFlow('idle');
  apply(true);

  // First entry plays the hero entrance, except on deep links.
  const heroPending = heroBlocks.filter(el => !seen.has(el));
  heroBlocks.forEach(el => seen.add(el));
  if (motion && (!deep || introDeep)) heroEntrance(heroPending);

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
