chcp 65001
rem .\bin\git_mochikara2.bat
rem https://utasachi.github.io/
.\bin\yt-dlp.exe -U
pause "git 実行してもよろしいですか？"
cd /d D:\karaoke\プレイリスト
chcp 932
git add .
git diff --cached --quiet
if %errorlevel%==0 goto end1
git commit -m "auto update"
git push --force
:end1

cd /d C:\mochikara2\htdocs
git add .
git diff --cached --quiet
if %errorlevel%==0 goto end2
git commit -m "auto update"
git push --force
:end2

cd /d C:\mochikara2\cgi-bin
git add .
git diff --cached --quiet
if %errorlevel%==0 goto end3
git commit -m "auto update"
git push --force
:end3

cd /d C:\mochikara2\bin
git add .
git diff --cached --quiet
if %errorlevel%==0 goto end4
git commit -m "auto update"
git push --force
:end4

cd /d C:\mochikara2\ahk\MochiutaSC
git add . 
git diff --cached --quiet
if %errorlevel%==0 goto end5
git commit -m "auto update"
git push --force
:end5

pause