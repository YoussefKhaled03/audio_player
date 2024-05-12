'''simple media player using tkinter'''

import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import vlc

class MediaPlayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('foxi')
        self.root.geometry('800x400')
        self.root.resizable(True, True)
        self.frame = ttk.Frame(self.root)
        self.create_widgets()
        self.player = vlc.MediaPlayer()
        image_icon = tk.PhotoImage(file = "foxi22.png")
        self.root.iconphoto(False, image_icon)
        lower_frame = tk.Frame(self.root, bg='#09edff')
        lower_frame.pack(side='bottom', fill='both', expand=True)


    def speed_up(self):
        current_speed = self.player.get_rate()
        new_speed = current_speed + 0.5
        self.player.set_rate(new_speed)

    def slow_down(self):
        current_speed = self.player.get_rate()
        new_speed = current_speed - 0.5
        self.player.set_rate(new_speed)

    # ... other code ...

    def create_widgets(self):
        self.play_button = ttk.Button(self.root, text='Play', command=self.play)
        self.play_button.pack()
        self.stop_button = ttk.Button(self.root, text='Stop', command=self.stop)
        self.stop_button.pack()
        self.open_button = ttk.Button(self.root, text='Open', command=self.open)
        self.open_button.pack()
        self.speed_up_button = ttk.Button(self.root, text='Speed Up', command=self.speed_up)
        self.speed_up_button.pack()
        self.slow_down_button = ttk.Button(self.root, text='Slow Down', command=self.slow_down)
        self.slow_down_button.pack()

        def speed_up(self):
            pass

        def slow_down(self):
            pass
    def play(self):
        self.player.play()

    def stop(self):
        self.player.stop()

    def open(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.player.set_mrl(filepath)

# Create an instance of the media player and start the Tkinter event loop
media_player = MediaPlayer()
media_player.root.mainloop()