from tkinter import *
import tkinter
import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

class WaveGeneratorApp:
    def __init__(self,win):

        window.title('Wave Generator Applet')
        window.geometry("600x400+10+20")

        self.title = Label(win, text = 'Wave Generator App', font = ("Arial",25))
        self.title.place(x = 300, anchor = "center", y=25)
        self.course = Label(win, text = 'ENGN 1735: Vibrations')
        self.course.place(x = 300, anchor = "center", y=50)
        self.authors = Label(win, text = 'Jack-William Barotta, Johnny Boustany, Maya Lewis, and Joshua Neronha')
        self.authors.place(x = 300, anchor = "center", y=70)
        self.btn=Button(win, text="Go")
        self.btn.bind('<Button-1>', self.generate_tone)
        self.btn.place(x=130, y=180, anchor = "center")
        self.freqfld=Entry(win, text="Frequency")
        self.freqfld.place(x=80, y=110, width = 80, anchor = "center")
        self.freqlabel = Label(win, text = "Frequency (Hz)")
        self.freqlabel.place(x=80, y=140, width = 100, anchor = "center")
        self.durfld=Entry(win, text="Duration")
        self.durfld.place(x=180, y=110, width = 80, anchor = "center")
        self.durlabel = Label(win, text = "Duration (s)")
        self.durlabel.place(x=180, y=140, width = 100, anchor = "center")


    def generate_tone(self,win):
        p = pyaudio.PyAudio()

        volume = 1     # range [0.0, 1.0]
        fs = 41000       # sampling rate, Hz, must be integer
        duration = int(self.durfld.get())   # in seconds, may be float
        f = int(self.freqfld.get())      # sine frequency, Hz, may be float

        self.time_array = np.arange(fs*duration)

        self.wave = np.sin(2*np.pi*self.time_array*f/fs).astype(np.float32).tobytes()
        self.waveplot = np.sin(2*np.pi*self.time_array*f/fs).astype(np.float32)

        self.plot_function(win)

        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True)

        stream.write(volume*self.wave)

        stream.stop_stream()
        stream.close()

        p.terminate()
    def plot_function(self, win):
        fig, ax = plt.subplots(figsize = (1,3))
        ax.set_xlim([0, 1000])

        canvas = FigureCanvasTkAgg(fig, master = window)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack(side = tkinter.RIGHT)

        ax.plot(self.waveplot)
        pass


window = Tk()
instance = WaveGeneratorApp(window)
window.mainloop()
