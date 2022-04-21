from tkinter import *
import tkinter as tk
import tkinter
import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import ImageTk, Image
import pkgutil


class WaveGeneratorApp:
    def __init__(self,win):

        window.title('Wave Generator Applet')
        window.geometry("600x400+10+20")

        brownraw = pkgutil.get_data('resources','brown.png')
        harrisraw = pkgutil.get_data('resources','harris.png')

        brown = ImageTk.PhotoImage(Image.open(brownraw))



        harris = ImageTk.PhotoImage(Image.open(harrisraw))

        self.brownlogo = Label(image=brown)
        self.brownlogo.image = brown
        self.brownlogo.place(x = 100, anchor = "center", y=300)

        self.harrislogo = Label(image=harris)
        self.harrislogo.image = harris
        self.harrislogo.place(x = 240, anchor = "center", y=300)

        self.title = Label(win, text = 'Wave Generator App', font = ("Arial",25))
        self.title.place(x = 140, anchor = "center", y=25)
        self.course = Label(win, text = 'ENGN 1735: Vibrations')
        self.course.place(x = 140, anchor = "center", y=50)
        # self.authors = Label(win, text = 'Jack-William Barotta, Johnny Boustany, Maya Lewis, and Joshua Neronha')
        # self.authors.place(x = 300, anchor = "center", y=70)
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

        self.fig, self.ax = plt.subplots(figsize = (2,3))

        self.canvas = FigureCanvasTkAgg(self.fig, master = window)
        self.canvas.get_tk_widget().pack(side = tkinter.RIGHT,fill=tkinter.Y)
        NavigationToolbar2Tk(self.canvas, win)


    def generate_tone(self,win):


        p = pyaudio.PyAudio()

        volume = 1     # range [0.0, 1.0]
        self.fs = 41000       # sampling rate, Hz, must be integer
        self.duration = int(self.durfld.get())   # in seconds, may be float
        self.f = int(self.freqfld.get())      # sine frequency, Hz, may be float

        self.time_array = np.arange(self.fs*self.duration)

        self.wave = np.sin(2*np.pi*self.time_array*self.f/self.fs).astype(np.float32).tobytes()
        self.waveplot = np.sin(2*np.pi*self.time_array*self.f/self.fs).astype(np.float32)

        self.plot_function(self.fig, self.ax)

        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=self.fs,
                        output=True)

        stream.write(volume*self.wave)

        stream.stop_stream()
        stream.close()

        p.terminate()
    def plot_function(self, fig, ax):

        # fig, ax = plt.subplots(figsize = (2,1))
        # ax.set_xlim([0, 1000])

        self.ax.plot(self.time_array / self.fs, self.waveplot)

        self.canvas.draw()

        # canvas = FigureCanvasTkAgg(fig, master = window)
        # # canvas.draw()
        # # placing the canvas on the Tkinter window
        # canvas.get_tk_widget().pack(side = tkinter.RIGHT,fill=tkinter.Y)

    def close_plot(self,pfig):
        pfig.close()


window = Tk()
instance = WaveGeneratorApp(window)
window.mainloop()
