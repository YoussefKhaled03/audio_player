import os
import tkinter as tk
from tkinter import filedialog
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
        self.player = vlc.MediaPlayer()
        image_icon = tk.PhotoImage(file = "foxi22.png")
        self.root.iconphoto(False, image_icon)
        top_frame = tk.Frame(self.root, bg='#09edff')
        top_frame.pack(side='top', fill='both', expand=True)

        # Create a Frame for the video in the lower_frame
        self.video_frame = tk.Frame(top_frame, bg='black')
        self.video_frame.pack(fill='both', expand=True)

        # Wait for the window to be created and mapped (shown on screen)
        self.video_frame.after(1, self.setup_player)

        # Create a Frame for the buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side='bottom', fill='x')

        self.middle_button_frame = tk.Frame(self.button_frame)
        self.middle_button_frame.pack(side='top', expand=True)

        

        # Create a volume scale
        self.volume_var = tk.DoubleVar(value=self.player.audio_get_volume())
        self.volume_scale = tk.Scale(self.root, from_=100, to=0, orient='vertical', variable=self.volume_var, command=self.set_volume, troughcolor='turquoise', sliderlength=20, bg='sky blue')
        self.volume_scale.pack(side='right')

        # Create a video progress scale
        self.progress_var = tk.DoubleVar()
        self.progress_scale = ttk.Scale(self.button_frame, from_=0, to=100, variable=self.progress_var, command=self.set_progress, length=1000)
        self.progress_label = ttk.Label(self.root, text='00:00')
        self.progress_scale.pack(side='left')
        self.update_progress()
        # Create a Frame for the other buttons
        self.other_button_frame = tk.Frame(self.root)
        self.other_button_frame.pack(side='bottom', expand=False)

        # Pack the buttons into the button_frame
        play_button_image = tk.PhotoImage(file="123.png").subsample(10, 15)
        self.play_button = ttk.Button(self.middle_button_frame, image=play_button_image, command=self.open)
        self.play_button.image = play_button_image
        self.play_button.pack(side='left')

        # Pack the other buttons into the other_button_frame
        pause_button_image = tk.PhotoImage(file="123.png").subsample(10, 15)
        self.pause_button = ttk.Button(self.middle_button_frame, image=pause_button_image, command=self.pause)
        self.pause_button.image = pause_button_image
        self.pause_button.pack(side='left')

        backward_button_image = tk.PhotoImage(file="123.png").subsample(10, 15)
        self.skip_backward_button = ttk.Button(self.other_button_frame, image=backward_button_image, command=self.skip_backward)
        self.skip_backward_button.image = backward_button_image
        self.skip_backward_button.pack(side='left')

        forward_button_image = tk.PhotoImage(file="123.png").subsample(10, 15)
        self.skip_forward_button = ttk.Button(self.other_button_frame, image=forward_button_image, command=self.skip_forward)
        self.skip_forward_button.image = forward_button_image
        self.skip_forward_button.pack(side='left')

        slow_down_button_image = tk.PhotoImage(file="123.png").subsample(10, 15)
        self.slow_down_button = ttk.Button(self.other_button_frame, image=slow_down_button_image, command=self.slow_down)
        self.slow_down_button.image = slow_down_button_image
        self.slow_down_button.pack(side='left')

        speed_up_button_image = tk.PhotoImage(file="123.png").subsample(10, 15)
        self.speed_up_button = ttk.Button(self.other_button_frame, image=speed_up_button_image, command=self.speed_up)
        self.speed_up_button.image = speed_up_button_image
        self.speed_up_button.pack(side='left')

    def setup_player(self):
        # Get the window identifier (wid) of the video_frame
        wid = self.video_frame.winfo_id()

        # Set the output window for the player
        if os.name == 'nt':  # for Windows
            self.player.set_hwnd(wid)
        else:  # for Linux and MacOS
            self.player.set_xwindow(wid)

    def set_volume(self, _=None):
        volume = self.volume_var.get()  # get the current volume
        self.player.audio_set_volume(int(volume))  # set the volume

    def set_progress(self, _=None):
        length = self.player.get_length()  # get the length of the video
        progress = self.progress_var.get()  # get the current progress
        time = length * progress / 100  # calculate the time
        self.player.set_time(int(time))  # set the time

    def update_progress(self):
        if self.player.get_state() == vlc.State.Playing:
            length = self.player.get_length()
            time = self.player.get_time()
            progress = time / length * 100
            self.progress_var.set(progress)

        # Schedule the next update
        self.root.after(1000, self.update_progress)

    def skip_backward(self):
        time = self.player.get_time() - 10000  # skip backward 10 seconds
        self.player.set_time(time)

    def skip_forward(self):
        time = self.player.get_time() + 10000  # skip forward 10 seconds
        self.player.set_time(time)

    def slow_down(self):
       current_speed = self.player.get_rate()
       new_speed = current_speed - 0.5
       if new_speed > 0:  # prevent the speed from becoming zero or negative
         self.player.set_rate(new_speed)

    def speed_up(self):
     current_speed = self.player.get_rate()
     new_speed = current_speed + 0.5
     self.player.set_rate(new_speed)

    def pause(self):
        self.player.pause()

    def open(self):
        filepath = filedialog.askopenfilename()
        if filepath:
           self.player.set_mrl(filepath)
           self.player.play()  # start playing the video to get its length
           time.sleep(0.1)  # add a short delay
           self.player.pause()  # pause the video
           length = self.player.get_length() / 1000  # get_length returns length in milliseconds
           self.progress_scale.config(to=length)  # set the Scale widget's range to the length of the video


media_player = MediaPlayer()
media_player.root.mainloop()