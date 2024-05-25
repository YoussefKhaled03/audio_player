'''simple media player using tkinter'''

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
        self.time_var = tk.DoubleVar()
        self.time_scale = ttk.Scale(self.root, from_=0, to=1, variable=self.time_var, command=self.set_time, length=400)
        self.time_scale.pack(side=tk.LEFT)
        self.time_label = ttk.Label(self.root, text='00:00')
        self.time_label.pack(side=tk.LEFT)
        self.update_time()  
        self.volume_var = tk.DoubleVar(value=self.player.audio_get_volume())
        self.volume_scale = tk.Scale(self.root, from_=100, to=0, orient='vertical', variable=self.volume_var, command=self.set_volume)
        self.volume_scale.pack(side='right')
        # Create a Frame for the video in the lower_frame
        self.video_frame = tk.Frame(lower_frame, bg='black')
        self.video_frame.pack(fill='both', expand=True)

        # Wait for the window to be created and mapped (shown on screen)
        self.video_frame.after(1, self.setup_player)



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
        self.skip_forward_button = ttk.Button(self.root, text='Skip Forward', command=self.skip_forward)
        self.skip_forward_button.pack()
        self.skip_backward_button = ttk.Button(self.root, text='Skip Backward', command=self.skip_backward)
        self.skip_backward_button.pack()
        '''self.five_sec_forward_button = ttk.Button(self.root, text='5 sec Forward', command=self.five_sec_forward_button)
        self.five_sec_forward_button.pack()
        self.five_sec_backward_button = ttk.Button(self.root, text='5 sec Backward', command=self.five_sec_backward_button)
        self.five_sec_backward_button.pack()'''

    def setup_player(self):
        # Get the window identifier (wid) of the video_frame
        wid = self.video_frame.winfo_id()

        # Set the output window for the player
        if os.name == 'nt':  # for Windows
            self.player.set_hwnd(wid)
        else:  # for Linux and MacOS
            self.player.set_xwindow(wid)

    def set_time(self, _=None):
        time = self.time_var.get()
        self.player.set_time(int(time * 1000))  # VLC's set_time method expects time in milliseconds

    def update_time(self):
        if self.player.get_state() == vlc.State.Playing:
            time = self.player.get_time() / 1000  # get_time returns time in milliseconds
            self.time_var.set(time)
            minutes, seconds = divmod(time, 60)
            self.time_label.config(text=f'{int(minutes):02}:{int(seconds):02}')
        self.root.after(1000, self.update_time)
  
    def speed_up(self):
        current_speed = self.player.get_rate()
        new_speed = current_speed + 0.5
        self.player.set_rate(new_speed)

    def slow_down(self):
        current_speed = self.player.get_rate()
        new_speed = current_speed - 0.5
        if new_speed > 0:  # prevent the speed from becoming zero or negative
           self.player.set_rate(new_speed)

    def set_volume(self, _=None):  # the Scale widget passes the new value to the command, but we don't need it because we're using a variable
        volume = self.volume_var.get()
        self.player.audio_set_volume(int(volume))

    def skip_forward(self):
     time = self.player.get_time() + 5000  # add 5 seconds
     self.player.set_time(time)
     
    def skip_backward(self):
        time = self.player.get_time() - 5000
        self.player.set_time(time)


    def play(self):
        self.player.play()
        self.update_time()  # start updating the time

    def stop(self):
        self.player.stop()


    def open(self):
        filepath = filedialog.askopenfilename()
        if filepath:
           self.player.set_mrl(filepath)
           self.player.play()  # start playing the video to get its length
           time.sleep(0.1)  # add a short delay
           self.player.pause()  # pause the video
           length = self.player.get_length() / 1000  # get_length returns length in milliseconds
           self.time_scale.config(to=length)  # set the Scale widget's range to the length of the video

    def pause(self):
        self.player.pause()

 # Create an instance of the media player and start the Tkinter event loop
media_player = MediaPlayer()
media_player.root.mainloop()