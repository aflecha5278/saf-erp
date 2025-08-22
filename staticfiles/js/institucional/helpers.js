document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.input-mayuscula').forEach(el => {
    el.addEventListener('input', () => {
      const pos = el.selectionStart;
      el.value = el.value.toUpperCase();
      el.setSelectionRange(pos, pos);
    });
  });
});

