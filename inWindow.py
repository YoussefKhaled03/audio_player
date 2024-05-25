import os
import tkinter as tk
from tkinter import filedialog
#from tkinter import messagebox
from tkinter import ttk
import vlc
import time

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
        self.pause_button = ttk.Button(self.root, text='Pause', command=self.pause)
        self.pause_button.pack()

        # Create a Frame for the video in the lower_frame
        self.video_frame = tk.Frame(lower_frame, bg='black')
        self.video_frame.pack(fill='both', expand=True)

        # Wait for the window to be created and mapped (shown on screen)
        self.video_frame.after(1, self.setup_player)


    def create_widgets(self):
        self.open_button = ttk.Button(self.root, text='Open', command=self.open)
        self.open_button.pack()

    def setup_player(self):
        # Get the window identifier (wid) of the video_frame
        wid = self.video_frame.winfo_id()

        # Set the output window for the player
        if os.name == 'nt':  # for Windows
            self.player.set_hwnd(wid)
        else:  # for Linux and MacOS
            self.player.set_xwindow(wid)

    def pause(self):
        self.player.pause()  # Toggle between play and pause


    def open(self):
        filepath = filedialog.askopenfilename()
        if filepath:
           self.player.set_mrl(filepath)
           self.player.play()  # start playing the video to get its length
           time.sleep(0.1)  # add a short delay
           self.player.pause()  # pause the video
           length = self.player.get_length() / 1000  # get_length returns length in milliseconds
           self.time_scale.config(to=length)  # set the Scale widget's range to the length of the video

media_player = MediaPlayer()
media_player.root.mainloop()