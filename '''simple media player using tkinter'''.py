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
        self.root.geometry('300x100')
        self.root.resizable(True, True)
        self.frame = ttk.Frame(self.root)
        self.frame.pack()  # pack the frame into the window
        self.create_widgets()
        self.player = vlc.MediaPlayer()
        image_icon = tk.PhotoImage(file = "foxi.JPG")
        self.root.iconphoto(False, image_icon)

    def create_widgets(self):
        self.play_button = ttk.Button(self.root, text='Play', command=self.play)
        self.play_button.pack()
        self.stop_button = ttk.Button(self.root, text='Stop', command=self.stop)
        self.stop_button.pack()

    def play(self):
        # Add code to play media
        pass

    def stop(self):
        # Add code to stop media
        pass

app = MediaPlayer()  # create an instance of the application
app.root.mainloop()  # run the application