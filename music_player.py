import tkinter as tk
from tkinter import filedialog
from tkinter import Scale
import os
import pygame as pg
import sys

BLACK_COLOR = '#000000'
PAUSED = True
root = tk.Tk()
root.title('Плеер')
pg.mixer.init()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
height = 500
width = 600
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 4) - (height // 4)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
window_main = tk.Frame(root)
window_playlist = tk.Frame(root)
window_main.config(background=BLACK_COLOR)
volume_scale = Scale(window_main, from_=0, to=1, resolution=0.1,
                     orient=tk.HORIZONTAL, background=BLACK_COLOR,
                     label='Громкость', activebackground='#7852E6',
                     fg='#7852E6', highlightbackground='#7852E6', length=374,
                     troughcolor=BLACK_COLOR, sliderlength=45)
volume_scale.set(1)
volume_scale.place(x=112, y=278)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


logo_image = tk.PhotoImage(file=resource_path('images/logo.png'))
button_play_image = tk.PhotoImage(file=resource_path('images/button_play.png'))
button_next_image = tk.PhotoImage(file=resource_path('images/button_next.png'))
button_previous_image = tk.PhotoImage(
    file=resource_path('images/button_previous.png'))
button_playlist_image = tk.PhotoImage(
    file=resource_path('images/button_playlist.png'))
button_pause_image = tk.PhotoImage(
    file=resource_path('images/button_pause.png'))
button_play_image_playlist = button_play_image
resume_image = button_play_image


def draw_button(window, img, command):
    """
    Создает и возвращает кнопку с изображением.

    Args:
        window (tk.Frame): Родительский фрейм, в котором будет размещена
        кнопка.
        img (tk.PhotoImage): Изображение для кнопки.
        command: Функция, вызываемая при нажатии кнопки.

    Returns:
        tk.Button: Созданная кнопка.
    """
    return tk.Button(
        window,
        image=img,
        borderwidth=0,
        highlightthickness=0,
        command=command,
        relief='flat',
        activebackground=BLACK_COLOR
    )


logo = tk.Label(window_main, image=logo_image, background='#7852E6')
logo.place(x=112, y=121)

button_play = draw_button(
    window_main, button_play_image, lambda: play())
button_play.place(x=243, y=386.0, width=80.0, height=81.0)
button_next = draw_button(
    window_main, button_next_image, lambda: next_song())
button_next.place(x=355, y=397.0, width=74.0, height=56.0)
button_previous = draw_button(
    window_main, button_previous_image, lambda: previous_song())
button_previous.place(x=137, y=397.0, width=74.0, height=56.0)
button_playlist = draw_button(
    window_main, button_playlist_image, lambda: show_frame(window_playlist))
button_playlist.place(x=49, y=378.0, width=76.0, height=32.0)

playing_song = tk.Label(
    window_main,
    text='',
    bg=BLACK_COLOR,
    fg='#7852E6',
    font=('yu gothic ui', 10, 'bold'),
    justify='center'
)
playing_song.place(x=150, y=360, height=20, width=300)

window_playlist.config(background=BLACK_COLOR)
button_play_playlist = draw_button(
    window_playlist, button_play_image_playlist, lambda: call_play())
button_play_playlist.place(x=100.0, y=2.0, width=80.0, height=80.0)

button_back = tk.Button(
    window_playlist,
    text='BACK',
    command=lambda: show_frame(window_main),
    background=BLACK_COLOR,
    activebackground='#7852E6',
    fg='#ffffff'
)
button_back.place(x=26.0, y=25.0, width=54.0, height=33.0)

playlist = tk.Listbox(
    window_playlist,
    selectmode=tk.SINGLE,
    bg=BLACK_COLOR,
    fg='#ffffff',
    font=('yu gothic ui', 10, 'bold'),
    bd=25,
    relief='flat'
)
playlist.place(x=30, y=80, height=406, width=520)

scroll = tk.Scrollbar(window_playlist)
scroll.place(x=550, y=80, height=406)
scroll.config(command=playlist.yview)
playlist.config(yscrollcommand=scroll.set)

for frame in (window_main, window_playlist):
    frame.grid(row=0, column=0, sticky='nsew')


def show_frame(frame):
    """
    Показывает указанный фрейм.

    Args:
        frame (tk.Frame): Фрейм, который нужно показать.
    """
    frame.tkraise()


def call_play():
    """
    Переключается на основное окно и начинает проигрывание песни.
    """
    show_frame(window_main)
    play()


songs = []


def add_files_to_playlist():
    """
    Добавляет выбранные файлы или директории в плейлист.
    """
    files_or_dirs = filedialog.askopenfilenames(
        title='Select Files',
        filetypes=(('Audio files', '*.mp3'),
                   ('All files', '*.*'))
    )
    for item in files_or_dirs:
        playlist.insert(tk.END, item)
        songs.append(os.path.basename(item))
        print(songs)
    playlist.selection_set(0)
    playlist.activate(0)


show_frame(window_main)

button_add_files = tk.Button(
    window_playlist, text='Add Files',
    command=add_files_to_playlist, background=BLACK_COLOR,
    activebackground='#7852E6', fg='#ffffff')
button_add_files.place(x=200, y=25, width=54.0, height=33.0)


def set_volume(volume):
    """
    Установка громкости.
    """
    pg.mixer.music.set_volume(volume)


def play():
    """
    Воспроизводит текущую выбранную песню из плейлиста.
    """
    global PAUSED
    if playlist.size() == 0 and PAUSED:
        show_frame(window_playlist)
        PAUSED = True
        button_pause = draw_button(
            window_main, button_pause_image, lambda: pause_song())
        button_pause.place(x=241, y=385.0, width=80.0, height=81.0)
        return
    else:
        current_song = playlist.get(tk.ACTIVE)
        playing_song['text'] = os.path.basename(current_song)
        song_path = playlist.get(tk.ACTIVE)
        pg.mixer.music.load(song_path)
        set_volume(volume_scale.get())
        pg.mixer.music.play()
        button_pause = draw_button(
            window_main, button_pause_image, lambda: pause_song())
        button_pause.place(x=241, y=385.0, width=80.0, height=81.0)
        root.title(playing_song['text'])
        PAUSED = False


def next_song():
    """
    Проигрывает следующую песню в плейлисте.
    """
    global PAUSED
    if playlist.size() == 0:
        show_frame(window_playlist)
        pause_song()
        return
    next_index = (playlist.curselection()[0] + 1) % playlist.size()
    playlist.selection_clear(0, tk.END)
    playlist.selection_set(next_index)
    playlist.activate(next_index)
    play()


def previous_song():
    """
    Проигрывает предыдущую песню в плейлисте.
    """
    if playlist.size() == 0:
        show_frame(window_playlist)
        return

    next_index = (playlist.curselection()[0] - 1) % playlist.size()
    playlist.selection_clear(0, tk.END)
    playlist.selection_set(next_index)
    playlist.activate(next_index)
    play()


def pause_song():
    """
    Приостанавливает воспроизведение текущей песни.
    """
    global PAUSED
    pg.mixer.music.pause()
    resume_button = draw_button(
        window_main, resume_image, lambda: resume_song())
    resume_button.place(x=243, y=386.0, width=80.0, height=81.0)
    PAUSED = True


def resume_song():
    """
    Возобновляет воспроизведение приостановленной песни.
    """
    global PAUSED
    pg.mixer.music.unpause()
    button_pause = draw_button(
        window_main, button_pause_image, lambda: pause_song())
    button_pause.place(x=243, y=386.0, width=80.0, height=81.0)
    PAUSED = False


def remove_song_from_playlist():
    """
    Удаляет выбранные песни из плейлиста.
    """
    selected_indices = playlist.curselection()
    for index in selected_indices[::-1]:
        playlist.delete(index)
        playlist.selection_set(0)
        playlist.activate(0)


button_remove_song = tk.Button(
    window_playlist, text='Remove Song',
    command=remove_song_from_playlist, background=BLACK_COLOR,
    activebackground='#7852E6', fg='#ffffff')
button_remove_song.place(x=300, y=25, width=100.0, height=33.0)


def check_song_end():
    """
    Проверяет, закончился ли текущий трек, и при необходимости
    переключается на следующий.
    """
    global PAUSED
    if not pg.mixer.music.get_busy() and PAUSED is False:
        next_song()
    # Повторно запускаем проверку каждую секунду
    root.after(1000, check_song_end)


check_song_end()  # Начинаем проверку окончания трека

volume_scale.config(command=lambda volume: set_volume(float(volume)))
root.resizable(False, False)
root.mainloop()
