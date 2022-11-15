import os
import subprocess
import ctypes
from datetime import datetime
import threading as th

from PIL import Image, ImageDraw, ImageFont
import pystray
import psutil
import darkdetect
import chromepilot.utils


def callback(color: str):
    # color in ('Light', 'Dark')
    global black
    black = not black


def set_sec(v):
    def inner(item):
        global sec
        sec = v
    return inner


def get_state(v):
    def inner(item):
        return '*' in os.popen('powercfg /l').read().splitlines()[v]
    return inner


def full_cpu():
    subprocess.Popen('powercfg /s 16a16fa7-cccc-45bb-a7f5-3a8ca6dc4d8e',
                     creationflags=subprocess.CREATE_NO_WINDOW).communicate()


def eq_cpu():
    subprocess.Popen('powercfg /s 381b4222-f694-41f0-9685-ff5bb260df2e',
                     creationflags=subprocess.CREATE_NO_WINDOW).communicate()


def sleepless():
    subprocess.Popen('powercfg /s d8486d7c-b26d-4924-9399-4d78100ddbf0',
                     creationflags=subprocess.CREATE_NO_WINDOW).communicate()


def exit_prog(icon):
    icon._hide()
    os._exit(0)


def get_image():
    global black

    info = round(psutil.cpu_percent(interval=sec))
    if info == 100:
        font_size, *pos_tuple = 21, 14, 14
    else:
        font_size, *pos_tuple = 24, 18, 14

    # More code but much more readable
    if black and info < 50:
        colors_tuple = (0, 0, 0, 255)
    elif black and info < 75:
        colors_tuple = (230, 122, 5, 255)
    elif info < 50:
        colors_tuple = (255, 255, 255, 255)
    elif info < 75:
        colors_tuple = (255, 255, 0, 255)
    else:
        colors_tuple = (255, 0, 0, 255)

    fnt = ImageFont.truetype('C:\\Windows\\Fonts\\msyh.ttc', font_size)
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text(pos_tuple, str(info), font=fnt, anchor='mm', fill=colors_tuple)
    return img


def check_choco_updates():
    global choco_update

    out, _ = subprocess.Popen(
        'choco outdated -r',
        stdout=subprocess.PIPE,
        creationflags=subprocess.CREATE_NO_WINDOW
    ).communicate()

    if out:
        choco_update = True


def check_chromedriver_update():
    global chrome_update

    if chromepilot.utils.upgrade_available():
        chrome_update = True


def check_pip_updates():
    global pip_update

    out, _ = subprocess.Popen(
        'pip list -o',
        stdout=subprocess.PIPE,
        creationflags=subprocess.CREATE_NO_WINDOW
    ).communicate()

    for line in out.decode().splitlines()[2:]:
        if not line.startswith(ignore_pip_updates):
            pip_update = True
            break  # noqa


def check_for_updates():
    th.Thread(target=check_choco_updates).start()
    th.Thread(target=check_chromedriver_update).start()
    th.Thread(target=check_pip_updates).start()


def main():

    global choco_update, chrome_update, pip_update

    t = th.Thread(target=darkdetect.listener, args=(callback,))
    t.daemon = True
    t.start()

    check_for_updates()

    menu = (pystray.MenuItem('1 sec', set_sec(1),
                             checked=lambda _: sec == 1, radio=True),
            pystray.MenuItem('0.5 sec', set_sec(0.5),
                             checked=lambda _: sec == 0.5, radio=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Full CPU', full_cpu,
                             checked=get_state(3), radio=True),
            pystray.MenuItem('Normal CPU', eq_cpu,
                             checked=get_state(4), radio=True),
            pystray.MenuItem('Sleepless', sleepless,
                             checked=get_state(5), radio=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Search for updates',
                             lambda x: (check_for_updates())),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Exit', exit_prog))

    icon = pystray.Icon('CpuIcon', get_image(), 'Percentual CPU usage', menu)
    icon.run_detached()

    signal22h = signal04h = 0
    while 1:

        if choco_update:
            icon.notify('Chocolatey signs upgrades available', 'Chocolatey')
            choco_update = False
        if chrome_update:
            icon.notify('New chromedriver available.', 'Chromepilot')
            chrome_update = False
        if pip_update:
            icon.notify('Pip signs upgrades available', 'Pip')
            pip_update = False

        if not signal22h:
            if datetime.now().hour == 22:
                if int(datetime.now().strftime('%j')) % 2 != 0:
                    icon.notify('Z99')

                check_for_updates()
                signal22h += 1

        if not signal04h:
            if datetime.now().hour == 4 and datetime.now().minute == 30:
                if int(datetime.now().strftime('%j')) % 2 == 0:
                    icon.notify('Z99')

                check_for_updates()
                signal04h += 1

        icon.icon = get_image()


if __name__ == '__main__':
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    psutil.Process(os.getpid()).nice(128)

    chrome_update = False
    choco_update = False
    pip_update = False
    sec = 0.5
    black = darkdetect.isLight()
    ignore_pip_updates = (
        'charset-normalizer',
    )

    main()
