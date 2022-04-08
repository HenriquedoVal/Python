import pystray
import os
import psutil
import subprocess

from PIL import Image, ImageDraw, ImageFont


def get_state(v):
    def inner(item):
        return '*' in os.popen('powercfg /l').read().splitlines()[v] # lê minha config atual
    return inner

def full_cpu(): # Uma dos meus planos de energia. Substituir o hexadecimal abaixo conforme necessidade
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW # para não abrir o console na execução
    subprocess.Popen('powercfg /s 16a16fa7-cccc-45bb-a7f5-3a8ca6dc4d8e', startupinfo=startupinfo).communicate()

def eq_cpu(): # Mesma coisa aqui
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.Popen('powercfg /s 381b4222-f694-41f0-9685-ff5bb260df2e', startupinfo=startupinfo).communicate()

def exit_prog(icon):
    icon.stop()
    os._exit(1)
    
def get_image():
    info = round(psutil.cpu_percent(interval=1))
    red = int(info > 74)                                    # Define as cores dos icones
    yellow = int(49 < info < 75)                            #
    g = 255*(yellow | int(not red))                         #
    b = 255*(int(not red and not yellow))                   #
    
    fnt = ImageFont.truetype('C:\\Windows\\Fonts\\msyhl.ttc', 14) # verificar a disponibilidade da fonte na máquina
    img = Image.new('RGBA', (16,16), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.text((8,8), str(info), font=fnt, anchor='mm', fill=(255, g, b, 255))
    return img

def main():
    menu = (pystray.MenuItem('Full CPU', full_cpu, checked=get_state(3), radio=True),
            pystray.MenuItem('Normal CPU', eq_cpu, checked=get_state(4), radio=True),
            pystray.MenuItem('Exit', exit_prog))

    icon = pystray.Icon('CpuIcon', get_image(), 'Battery plan settings', menu)
    
    icon.run_detached()
     
    while 1:
        icon._icon = get_image()  
        icon._update_icon()


if __name__ == '__main__':
    main()