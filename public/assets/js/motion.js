/* RESET motion layer. The page is fully visible without this file; it only adds:
   1. the hero wipe: a sky blade clears the collage from hazy to crisp, then the checks tick off
   2. the drip pattern growing in when it scrolls into view
   3. photographic wipe reveals on the big images
   4. working carousels (Uber drove them with its own JS) */
(() => {
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  root.classList.add('rs-js');
  if (reduce) root.classList.add('rs-reduce');

  const visible = (el) => {
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== 'hidden';
  };

  /* ---------- 1. hero wipe ---------- */
  const collage = [...document.querySelectorAll('img[src*="hero-collage"]')]
    .map((img) => img.closest('picture').parentElement);
  collage.forEach((box) => {
    box.classList.add('rs-collage');
    if (reduce) { box.classList.add('is-clean'); return; }
    const haze = document.createElement('div');
    haze.className = 'rs-haze';
    const blade = document.createElement('div');
    blade.className = 'rs-blade';
    box.append(haze, blade);
    // start just after the hazy state paints; a timer (not rAF) so a background tab still gets going
    setTimeout(() => box.classList.add('is-wiping'), 60);
    blade.addEventListener('animationend', () => box.classList.add('is-clean'), { once: true });
    // never leave the collage hazy, whatever the browser does with animations
    setTimeout(() => box.classList.add('is-clean'), 2600);
  });

  /* Typed headline, as on the RESET site (localhost:3002): "Home," stays, the last word types,
     holds and swaps. ~100ms per letter each way, ~1.4s hold. Reduced motion keeps "Home, sorted." */
  const TYPE_MS = 100, HOLD_MS = 1400, ENDINGS = ['sorted.', 'done.', 'reset.'];
  document.querySelectorAll('[data-rs-headline]').forEach((h) => {
    const full = h.textContent.trim();
    const m = full.match(/^(.*\s)(\S+)$/);
    if (!m) return;
    // full text for screen readers and crawlers; the typed version is visual only
    h.innerHTML = `<span class="rs-vh">${full}</span><span aria-hidden="true">${m[1]}<span class="rs-typed">${m[2]}</span></span>`;
    if (reduce) return;
    const out = h.querySelector('.rs-typed');
    let i = 0, len = ENDINGS[0].length, deleting = false;
    const tick = () => {
      const word = ENDINGS[i];
      let wait = TYPE_MS;
      if (!deleting && len === word.length) { deleting = true; wait = HOLD_MS; }
      else if (deleting && len === 0) { deleting = false; i = (i + 1) % ENDINGS.length; }
      else len += deleting ? -1 : 1;
      // a zero-width space keeps the line height when every letter is deleted
      out.textContent = ENDINGS[i].slice(0, len) || '\u200b';
      setTimeout(tick, wait);
    };
    tick();   // shows the full first word, then holds
  });

  /* ---------- 2 + 3. in-view triggers ---------- */
  const reveal = [
    ...document.querySelectorAll('.rs-drip'),
    ...[...document.querySelectorAll('img')].filter((img) =>
      /step-|more-|member|earn-|business|banner-|card-|city-guide/.test(img.getAttribute('src') || '')),
  ];
  reveal.forEach((el) => {
    if (el.tagName === 'IMG') {
      el.classList.add('rs-photo');
      // the wipe lives on the image's frame so the crop stays put
      el.parentElement.classList.add('rs-frame');
    }
  });
  if (reduce || !('IntersectionObserver' in window)) {
    reveal.forEach((el) => el.classList.add('is-in'));
  } else {
    // Images start clipped to nothing, and a clipped element never "intersects", so watch their frame.
    const watched = new Map(reveal.map((el) => [el.tagName === 'IMG' ? el.parentElement : el, el]));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { watched.get(e.target).classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
    watched.forEach((_, target) => io.observe(target));
  }

  /* ---------- 4. carousels ---------- */
  document.querySelectorAll('[aria-roledescription="carousel"]').forEach((car) => {
    const track = car.querySelector('ul');
    if (!track) return;
    const block = car.closest('[data-testid="block-container"]') || car.parentElement.parentElement;
    const navs = [...block.querySelectorAll('nav[aria-label="Gallery controls"]')];
    if (!navs.length) return;
    let index = 0;
    const metrics = () => {
      const items = [...track.children];
      const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      const step = items[0].getBoundingClientRect().width + gap;
      const perView = Math.max(1, Math.round((car.getBoundingClientRect().width + gap) / step));
      return { step, max: Math.max(0, items.length - perView), pages: Math.max(1, items.length - perView + 1) };
    };
    const render = () => {
      const { step, max, pages } = metrics();
      index = Math.min(index, max);
      track.style.transform = `translateX(${-index * step}px)`;
      navs.forEach((nav) => {
        const status = nav.querySelector('[role="status"]');
        if (status) status.textContent = `${index + 1}/${pages}`;
        const prev = nav.querySelector('[data-testid="pagination-prev"]');
        const next = nav.querySelector('[data-testid="pagination-next"]');
        if (prev) prev.disabled = index === 0;
        if (next) next.disabled = index >= max;
      });
    };
    track.classList.add('rs-track');
    navs.forEach((nav) => {
      nav.querySelectorAll('button').forEach((b) => b.setAttribute('type', 'button'));
      nav.querySelector('[data-testid="pagination-prev"]')?.addEventListener('click', () => { index = Math.max(0, index - 1); render(); });
      nav.querySelector('[data-testid="pagination-next"]')?.addEventListener('click', () => { index += 1; render(); });
    });
    addEventListener('resize', render, { passive: true });
    render();
  });
})();
