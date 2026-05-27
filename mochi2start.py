#!c:/mochikara2/.venv/Scripts/pythonw.exe
# -*- coding: utf-8 -*-
# pip install qrcode pillow
import subprocess, shutil, qrcode, time
from configparser import ConfigParser
from pathlib import Path

# プロセス停止
# print(f"mochi2start.py プロセス停止中...")
# subprocess.run(["taskkill", "/IM", "httpd.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# subprocess.run(["taskkill", "/IM", "ffplay.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# subprocess.run(["taskkill", "/IM", "mpc-be64.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ドライブチェック、定義コピー
print(f"mochi2start.py ドライブチェック中...")
src_conf = Path(r"C:\mochikara2\bin\httpd.conf")
dst_conf = Path(r"C:\mochikara2\Apache24\conf\httpd.conf")
shutil.copyfile(src_conf, dst_conf)
for drive in "DEFGHI":
    kara_path = Path(f"{drive}:/karaoke")
    if kara_path.exists():
        src_conf = Path(fr"C:\mochikara2\bin\httpd-mochikara-{drive}.conf")
        dst_conf = Path(r"C:\mochikara2\Apache24\conf\httpd-mochikara.conf")
        shutil.copyfile(src_conf, dst_conf)
        print(f"{drive}ドライブで起動します")
        break
else:
    print("karaoke フォルダが見つかりませんでした")
    exit(1)

# tmp削除
base = Path(__file__).resolve().parent / ".." / "tmp"
patterns = [
    "*.log", "*.txt", "*.ass", "*.mp3",
    "*.mp4", "*.m4a", "*.264", "*_track1", "*.pkl"
]
for p in patterns:
    for f in base.glob(p):
        f.unlink(missing_ok=True)

# QR 作成
input_video = "../htdocs/startmv_org.mp4"
overlay_png1 = "../tmp/qr_wifi.png"
overlay_png2 = "../tmp/qr_url.png"
output_video = "../htdocs/startmv.mp4"
config = ConfigParser()
config.read("../mochikara2.ini", encoding="utf-8")
makeqr = config.get("wifi", "makeqr", fallback="")
ssid =   config.get("wifi", "ssid", fallback="")
passwd = config.get("wifi", "passwd", fallback="")
ipaddr = config.get("wifi", "ipaddr", fallback="")
l3 = config.get("topic", "1", fallback="")
l4 = config.get("topic", "2", fallback="")
shutil.copyfile('../htdocs/startmv_org.ass', '../htdocs/startmv.ass')
l1 = l2 = ""
if ssid and passwd and ipaddr:
    if makeqr == "yes":
        qrcode.make(f"WIFI:T:WPA;S:{ssid};P:{passwd};;",box_size=5,border=2).save("../tmp/qr_wifi.png")
        qrcode.make(f"http://{ipaddr}/",box_size=6,border=2).save("../tmp/qr_url.png")
        cmd = [ "ffmpeg", "-y",
                "-i", input_video,
                "-i", overlay_png1,
                "-i", overlay_png2,
                "-filter_complex",
                "[0:v][1:v]overlay=1050:150[tmp];"
                "[tmp][2:v]overlay=1050:400",
                "-an",output_video ]
        subprocess.run(cmd, check=True)
    else:
        time.sleep(2)
    l1 = f"SSID {ssid} / PASS: {passwd}"
    l2 = f"URL  http://{ipaddr}/"

# ass作成
p = Path("../htdocs/startmv.ass")
txtl = p.read_text(encoding="utf-8")
lines = []
for l in txtl.splitlines():
    if ",Karaoke1," in l:    l += l1
    if ",Karaoke2," in l:    l += l2
    if ",Karaoke3," in l:    l += l3
    if ",Karaoke4," in l:    l += l4
    lines.append(l)
p.write_text("\n".join(lines), encoding="utf-8")

# topic作成
p = Path("../htdocs/mochi2topic.txt")
lines = []
if l3 or l4:
    lines.append("【今日のトピック】")
    lines.append(l3)
    lines.append(l4)
p.write_text("\n".join(lines), encoding="utf-8")


# mochilistクリア
open("../htdocs/mochilist.txt", "w").close()
Path("../htdocs/mochivol.txt").write_text("70")

# iniファイル書き換え
p = Path("../MPC-BE/mpc-be64.ini")
p.write_text(
    p.read_text(encoding="utf-8-sig")
    .replace("PrioritizeExternalAudio=0", "PrioritizeExternalAudio=1")
    .replace("AutoReloadExtSubtitles=1", "AutoReloadExtSubtitles=0"),
    encoding="utf-8-sig"
)