/**
 * Cloudflare Worker: recibe el formulario de editor.nicoyestefi.com
 *  1. Reenvía los datos al Apps Script (Hoja de Google), igual que antes.
 *  2. Suma a la persona a la lista "Editor para gente común" de Brevo.
 *  3. Le envía el correo de bienvenida desde hola@nicoyestefi.com.
 *
 * La clave de Brevo se guarda como secreto del Worker: BREVO_API_KEY
 */

const HOJA = "https://script.google.com/macros/s/AKfycbw9nO9B7FUEtaDa8lLuLlUMNf1fK22gUh6EXsATKY1roh_lj4q6iCziIdz6B_jPEaK1gQ/exec";
const LISTA_BREVO = 3;
const REMITENTE = { name: "Nico y Estefi", email: "hola@nicoyestefi.com" };
const PAGINA_INSTALAR = "https://editor.nicoyestefi.com/instalar.html";
const CANAL_YOUTUBE = "https://www.youtube.com/@nicoyestefi";
const ORIGENES = ["https://editor.nicoyestefi.com", "https://nicoparetti.github.io"];

export default {
  async fetch(request, env, ctx) {
    const origen = request.headers.get("Origin") || "";
    const cors = {
      "Access-Control-Allow-Origin": ORIGENES.includes(origen) ? origen : ORIGENES[0],
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    };
    if (request.method === "OPTIONS") return new Response(null, { headers: cors });
    if (request.method !== "POST") return new Response("ok", { headers: cors });

    const cuerpo = await request.text();
    const datos = new URLSearchParams(cuerpo);
    const limpio = (v) => String(v || "").replace(/^'/, "").trim();
    const email = limpio(datos.get("email")).toLowerCase();
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      return new Response("correo inválido", { status: 400, headers: cors });
    }
    const partes = limpio(datos.get("nombre")).split(/\s+/);
    const pila = partes.shift() || "";
    const apellido = partes.join(" ");
    const via = limpio(datos.get("origen"));

    ctx.waitUntil(Promise.allSettled([
      fetch(HOJA, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: cuerpo
      }),
      enviarABrevo(env.BREVO_API_KEY, email, pila, apellido, via)
    ]));

    return new Response("ok", { headers: cors });
  }
};

async function enviarABrevo(clave, email, pila, apellido, via) {
  if (!clave) return;
  const pedir = (ruta, cuerpo) => fetch("https://api.brevo.com/v3" + ruta, {
    method: "POST",
    headers: { "api-key": clave, "content-type": "application/json", accept: "application/json" },
    body: JSON.stringify(cuerpo)
  });

  const contacto = await pedir("/contacts", {
    email,
    attributes: { FIRSTNAME: pila, LASTNAME: apellido },
    listIds: [LISTA_BREVO],
    updateEnabled: true
  });

  // Brevo responde 201 si el contacto es nuevo y 204 si ya existía.
  // Solo la primera vez se envía la bienvenida, para no gastar envíos.
  if (contacto.status !== 201) return;

  await pedir("/smtp/email", {
    sender: REMITENTE,
    to: [{ email, name: (pila + " " + apellido).trim() }],
    replyTo: REMITENTE,
    subject: "¡Ya es tuyo! Editor con IA",
    htmlContent: correoBienvenida(pila),
    tags: ["bienvenida-editor", via || "sin-origen"]
  });
}

function correoBienvenida(pila) {
  const saludo = pila ? "Hola " + escapar(pila) + "," : "Hola,";
  const p = 'style="margin:0 0 16px;font:16px/1.55 Arial,Helvetica,sans-serif;color:#1B1F24"';
  const enlace = 'style="color:#E07B2A"';
  return '<div style="background:#F2EBDD;padding:32px 16px">' +
    '<div style="max-width:560px;margin:0 auto;background:#FBF7EE;border-radius:14px;padding:32px 28px">' +
    '<p ' + p + '>' + saludo + '<br>Qué bueno estar en contacto. Acá tenés los pasos para instalar la herramienta:</p>' +
    '<p style="margin:0 0 24px"><a href="' + PAGINA_INSTALAR + '" style="display:inline-block;background:#E07B2A;color:#fff;text-decoration:none;font:bold 16px Arial,Helvetica,sans-serif;padding:14px 22px;border-radius:999px">Ver cómo instalarla</a></p>' +
    '<p ' + p + '>Tres cosas para que empieces bien:</p>' +
    '<ol style="margin:0 0 16px;padding-left:22px;font:16px/1.55 Arial,Helvetica,sans-serif;color:#1B1F24">' +
    '<li style="margin-bottom:8px">Necesitás Claude Pro y tu compu (Mac o Windows).</li>' +
    '<li style="margin-bottom:8px">Cuando la tengas instalada, escribí <b>/empezar</b> en un chat y ella te guía.</li>' +
    '<li>Si algo no funciona, respondé este correo. Lo leo yo.</li>' +
    '</ol>' +
    '<p ' + p + '>Esta es una herramienta para gente común. Aquellos que quieren compartir su asignación en redes sociales. No es para vender, es para comunicar. Lográ editar con criterios especialmente creados, elegidos y probados.</p>' +
    '<p ' + p + '>En el <a href="' + CANAL_YOUTUBE + '" ' + enlace + '>canal de YouTube</a> vas a encontrar el tutorial de instalación y nuevo contenido.</p>' +
    '<p ' + p + '>Abrazo,<br><b>Nico</b></p>' +
    '<p style="margin:24px 0 0;font:14px/1.5 Arial,Helvetica,sans-serif;color:#5C574E">PD: Si conocés a alguien que necesita esto, compartile este enlace: <a href="https://editor.nicoyestefi.com" ' + enlace + '>editor.nicoyestefi.com</a></p>' +
    '</div></div>';
}

function escapar(t) {
  return String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}
