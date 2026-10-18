/* Book: three steps in one panel (where and when -> choose your reset -> request sent), Uber Go style.
   No prices or bookings are real yet: prices show as "$ —" until RESET's pricing exists, and nothing is sent. */
(() => {
  const form = document.getElementById('go-form');
  const opts = document.getElementById('go-options');
  const done = document.getElementById('go-done');
  const error = form.querySelector('.go-error');
  const confirmBtn = opts.querySelector('[data-confirm]');
  let rhythm = 'Once';

  const show = (el) => {
    [form, opts, done].forEach((x) => { x.hidden = x !== el; });
    const target = el.querySelector('h1') || el;
    if (el === done) done.focus(); else target.setAttribute('tabindex', '-1'), target.focus({ preventScroll: true });
  };

  form.querySelectorAll('.go-pill').forEach((p) => p.addEventListener('click', () => {
    form.querySelectorAll('.go-pill').forEach((x) => x.setAttribute('aria-pressed', String(x === p)));
    rhythm = p.dataset.rhythm;
  }));
  if (location.hash === '#recurring') form.querySelector('[data-rhythm="Every week"]').click();

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const address = form.elements.address.value.trim();
    const size = form.elements.size.value;
    if (!address || !size) {
      error.textContent = !address ? 'Enter your address to see prices.' : 'Choose your home size to see prices.';
      error.hidden = false;
      (!address ? form.elements.address : form.elements.size).focus();
      return;
    }
    error.hidden = true;
    opts.querySelector('[data-summary]').textContent = `${size} · ${address} · ${form.elements.when.value} · ${rhythm}`;
    show(opts);
  });

  opts.querySelectorAll('.go-opt').forEach((o) => o.addEventListener('click', () => {
    opts.querySelectorAll('.go-opt').forEach((x) => x.setAttribute('aria-checked', String(x === o)));
    confirmBtn.textContent = `Book ${o.dataset.name}`;
  }));
  // arrow keys move through the options, as a radio group should
  opts.querySelector('.go-opts').addEventListener('keydown', (e) => {
    if (!['ArrowDown', 'ArrowUp'].includes(e.key)) return;
    const list = [...opts.querySelectorAll('.go-opt')];
    const i = list.indexOf(document.activeElement);
    const next = list[(i + (e.key === 'ArrowDown' ? 1 : list.length - 1)) % list.length];
    next.focus(); next.click(); e.preventDefault();
  });

  opts.querySelector('[data-back]').addEventListener('click', () => show(form));
  confirmBtn.addEventListener('click', () => {
    const name = opts.querySelector('.go-opt[aria-checked="true"]').dataset.name;
    done.querySelector('[data-done-text]').textContent =
      `Your ${name} request is in for ${form.elements.when.value.toLowerCase()}. We'll confirm your RESET member and time in the RESET app.`;
    show(done);
  });
  done.querySelector('[data-again]').addEventListener('click', () => { form.reset(); show(form); });
})();
