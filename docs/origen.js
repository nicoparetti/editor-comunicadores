// Recuerda de dónde llegó la persona (?origen=ig | yt) y lo pasa de página en página.
// También guarda la configuración del sitio.
window.CONFIG = {
  // Pega aquí la dirección del script de Google (termina en /exec). Ver docs/LEEME-formulario.md
  urlFormulario: "",
  // ID del video de YouTube de instalación (lo que va después de watch?v=). Vacío = muestra "en preparación".
  videoInstalacion: "",
  instagram: "nicoyestefi",
  youtube: "nicoyestefi",
  repo: "https://github.com/nicoparetti/editor-comunicadores"
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
