@echo off
chcp 65001 >nul
rem Plan B en Windows: descarga el modelo de transcripción (Whisper large-v3-turbo, ~1,6 GB) con la conexión de esta computadora.
rem Doble clic para ejecutar. Si se corta, volvé a hacer doble clic: sigue donde quedó.
cd /d "%~dp0.."
if not exist ".herramientas\whisper" mkdir ".herramientas\whisper"
echo.
echo Descargando el modelo de transcripción (~1,6 GB). Puede tardar unos minutos...
echo.
curl.exe -L -C - --fail -o ".herramientas\whisper\ggml-large-v3-turbo.bin.parcial" "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin"
set TAM=0
for %%A in (".herramientas\whisper\ggml-large-v3-turbo.bin.parcial") do set TAM=%%~zA
if %TAM% GTR 1500000000 (
  move /y ".herramientas\whisper\ggml-large-v3-turbo.bin.parcial" ".herramientas\whisper\ggml-large-v3-turbo.bin" >nul
  echo.
  echo LISTO. El modelo quedó instalado. Ya podés cerrar esta ventana.
) else (
  echo.
  echo La descarga no terminó. Volvé a hacer doble clic en este archivo para seguir.
)
echo.
pause
