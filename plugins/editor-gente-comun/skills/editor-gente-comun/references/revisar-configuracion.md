# Revisar la configuración

Se usa cuando la persona escribe **"ya terminé con la configuración"** (o algo parecido: "ya está todo instalado", "terminé la configuración", "¿quedó todo listo?") o `/revisar-configuracion`. Tu trabajo es comprobar, no suponer: revisas cada punto con una herramienta y recién después le respondes.

## 1. Qué revisas, en este orden

1. **Proyecto.** Estás en un chat dentro de un proyecto de Claude (el hub y el editor viven ahí).
2. **Carpeta.** `Editor de Videos IA` está conectada a esta conversación (`get_device_info` → carpetas conectadas) y tiene sus carpetas: `1_Videos sin editar`, `2_Referencias`, `3_Videos editados`, `4_Recursos`, `5_Mi estilo`.
3. **Permiso de borrado.** Crea un archivo de prueba en `.herramientas/` y bórralo. Si el borrado falla, falta el permiso.
4. **Herramientas.** Corre `bash .herramientas/scripts/preparar_entorno.sh` (sin paso): cada línea tiene que decir `[OK]`. Anota cada `[FALTA]` con su paso.
5. **Transcriptor.** La línea "Modelo Whisper" dice `[OK]`.
6. **Perfil.** Existe `5_Mi estilo/mi-perfil.md` y tiene completos el nombre, el tipo de videos y cómo habla.
7. **Hub.** El hub de contenido está creado (o la persona dijo que no lo quiere) y el archivo **"HUB - leer primero.md"** está en los archivos del proyecto, con el enlace al hub.

## 2. Cómo le respondes

Un mensaje corto con la lista de los siete puntos, cada uno con ✓ o ✗ y una frase simple, sin jerga. Por ejemplo:

> ✓ Tu carpeta Editor de Videos IA está lista.
> ✗ Falta el transcriptor, que pasa tu voz a texto.

- **Si todo está ✓:** felicítala, dile que ya puede empezar y dale tres pedidos de ejemplo adaptados a su perfil (como en el cierre de `bienvenida.md`).
- **Si falta algo:** no le des instrucciones para que lo arregle sola. Ofrécele con la herramienta de preguntas, como opción recomendada, **"Hazlo tú por mí (recomendado)"** (en su trato: "Hacelo vos por mí" si habla de vos), y aplica la regla de oro de `bienvenida.md`: un punto por vez, avisándole antes qué cartel va a ver y qué tocar, comprobando que quedó bien antes de pasar al siguiente. Lo único que solo puede hacer ella es subir "HUB - leer primero.md" a los archivos del proyecto: guíala con una acción por mensaje.
- Al terminar de resolver, vuelve a correr esta revisión entera y muéstrale la lista otra vez, ya con todo en ✓.
