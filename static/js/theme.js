(function () {
  var root = document.documentElement;
  var btn = document.getElementById('theme-toggle');
  if (!btn) return;

  function currentResolved() {
    var attr = root.getAttribute('data-theme');
    if (attr === 'light' || attr === 'dark') return attr;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function apply(mode) {
    root.setAttribute('data-theme', mode);
    try { localStorage.setItem('theme', mode); } catch (e) {}
    btn.setAttribute('aria-pressed', mode === 'dark' ? 'true' : 'false');
  }

  btn.addEventListener('click', function () {
    var next = currentResolved() === 'dark' ? 'light' : 'dark';
    apply(next);
  });

  btn.setAttribute('aria-pressed', currentResolved() === 'dark' ? 'true' : 'false');
})();
