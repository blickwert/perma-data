/* Nur Vorschau: Formulare senden nichts, sie zeigen nach gültiger Eingabe die Bestätigung an. */
document.querySelectorAll('[data-preview-form]').forEach(function (form) {
  var group = form.querySelector('[data-require-one]');
  var boxes = group ? group.querySelectorAll('input[type=checkbox]') : [];
  function checkGroup() {
    if (!boxes.length) return;
    var any = Array.prototype.some.call(boxes, function (b) { return b.checked; });
    boxes[0].setCustomValidity(any ? '' : 'Bitte wähle mindestens eine Ausbildung aus.');
  }
  Array.prototype.forEach.call(boxes, function (b) { b.addEventListener('change', checkGroup); });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    checkGroup();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    form.querySelector('.bw-form__thanks').hidden = false;
    form.querySelector('button[type=submit]').disabled = true;
  });
});
