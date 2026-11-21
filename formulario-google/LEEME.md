# Conectar el formulario a una Hoja de Google

1. Crea una Hoja de Google nueva (por ejemplo, "Descargas · Editar con sentido").
2. Menú **Extensiones → Apps Script**.
3. Borra lo que aparece y pega el contenido de `Codigo.gs`. Guarda.
4. **Implementar → Nueva implementación** → tipo **Aplicación web**.
   - Ejecutar como: **Yo**
   - Quién tiene acceso: **Cualquier usuario**
5. Autoriza los permisos (Google te avisa que la app no está verificada: es tu propio script). El script solo pide acceso a esta hoja.
6. Copia la **URL de la aplicación web** (termina en `/exec`) y pégala en `docs/origen.js`, en `urlFormulario`.
