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
        self.root.configure(bg='turquoise')
        self.frame = ttk.Frame(self.root)
        #self.create_widgets()
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
        self.button_frame = tk.Frame(self.root, bg='turquoise')
        self.button_frame.pack(side='bottom', fill='x')

         # Create a Frame for the other buttons
        self.other_button_frame = tk.Frame(self.root, bg='turquoise')
        self.other_button_frame.pack(side='bottom', expand=False)
        
        self.middle_button_frame = tk.Frame(self.button_frame, bg='turquoise')
        self.middle_button_frame.pack(side='top', expand=True,)

        # Create a volume scale
        self.volume_var = tk.DoubleVar(value=self.player.audio_get_volume())
        self.volume_scale = tk.Scale(self.middle_button_frame, from_=100, to=0, orient='vertical', variable=self.volume_var, command=self.set_volume, troughcolor='turquoise', sliderlength=20, bg='sky blue')
        self.volume_scale.pack(side='right', fill='y')

        # Pack the buttons into the button_frame
        play_button_image = tk.PhotoImage(file="123.png").subsample(14, 19)
        self.play_button = ttk.Button(self.middle_button_frame, image=play_button_image, command=self.open)
        self.play_button.image = play_button_image
        self.play_button.pack(side='left')

        # Pack the other buttons into the other_button_frame
        pause_button_image = tk.PhotoImage(file="better_pause.png").subsample(3, 4)
        self.pause_button = ttk.Button(self.middle_button_frame, image=pause_button_image, command=self.pause)
        self.pause_button.image = pause_button_image
        self.pause_button.pack(side='left')

        backward_button_image = tk.PhotoImage(file="bkwrd.png").subsample(3, 4)
        self.skip_backward_button = ttk.Button(self.other_button_frame, image=backward_button_image, command=self.skip_backward)
        self.skip_backward_button.image = backward_button_image
        self.skip_backward_button.pack(side='left')

        forward_button_image = tk.PhotoImage(file="frwrd.png").subsample(3, 4)
        self.skip_forward_button = ttk.Button(self.other_button_frame, image=forward_button_image, command=self.skip_forward)
        self.skip_forward_button.image = forward_button_image
        self.skip_forward_button.pack(side='left')

        slow_down_button_image = tk.PhotoImage(file="slow.png").subsample(14, 19)
        self.slow_down_button = ttk.Button(self.other_button_frame, image=slow_down_button_image, command=self.slow_down)
        self.slow_down_button.image = slow_down_button_image
        self.slow_down_button.pack(side='left')

        speed_up_button_image = tk.PhotoImage(file="spd.png").subsample(14, 19)
        self.speed_up_button = ttk.Button(self.other_button_frame, image=speed_up_button_image, command=self.speed_up)
        self.speed_up_button.image = speed_up_button_image
        self.speed_up_button.pack(side='left')

        self.new_speed = 1.0 
        self.speed_label = tk.Label(self.other_button_frame, text=f"Speed: {self.new_speed}", bg='turquoise')
        self.speed_label.pack(side='right')

        # Create a video progress scale
        self.time_var = tk.DoubleVar()
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TScale", background="turquoise")
        self.time_scale = ttk.Scale(self.button_frame, from_=0, to=1500, variable=self.time_var, length=1500 , command=self.set_time, style="TScale")
        self.time_label = ttk.Label(self.button_frame, text='00:00')
        self.time_label.pack(side='right')
        self.time_scale.pack(side='left')
        self.update_time()

        # Wait for the window to be created and mapped (shown on screen)
        self.video_frame.after(1, self.setup_player)

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
  
    # Create a method to update the speed label
    def update_speed_label(self):
        self.speed_label.config(text=f"Speed: {self.new_speed}")

    def speed_up(self):
        current_speed = self.player.get_rate()
        new_speed = current_speed + 0.5
        self.player.set_rate(new_speed)
        self.new_speed += 0.5
        self.update_speed_label()
    
    def slow_down(self):
        current_speed = self.player.get_rate()
        new_speed = current_speed - 0.5
        if new_speed > 0:  # prevent the speed from becoming zero or negative
           self.player.set_rate(new_speed)
        self.new_speed -= 0.5
        self.update_speed_label()

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
           #self.player.pause()  # pause the video
           length = self.player.get_length() / 1000  # get_length returns length in milliseconds
           self.time_scale.config(to=length)  # set the Scale widget's range to the length of the video

    def pause(self):
        self.player.pause()

 # Create an instance of the media player and start the Tkinter event loop
media_player = MediaPlayer()
media_player.root.mainloop()