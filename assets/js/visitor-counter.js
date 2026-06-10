(function () {
  var today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  var storageKey = 'blog_v_' + today;
  var ns = 'junhaing-blog';
  var base = 'https://api.countapi.xyz';

  function render(n) {
    var el = document.getElementById('today-visitor-count');
    if (el) el.textContent = (n > 0 ? n : 0).toLocaleString();
  }

  function fetchCount() {
    fetch(base + '/get/' + ns + '/' + today)
      .then(function (r) { return r.json(); })
      .then(function (d) { render(d.value); })
      .catch(function () {});
  }

  // 오래된 localStorage 키 정리 (7일 이상)
  try {
    Object.keys(localStorage)
      .filter(function (k) { return k.startsWith('blog_v_') && k !== storageKey; })
      .forEach(function (k) { localStorage.removeItem(k); });
  } catch (e) {}

  // 오늘 처음 방문이면 카운트 증가, 아니면 현재 수치만 조회
  var alreadyCounted = false;
  try { alreadyCounted = !!localStorage.getItem(storageKey); } catch (e) {}

  if (!alreadyCounted) {
    try { localStorage.setItem(storageKey, '1'); } catch (e) {}
    fetch(base + '/hit/' + ns + '/' + today)
      .then(function (r) { return r.json(); })
      .then(function (d) { render(d.value); })
      .catch(function () { fetchCount(); });
  } else {
    fetchCount();
  }
})();
