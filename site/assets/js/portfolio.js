/*
 * Portfolio interactions: collapsible mobile menu, current-section tracking,
 * language links that keep the section hash, and the motion pause control.
 * Everything here is progressive enhancement: anchors and content work without it.
 * Loaded in <head> (not deferred) so the html classes exist before first paint.
 */
(() => {
  const root = document.documentElement;
  const MOTION_KEY = "pf-motion";
  const reduceQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  const desktopQuery = window.matchMedia("(min-width: 60em)");

  const readMotion = () => {
    try {
      return localStorage.getItem(MOTION_KEY);
    } catch {
      return null;
    }
  };

  const onQueryChange = (query, handler) => {
    if (query.addEventListener) query.addEventListener("change", handler);
    else if (query.addListener) query.addListener(handler);
  };

  // Before first paint: enable JS-only styles and pick the initial motion state.
  root.classList.add("pf-js");
  const storedMotion = readMotion();
  root.dataset.pfMotion = storedMotion || (reduceQuery.matches ? "off" : "on");

  const initMenu = () => {
    const nav = document.querySelector("[data-pf-nav]");
    const toggle = nav && nav.querySelector("[data-pf-nav-toggle]");
    const list = toggle && document.getElementById(toggle.getAttribute("aria-controls"));
    if (!nav || !toggle || !list) return;

    const isOpen = () => toggle.getAttribute("aria-expanded") === "true";
    const setOpen = (open, restoreFocus = false) => {
      toggle.setAttribute("aria-expanded", String(open));
      nav.toggleAttribute("data-open", open);
      if (!open && restoreFocus) toggle.focus();
    };

    toggle.addEventListener("click", () => setOpen(!isOpen()));

    // Selecting a menu item closes the menu; the native anchor handles navigation.
    list.addEventListener("click", (event) => {
      if (event.target.closest("a")) setOpen(false);
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && isOpen()) setOpen(false, true);
    });

    document.addEventListener("click", (event) => {
      if (isOpen() && !nav.contains(event.target)) setOpen(false);
    });

    nav.addEventListener("focusout", (event) => {
      if (isOpen() && event.relatedTarget && !nav.contains(event.relatedTarget)) setOpen(false);
    });

    // Returning to desktop width resets the collapsed state.
    onQueryChange(desktopQuery, () => setOpen(false));
  };

  const initSections = () => {
    const sections = Array.from(document.querySelectorAll("[data-pf-section]"));
    const ids = new Set(sections.map((section) => section.id));
    const navLinks = Array.from(document.querySelectorAll("[data-pf-nav-link]"));
    const langLinks = Array.from(document.querySelectorAll("[data-pf-lang]"));
    let current = "";

    const hashFor = () => {
      const fromUrl = decodeURIComponent(window.location.hash.slice(1));
      const id = current || fromUrl;
      return ids.has(id) ? `#${id}` : "";
    };

    // Language pages share section ids, so the other language opens at the same section.
    const updateLangLinks = () => {
      const hash = hashFor();
      langLinks.forEach((link) => {
        const base = link.getAttribute("href").split("#")[0];
        link.setAttribute("href", base + hash);
      });
    };

    const setCurrent = (id) => {
      current = id;
      navLinks.forEach((link) => {
        if (link.hash === `#${id}`) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      });
      updateLangLinks();
    };

    langLinks.forEach((link) => {
      link.addEventListener("click", updateLangLinks);
      link.addEventListener("focus", updateLangLinks);
    });
    window.addEventListener("hashchange", updateLangLinks);
    updateLangLinks();

    if (!sections.length || !("IntersectionObserver" in window)) return;
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) setCurrent(entry.target.id);
        });
      },
      { rootMargin: "-40% 0px -55% 0px" },
    );
    sections.forEach((section) => observer.observe(section));
  };

  const initMotion = () => {
    const button = document.querySelector("[data-pf-motion-toggle]");
    const apply = (on) => {
      root.dataset.pfMotion = on ? "on" : "off";
      if (button) button.setAttribute("aria-pressed", String(!on));
    };

    apply(root.dataset.pfMotion === "on");

    // Without a saved choice, follow the system reduced-motion setting.
    onQueryChange(reduceQuery, () => {
      if (!readMotion()) apply(!reduceQuery.matches);
    });

    if (!button) return;
    button.hidden = false;
    button.addEventListener("click", () => {
      const on = root.dataset.pfMotion !== "on";
      apply(on);
      try {
        localStorage.setItem(MOTION_KEY, on ? "on" : "off");
      } catch {
        // Storage may be unavailable; the choice still applies to this page view.
      }
    });
  };

  const init = () => {
    initMenu();
    initSections();
    initMotion();
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
