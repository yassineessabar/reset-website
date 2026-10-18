/* Earn: application form. Validates in the browser and shows a confirmation.
   Nothing is sent anywhere yet: connect the submit handler to RESET's backend when it exists. */
(() => {
  const form = document.getElementById('apply-form');
  if (!form) return;
  const done = document.getElementById('apply-done');
  const error = form.querySelector('.rs-form-error');

  const messages = {
    first: 'Enter your first name.',
    last: 'Enter your last name.',
    email: 'Enter an email address like name@example.com.',
    mobile: 'Enter your mobile number.',
    suburb: 'Enter the suburb you live in.',
    experience: 'Choose your cleaning experience.',
    rights: 'Confirm you have the right to work in Australia.',
    checks: 'Agree to the ID and background check to continue.',
  };

  form.addEventListener('input', (e) => {
    if (e.target.closest('.rs-field, .rs-check')) e.target.closest('.rs-field, .rs-check').classList.remove('is-invalid');
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const invalid = [...form.elements].filter((el) => el.name && el.required && !el.checkValidity());
    form.querySelectorAll('.is-invalid').forEach((el) => el.classList.remove('is-invalid'));
    if (invalid.length) {
      invalid.forEach((el) => el.closest('.rs-field, .rs-check')?.classList.add('is-invalid'));
      error.textContent = messages[invalid[0].name] || 'Check the highlighted fields.';
      error.hidden = false;
      invalid[0].focus();
      return;
    }
    error.hidden = true;
    done.querySelector('[data-first]').textContent = form.elements.first.value.trim() || 'there';
    form.hidden = true;
    done.hidden = false;
    done.focus();
  });
})();
