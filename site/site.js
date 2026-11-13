(function () {
  var root = document.documentElement;
  var btn = document.getElementById('theme');
  var frames = Array.prototype.slice.call(document.querySelectorAll('.embed iframe'));

  function fit(f) {
    try {
      var d = f.contentDocument;
      if (d && d.body) f.style.height = Math.ceil(d.documentElement.scrollHeight) + 'px';
    } catch (e) {}
  }
  function paint() {
    var dark = root.dataset.theme === 'dark';
    btn.querySelector('.tl').textContent = dark ? 'Light' : 'Salon Black';
    btn.setAttribute('aria-label', 'Switch to the ' + (dark ? 'Light' : 'Salon Black') + ' theme');
    frames.forEach(function (f) {
      try { f.contentDocument.documentElement.dataset.theme = root.dataset.theme; } catch (e) {}
    });
  }
  btn.addEventListener('click', function () {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('chi-theme', root.dataset.theme); } catch (e) {}
    paint();
  });
  frames.forEach(function (f) {
    f.addEventListener('load', function () { paint(); fit(f); setTimeout(function () { fit(f); }, 400); });
    if (f.contentDocument && f.contentDocument.readyState === 'complete') fit(f);
  });
  window.addEventListener('resize', function () { frames.forEach(fit); });
  paint();

  // keep the current section visible in the horizontal nav on phones
  var cur = document.querySelector('.side a[aria-current]');
  if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: 'nearest', inline: 'center' });

  var toast = document.getElementById('toast'), timer;
  function say(msg) {
    toast.textContent = msg; toast.hidden = false;
    clearTimeout(timer); timer = setTimeout(function () { toast.hidden = true; }, 1600);
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('[data-copy]') : null;
    if (!b) return;
    var v = b.getAttribute('data-copy');
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(v).then(function () { say('Copied ' + v); }, function () { say(v); });
    } else { say(v); }
  });
})();
