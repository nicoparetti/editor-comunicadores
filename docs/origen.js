// Recuerda de dónde llegó la persona (?origen=ig | yt) y lo pasa de página en página.
// También guarda la configuración del sitio.
window.CONFIG = {
  // Pega aquí la dirección del script de Google (termina en /exec). Ver docs/LEEME-formulario.md
  urlFormulario: "https://formulario-editor.nicolas-paretti.workers.dev/",
  // ID del video de YouTube de instalación (lo que va después de watch?v=). Vacío = muestra "en preparación".
  videoInstalacion: "",
  instagram: "nicoyestefi",
  youtube: "nicoyestefi",
  repo: "https://github.com/nicoparetti/editor-gente-comun"
};

(function () {
  var p = new URLSearchParams(location.search).get("origen");
  var o = null;
  try {
    if (p) sessionStorage.setItem("origen", p);
    o = p || sessionStorage.getItem("origen");
  } catch (e) { o = p; }
  window.ORIGEN = o || "directo";
  if (o) {
    document.querySelectorAll("a.ir-formulario").forEach(function (a) {
      a.href = "formulario.html?origen=" + encodeURIComponent(o);
    });
  }
})();

// Aparecer al bajar y puntos del carrusel de formatos
document.addEventListener("DOMContentLoaded", function () {
  var sel = ".tipos-cabeza,.tipo,.sin-codigo,.criterios h2,.aviso,.pieza,.adapta,.hub>div,.ventana,.cta-final,.paso";
  var els = document.querySelectorAll(sel);
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("visible"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    els.forEach(function (el) { el.classList.add("aparece"); io.observe(el); });
  }
  var carril = document.querySelector(".tipos-carril"), puntos = document.querySelectorAll(".carril-puntos i");
  if (carril && puntos.length) {
    var marcar = function () {
      var hijos = carril.children, centro = carril.scrollLeft + carril.clientWidth / 2, mejor = 0, dist = 1e9;
      for (var i = 0; i < hijos.length; i++) {
        var c = hijos[i].offsetLeft + hijos[i].offsetWidth / 2, d = Math.abs(c - centro);
        if (d < dist) { dist = d; mejor = i; }
      }
      puntos.forEach(function (p, i) { p.classList.toggle("on", i === mejor); });
    };
    carril.addEventListener("scroll", marcar, { passive: true }); marcar();
  }
});

// Botón fijo en celular: aparece al pasar el hero y se esconde en el cierre
document.addEventListener("DOMContentLoaded", function () {
  var barra = document.querySelector(".barra-movil"), hero = document.querySelector(".hero"), cierre = document.querySelector(".cierre");
  if (!barra || !hero || !("IntersectionObserver" in window)) return;
  var heroVisible = true, cierreVisible = false;
  var act = function () { barra.classList.toggle("visible", !heroVisible && !cierreVisible); };
  new IntersectionObserver(function (e) { heroVisible = e[0].isIntersecting; act(); }).observe(hero);
  if (cierre) new IntersectionObserver(function (e) { cierreVisible = e[0].isIntersecting; act(); }).observe(cierre);
});
