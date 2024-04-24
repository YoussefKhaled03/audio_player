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
        self.root.title('Media Player')
        self.root.geometry('300x100')
        self.root.resizable(True, True)
        self.frame = ttk.Frame(self.root)
        self.create_widgets()
        self.player = vlc.MediaPlayer()

    def create_widgets(self):
        self.play_button = ttk.Button(self.root, text='Play', command=self.play)
        self.play_button.pack()
        self.stop_button = ttk.Button(self.root, text='Stop', command=self.stop)
        self.stop_button.pack()
        self.open_button = ttk.Button(self.root, text='Open', command=self.open)
        self.open_button.pack()

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