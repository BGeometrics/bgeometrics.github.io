/*
 * Selector Claro/Oscuro de las paginas en espanol: lleva a la misma pagina en el otro tema
 * (pagina.html <-> pagina_dark.html) en vez de a la portada.
 * Los enlaces se marcan con data-theme-link="light|dark" en tools/es/web-generation-model.html;
 * su href (portada) queda como respaldo si la variante no existe o no hay JS.
 */
(function () {
  function setup() {
    var links = document.querySelectorAll('a[data-theme-link]');
    if (!links.length) return;

    var file = window.location.pathname.split('/').pop() || 'index.html';
    if (!/\.html$/.test(file)) return;

    var light = file.replace(/_dark\.html$/, '.html');
    var dark = light.replace(/\.html$/, '_dark.html');
    var query = window.location.search + window.location.hash;

    links.forEach(function (a) {
      var target = (a.getAttribute('data-theme-link') === 'dark' ? dark : light);
      if (target === file) {
        a.setAttribute('href', target + query);
        return;
      }
      var fallback = a.getAttribute('href');
      a.setAttribute('href', target + query);
      a.addEventListener('click', function (e) {
        e.preventDefault();
        fetch(target, { method: 'HEAD' })
          .then(function (r) { window.location.href = r.ok ? target + query : fallback; })
          .catch(function () { window.location.href = target + query; });
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setup);
  } else {
    setup();
  }
})();
