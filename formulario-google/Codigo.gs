// Recibe los datos del formulario de la página y los guarda en esta Hoja de Google.
// También envía un correo de bienvenida con el enlace de instalación.
var URL_INSTALAR = "https://nicoparetti.github.io/editor-comunicadores/instalar.html";

function doPost(e) {
  var p = e.parameter;
  var hoja = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (hoja.getLastRow() === 0) {
    hoja.appendRow(["Fecha", "Nombre y apellido", "Correo", "Celular", "País", "Origen"]);
  }
  hoja.appendRow([new Date(), p.nombre, p.email, p.telefono, p.pais, p.origen]);
  try {
    var nombre = (p.nombre || "").split(" ")[0];
    MailApp.sendEmail({
      to: p.email,
      name: "Nicolás Paretti",
      subject: "Tu herramienta de edición con IA 🎬",
      htmlBody:
        "<p>¡Hola, " + nombre + "!</p>" +
        "<p>Gracias por sumarte. Acá tienes el paso a paso para instalar la herramienta:</p>" +
        '<p><a href="' + URL_INSTALAR + '">' + URL_INSTALAR + "</a></p>" +
        "<p>Cualquier duda, escríbeme por Instagram a @nicoyestefi.</p>" +
        "<p>Bendiciones,<br>Nico</p>"
    });
  } catch (err) {}
  return ContentService.createTextOutput("ok");
}
