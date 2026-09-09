---
---
(function () {
  var code = "{{ site.goatcounter.code }}";
  if (!code) return;

  function render(n) {
    var el = document.getElementById('today-visitor-count');
    if (el) el.textContent = n;
  }

  fetch('https://' + code + '.goatcounter.com/counter/TOTAL.json')
    .then(function (r) { return r.json(); })
    .then(function (d) { render(d.count); })
    .catch(function () {});
})();
