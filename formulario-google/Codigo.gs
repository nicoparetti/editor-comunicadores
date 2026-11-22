/**
 * @OnlyCurrentDoc
 * Recibe los datos del formulario de la página:
 *  1. Los guarda en esta Hoja de Google.
 *  2. Suma a la persona a la lista "Editor para gente común" de Brevo.
 *  3. Le envía el correo de bienvenida desde hola@nicoyestefi.com.
 *
 * La clave de Brevo NO va en el código. Se guarda en:
 * Configuración del proyecto (engranaje) > Propiedades de la secuencia de comandos
 *   Propiedad: BREVO_API_KEY   Valor: la clave que empieza con xkeysib-
 */

var LISTA_BREVO = 3; // Lista "Editor para gente común"
var REMITENTE = { name: "Nico y Estefi", email: "hola@nicoyestefi.com" };
var PAGINA_INSTALAR = "https://editor.nicoyestefi.com/instalar.html";
var CANAL_YOUTUBE = "https://www.youtube.com/@nicoyestefi";

function doPost(e) {
  var p = e.parameter;
  var hoja = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (hoja.getLastRow() === 0) {
    hoja.appendRow(["Fecha", "Nombre y apellido", "Correo", "Celular", "País", "Origen", "Brevo"]);
  }

  var estado = "";
  try {
    var limpio = function (v) { return String(v || "").replace(/^'/, "").trim(); };
    var nombre = limpio(p.nombre);
    var email = limpio(p.email).toLowerCase();
    var partes = nombre.split(/\s+/);
    var pila = partes.shift() || "";
    estado = enviarABrevo(email, pila, partes.join(" "), limpio(p.origen));
  } catch (err) {
    estado = "error: " + err;
  }

  hoja.appendRow([new Date(), p.nombre, p.email, p.telefono, p.pais, p.origen, estado]);
  return ContentService.createTextOutput("ok");
}

function enviarABrevo(email, pila, apellido, origen) {
  var clave = PropertiesService.getScriptProperties().getProperty("BREVO_API_KEY");
  if (!clave) return "sin clave";

  var pedir = function (ruta, cuerpo) {
    return UrlFetchApp.fetch("https://api.brevo.com/v3" + ruta, {
      method: "post",
      contentType: "application/json",
      headers: { "api-key": clave, accept: "application/json" },
      payload: JSON.stringify(cuerpo),
      muteHttpExceptions: true
    }).getResponseCode();
  };

  var contacto = pedir("/contacts", {
    email: email,
    attributes: { FIRSTNAME: pila, LASTNAME: apellido },
    listIds: [LISTA_BREVO],
    updateEnabled: true
  });

  var correo = pedir("/smtp/email", {
    sender: REMITENTE,
    to: [{ email: email, name: (pila + " " + apellido).trim() }],
    replyTo: REMITENTE,
    subject: "Ya es tuya: Editor para gente común",
    htmlContent: correoBienvenida(pila),
    tags: ["bienvenida-editor", origen || "sin-origen"]
  });

  return "contacto " + contacto + " / correo " + correo;
}

function correoBienvenida(pila) {
  var saludo = pila ? "Hola " + escapar(pila) + "," : "Hola,";
  var p = 'style="margin:0 0 16px;font:16px/1.55 Arial,Helvetica,sans-serif;color:#1B1F24"';
  return '' +
    '<div style="background:#F2EBDD;padding:32px 16px">' +
    '<div style="max-width:560px;margin:0 auto;background:#FBF7EE;border-radius:14px;padding:32px 28px">' +
    '<p ' + p + '>' + saludo + '</p>' +
    '<p ' + p + '>Gracias por dejarme tus datos. Acá tenés los pasos para instalar la herramienta:</p>' +
    '<p style="margin:0 0 24px"><a href="' + PAGINA_INSTALAR + '" style="display:inline-block;background:#E07B2A;color:#fff;text-decoration:none;font:bold 16px Arial,Helvetica,sans-serif;padding:14px 22px;border-radius:999px">Ver cómo instalarla</a></p>' +
    '<p ' + p + '>Tres cosas para que arranques bien:</p>' +
    '<ol style="margin:0 0 16px;padding-left:22px;font:16px/1.55 Arial,Helvetica,sans-serif;color:#1B1F24">' +
    '<li>Necesitás Claude Pro y tu compu (Mac o Windows).</li>' +
    '<li>Cuando la tengas instalada, escribí <b>/empezar</b> y ella te guía.</li>' +
    '<li>Si algo no funciona, respondé este correo. Lo leo yo.</li>' +
    '</ol>' +
    '<p ' + p + '>La hice para que más gente común pueda comunicar lo que Dios le puso en el corazón, con criterio y sin efectos de más. No es para vender, es para comunicar.</p>' +
    '<p ' + p + '>En el <a href="' + CANAL_YOUTUBE + '" style="color:#E07B2A">canal de YouTube</a> vas a encontrar el tutorial de instalación y nuevo contenido.</p>' +
    '<p ' + p + '>Abrazo,<br><b>Nico</b></p>' +
    '<p style="margin:24px 0 0;font:14px/1.5 Arial,Helvetica,sans-serif;color:#5C574E">PD: Si conocés a alguien que necesita esto, reenviale este correo.</p>' +
    '</div></div>';
}

function escapar(t) {
  return String(t).replace(/[&<>"]/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
  });
}

/** Para probar desde el editor: cambiá el correo y ejecutá esta función. */
function probarBrevo() {
  Logger.log(enviarABrevo("nicolas.paretti@gmail.com", "Nico", "Paretti", "prueba"));
}
