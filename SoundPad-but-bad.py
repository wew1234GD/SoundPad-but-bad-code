import pygame
import pygame_gui
import tkinter as tk
from tkinter import filedialog
import os

pygame.init()
pygame.mixer.init()

pygame.display.set_caption("SoundPad dlya bednix")
window_size = (800, 600)
window_surface = pygame.display.set_mode(window_size)

manager = pygame_gui.UIManager(window_size)

add_sound_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 50), (200, 50)),
    text='Добавить звук',
    manager=manager
)

play_sound_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 120), (200, 50)),
    text='Проиграть звук',
    manager=manager
)

pause_sound_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 190), (200, 50)),
    text='Остановить',
    manager=manager
)


sound_list = []
sound_files = []  
selected_sound = None
is_paused = False


sound_selection_list = pygame_gui.elements.UISelectionList(
    relative_rect=pygame.Rect((300, 50), (400, 400)),  
    item_list=sound_list,
    manager=manager
)

def add_sound():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Выберите звуковой файл",
        filetypes=(("Audio files", "*.wav;*.mp3"), ("All files", "*.*"))
    )
    if file_path:
        sound_name = os.path.basename(file_path)  
        sound_list.append(sound_name)  
        sound_files.append(file_path)  
        sound_selection_list.set_item_list(sound_list)  
        print(f"Звук добавлен: {file_path}")

def play_sound():
    global selected_sound, is_paused
    if selected_sound:
        pygame.mixer.music.load(selected_sound)
        pygame.mixer.music.play()
        is_paused = False
        print(f"Проигрывание звука: {selected_sound}")

def pause_sound():
    global is_paused
    if pygame.mixer.music.get_busy():
        if is_paused:
            pygame.mixer.music.unpause()
            is_paused = False
        else:
            pygame.mixer.music.pause()
            is_paused = True

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == add_sound_button:
                add_sound()

            if event.ui_element == play_sound_button:
                if selected_sound:
                    play_sound()

            if event.ui_element == pause_sound_button:
                pause_sound()

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            selected_index = sound_list.index(event.text)
            selected_sound = sound_files[selected_index] 
            print(f"Выбран звук: {selected_sound}")

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.fill((0, 0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()
