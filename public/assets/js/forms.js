/* Generic RESET forms (gift cards, partners). A form with data-rs-form="<done panel id>" validates
   required fields in the browser, shows a clear message for the first problem, then swaps to its
   confirmation panel. Nothing is sent anywhere yet: connect to a backend before launch.
   Messages come from each field's data-msg attribute. */
(() => {
  document.querySelectorAll('form[data-rs-form]').forEach((form) => {
    const done = document.getElementById(form.dataset.rsForm);
    const error = form.querySelector('.rs-form-error');
    const host = form.closest('.rs-apply-card');

    form.addEventListener('input', (e) => e.target.closest('.rs-field, .rs-check')?.classList.remove('is-invalid'));

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      form.querySelectorAll('.is-invalid').forEach((el) => el.classList.remove('is-invalid'));
      const invalid = [...form.elements].filter((el) => el.name && el.willValidate && !el.checkValidity());
      if (invalid.length) {
        invalid.forEach((el) => el.closest('.rs-field, .rs-check')?.classList.add('is-invalid'));
        error.textContent = invalid[0].dataset.msg || 'Check the highlighted fields.';
        error.hidden = false;
        invalid[0].focus();
        return;
      }
      error.hidden = true;
      done.querySelectorAll('[data-fill]').forEach((el) => {
        const v = form.elements[el.dataset.fill]?.value?.trim();
        if (v) el.textContent = v;
      });
      form.hidden = true;
      done.hidden = false;
      host?.classList.add('is-done');
      done.focus();
    });
  });

  /* Gift card: live preview of amount, recipient and message */
  const gift = document.getElementById('gift-form');
  if (gift) {
    const card = document.querySelector('.rs-giftcard');
    const custom = gift.elements.custom;
    const amountOut = card.querySelector('[data-amount]');
    const toOut = card.querySelector('[data-to]');
    const update = () => {
      const picked = gift.querySelector('input[name="amount"]:checked');
      let amount = picked ? picked.value : '';
      custom.closest('.rs-field').hidden = amount !== 'custom';
      custom.required = amount === 'custom';
      if (amount === 'custom') amount = custom.value ? String(Math.round(+custom.value)) : '';
      amountOut.textContent = amount ? `$${amount}` : '$—';
      gift.elements.total.value = amount;
      toOut.textContent = gift.elements.to_name.value.trim() ? `For ${gift.elements.to_name.value.trim()}` : 'For someone who deserves a break';
    };
    gift.addEventListener('input', update);
    gift.addEventListener('change', update);
    update();
  }
})();
