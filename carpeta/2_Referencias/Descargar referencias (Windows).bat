@echo off
chcp 65001 >nul
rem Descarga los videos de referencia listados en 2_Referencias\links.txt con la conexión de esta computadora (Windows).
rem Un link por línea; opcional, después del link, un nombre para la carpeta. Los videos son solo para estudiar el estilo.
cd /d "%~dp0.."
set Y=.herramientas\win\yt-dlp.exe
set F=.herramientas\win\ffmpeg.exe
if not exist "%Y%" ( echo Falta yt-dlp. Pedile al editor que corra el paso "win". & pause & exit /b 1 )
for /f "usebackq tokens=1,2" %%a in ("2_Referencias\links.txt") do call :bajar "%%a" "%%b"
echo.
echo LISTO. Los videos están en 2_Referencias. Cuando quieras, vaciá links.txt (los ya descargados no se repiten).
pause
exit /b 0
:bajar
set URL=%~1
set NOM=%~2
if "%URL%"=="" exit /b 0
if "%URL:~0,1%"=="#" exit /b 0
if "%NOM%"=="" set NOM=%%(uploader_id,uploader^|ref)s-%%(id)s
echo.
echo - %URL%
"%Y%" --ffmpeg-location "%F%" -f "bv*[height<=1920][ext=mp4]+ba[ext=m4a]/bv*+ba/b" --merge-output-format mp4 --no-playlist --write-info-json --no-overwrites -o "2_Referencias\%NOM%\video.%%(ext)s" "%URL%"
if errorlevel 1 (
  echo    Reintento con la sesión de Chrome ^(para Instagram o videos que piden iniciar sesión^)...
  "%Y%" --ffmpeg-location "%F%" -f "bv*[height<=1920][ext=mp4]+ba[ext=m4a]/bv*+ba/b" --merge-output-format mp4 --no-playlist --write-info-json --no-overwrites --cookies-from-browser chrome -o "2_Referencias\%NOM%\video.%%(ext)s" "%URL%"
)
exit /b 0
