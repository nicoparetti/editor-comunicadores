/**
 * @OnlyCurrentDoc
 * Recibe los datos del formulario de la página y los guarda en esta Hoja de Google.
 * Solo pide permiso sobre ESTA hoja (nada de correo ni de otros archivos).
 */
function doPost(e) {
  var p = e.parameter;
  var hoja = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (hoja.getLastRow() === 0) {
    hoja.appendRow(["Fecha", "Nombre y apellido", "Correo", "Celular", "País", "Origen"]);
  }
  hoja.appendRow([new Date(), p.nombre, p.email, p.telefono, p.pais, p.origen]);
  return ContentService.createTextOutput("ok");
}
