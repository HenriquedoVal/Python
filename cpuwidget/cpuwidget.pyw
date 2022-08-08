import os
import subprocess
import ctypes
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

import pystray
import psutil


def set_sec(v):  # Lê o valor atual de "sec"
    def inner(item):
        global sec
        sec = v
    return inner


def get_state(v):  # Lê a configuração atual do plano de energia.
    def inner(item):
        return '*' in os.popen('powercfg /l').read().splitlines()[v]
    return inner


def full_cpu():  # Muda a configuração sem abrir nova janela.
    global startupinfo
    subprocess.Popen('powercfg /s 16a16fa7-cccc-45bb-a7f5-3a8ca6dc4d8e',
                     startupinfo=startupinfo).communicate()


def eq_cpu():
    global startupinfo
    subprocess.Popen('powercfg /s 381b4222-f694-41f0-9685-ff5bb260df2e',
                     startupinfo=startupinfo).communicate()


def sleepless():
    global startupinfo
    subprocess.Popen('powercfg /s d8486d7c-b26d-4924-9399-4d78100ddbf0',
                     startupinfo=startupinfo).communicate()


def exit_prog(icon):
    icon.stop()
    os._exit(0)


def get_image():
    global sec
    info = round(psutil.cpu_percent(interval=sec))
    font_size = 15 if info == 100 else 16
    red = int(info > 74)
    yellow = int(49 < info < 75)
    g = 255*(yellow | int(not red))
    b = 255*(int(not red and not yellow))

    fnt = ImageFont.truetype('C:\\Windows\\Fonts\\msyh.ttc', font_size)
    img = Image.new('RGBA', (22, 22), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((10, 11), str(info), font=fnt, anchor='mm', fill=(255, g, b, 255))
    return img


def main():
    global sec
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
            pystray.MenuItem('Exit', exit_prog))

    icon = pystray.Icon('CpuIcon', get_image(), 'Percentual CPU usage', menu)

    icon.run_detached()

    signal22h = signal04h = 0
    while 1:
        # Totalmente pessoal, notifica em horários e dias específicos.
        if not signal22h and int(datetime.now().strftime('%j')) % 2 != 0:
            if datetime.now().hour == 22:
                icon.notify('Z99')
                signal22h += 1

        if not signal04h and int(datetime.now().strftime('%j')) % 2 == 0:
            if datetime.now().hour == 4 and datetime.now().minute == 30:
                icon.notify('Z99')
                signal04h += 1

        icon._icon = get_image()
        icon._update_icon()


if __name__ == '__main__':
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    sec = 0.5
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    os.popen(f'wmic Process {os.getpid()} Call SetPriority 128')
    main()
