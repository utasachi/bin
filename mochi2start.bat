cd /d %~dp0
taskkill /im httpd.exe    2>NUL
taskkill /im mpc-be64.exe 2>NUL
taskkill /im ffplay.exe   2>NUL
uwsc uwsc_usage.uws
if errorlevel 1 exit
..\.venv\Scripts\python.exe mochi2start.py
start .\mochikara2_httpd.lnk
timeout /t 1
start "âπê∫êÿë÷ó}é~" /min ffplay.exe -volume 1 -loop -1 -hide_banner -nodisp ..\htdocs\startmv_silent.mp3
timeout /t 1
start "MPC-BE" "C:\mochikara2\MPC-BE\mpc-be64.exe" C:\mochikara2\htdocs\startmv.mp4 /fullscreen /monitor 2 /play /volume 70
timeout /t 20
