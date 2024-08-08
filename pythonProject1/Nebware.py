import os
import requests
import platform
import threading
import random
import time
import pygame
from ctypes import windll
from tkinter import Tk, Label
from PIL import Image, ImageTk

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def download_file(url, local_path):
    response = requests.get(url)
    with open(local_path, 'wb') as file:
        file.write(response.content)

def download_resources():
    popup_urls = [
        'https://github.com/NebbyOW/Nebware/blob/main/Nebware/image1.jpeg',
        'https://github.com/NebbyOW/Nebware/blob/main/Nebware/image2.jpg',
        'https://github.com/NebbyOW/Nebware/blob/main/Nebware/image3.jpg',
        'https://github.com/NebbyOW/Nebware/blob/main/Nebware/image4.jpg',
        'https://github.com/NebbyOW/Nebware/blob/main/Nebware/image5.jpeg',
        'https://github.com/NebbyOW/Nebware/blob/main/Nebware/image6.PNG',
        'https://github.com/NebbyOW/Nebware/blob/main/Nebware/image7.jpg',
        'https://github.com/NebbyOW/Nebware/blob/main/Nebware/image8.jpg'
    ]
    audio_urls = {
        'https://github.com/NebbyOW/Nebware/blob/main/Nebware/audio1.mp3',
        'https://github.com/NebbyOW/Nebware/blob/main/Nebware/audio2.mp3',
        'https://github.com/NebbyOW/Nebware/blob/main/Nebware/audio3.mp3'
    }
    wallpaper_urls = [
        'https://github.com/NebbyOW/Nebware/blob/main/Nebware/wallpaper1.png',
        'https://github.com/NebbyOW/Nebware/blob/main/Nebware/wallpaper2.jpg'
    ]

    #Create Temp Directories
    os.makedirs('temp/popup', exist_ok=True)
    os.makedirs('temp/audio', exist_ok=True)
    os.makedirs('temp/wallpaper', exist_ok=True)

    wallpaper_files = []
    popup_files = []
    audio_files = []

    for url in popup_urls:
        local_path = os.path.join('temp/popup', os.path.basename(url))
        download_file(url, local_path)

    for url in audio_urls:
        local_path = os.path.join('temp/audio', os.path.basename(url))
        download_file(url, local_path)

    for url in wallpaper_urls:
        local_path = os.path.join('temp/wallpaper', os.path.basename(url))
        download_file((url, local_path))

    return popup_files, audio_files, wallpaper_files

def change_wallpaper(image_path):
    if platform.system() == 'Windows':
        windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
    elif platform.system() == 'Darwin':
        os.system(f"osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"{image_path}\"'")
    elif platform.system() == 'Linux':
        os.system(f"gsettings set org.gnome.desktop.background picture-uri file://{image_path}")

def play_random_audio(audio_files):
    pygame.mixer.init()
    while True:
        audio_file = random.choice(audio_files)
        pygame.mixer.music.load(audio_files)
        pygame.mixer.music.play()
        time.sleep(random.randint(30, 120))

def show_popup(image_path):
    root = Tk()
    img = Image.open(image_path)
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    root.after(5000, lambda: root.destroy()) #close after 5 seconds
    root.mainloop()

def random_popups(popup_files):
    while True:
        image_file = random.choice(popup_files)
        show_popup(popup_files)
        time.sleep(random.randint(30, 120))

def main():
    popup_files, audio_files, wallpaper_files = download_resources()

    #Start the wall paper change, audio player, and popup gen
    threading.Thread(target=random_popups, args=(popup_files,)).start()
    threading.Thread(target=play_random_audio, args=(audio_files,)).start()

    #change wallpaper every minute
    while True:
        change_wallpaper(random.choice(wallpaper_files))
        time.sleep(60)

if __name__ == '__main__':
    main()





# Press the green button in the gutter to run the script.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
