from tkinter import *
import tkinter as tk
import tkinter
import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class WaveGeneratorApp:
    def __init__(self,win):

        window.title('Wave Generator Applet')
        window.geometry("800x400+10+20")

        self.title = Label(win, text = 'Wave Generator App', font = ("Arial",25))
        self.title.place(x = 180, anchor = "center", y=25)
        self.course = Label(win, text = 'ENGN 1735: Vibrations')
        self.course.place(x = 180, anchor = "center", y=50)
        # self.authors = Label(win, text = 'Jack-William Barotta, Johnny Boustany, Maya Lewis, and Joshua Neronha')
        # self.authors.place(x = 300, anchor = "center", y=70)
        self.btn=Button(win, text="Go")
        self.btn.bind('<Button-1>', self.generate_tone)
        self.btn.place(x=180, y=210, anchor = "center")

        self.freqfld=Entry(win, text="Frequency")
        self.freqfld.place(x=80, y=110, width = 80, anchor = "center")
        self.freqlabel = Label(win, text = "Right (Hz)")
        self.freqlabel.place(x=80, y=140, anchor = "center")

        self.freqfld1=Entry(win, text="Frequency1")
        self.freqfld1.place(x=180, y=110, width = 80, anchor = "center")
        self.freqlabel1 = Label(win, text = "Left(Hz)")
        self.freqlabel1.place(x=180, y=140, anchor = "center")
        self.optionallabel = Label(win, text = "--optional--")
        self.optionallabel.place(x=180, y=160, anchor = "center")

        self.durfld=Entry(win, text="Duration")
        self.durfld.place(x=280, y=110, width = 80, anchor = "center")
        self.durlabel = Label(win, text = "Duration (s)")
        self.durlabel.place(x=280, y=140, width = 100, anchor = "center")

        #self.course = Label(win, text = 'RIGHT')
        #self.course.place(x = 250, anchor = "center", y=110)

        self.fig, self.ax = plt.subplots(figsize = (2,3))
        self.canvas = FigureCanvasTkAgg(self.fig, master = window)
        self.canvas.get_tk_widget().pack(side = tkinter.RIGHT,fill=tkinter.Y)
        NavigationToolbar2Tk(self.canvas, win)


    def generate_tone(self,win):

        self.ax.clear()

        p = pyaudio.PyAudio()

        volume = 1     # range [0.0, 1.0]
        self.fs = 41000       # sampling rate, Hz, must be integer

        try:
            self.f = int(self.freqfld.get())      # sine frequency, Hz, may be float
            self.f1 = int(self.freqfld1.get())      # sine frequency, Hz, may be float

            self.flist = [self.f, self.f1]

        except:
            self.f = int(self.freqfld.get())      # sine frequency, Hz, may be float

            self.flist = [self.f]

        if len(self.durfld.get()) != 0:
            self.duration = int(self.durfld.get())   # in seconds, may be float

            if len(self.freqfld.get()) != 0:
                self.time_array = np.arange(self.fs*self.duration)
                self.wave = np.sin(2*np.pi*self.time_array*self.f/self.fs).astype(np.float32)
                self.waveplot = np.sin(2*np.pi*self.time_array*self.f/self.fs).astype(np.float32)
                self.plot_function(self.fig, self.ax, self.waveplot, self.time_array, self.canvas,self.flist)

            if len(self.freqfld1.get()) != 0:
                self.time_array1 = np.arange(self.fs*self.duration)
                self.wave1 = np.sin(2*np.pi*self.time_array1*self.f1/self.fs).astype(np.float32)
                self.waveplot1 = np.sin(2*np.pi*self.time_array1*self.f1/self.fs).astype(np.float32)
                self.plot_function(self.fig, self.ax, self.waveplot1, self.time_array1, self.canvas, self.flist)

            signal = 0
            channels = 1

            if len(self.freqfld.get()) != 0 and len(self.freqfld1.get()) != 0:
                signal = volume*self.wave
                signal1 = volume*self.wave1
                length = len(signal)
                stereo_signal = np.zeros([length, 2])
                stereo_signal[:, 1] = signal[:]
                stereo_signal[:, 0] = signal1[:]
                signal = stereo_signal
                channels = 2

            elif len(self.freqfld.get()) != 0 and len(self.freqfld1.get()) == 0:
                signal = volume*self.wave

            elif len(self.freqfld.get()) == 0 and len(self.freqfld1.get()) != 0:
                signal = volume*self.wave1

            if len(self.freqfld.get()) != 0 or len(self.freqfld1.get()) != 0:
                stream = p.open(format=pyaudio.paFloat32,
                                channels=channels,
                                rate=self.fs,
                                output=True)
                chunks = []
                chunks.append(signal)
                chunk = np.concatenate(chunks)*0.1
                stream.write(chunk.astype(np.float32).tobytes())
                stream.stop_stream()
                stream.close()
        p.terminate()

    def plot_function(self, fig, ax, waveplot, time_array, canvas, flist):

        # fig, ax = plt.subplots(figsize = (2,1))
        # ax.set_xlim([0, 1000])

        # fig.clf()

        maxf = max(flist)

        ax.plot(time_array / self.fs, waveplot)

        ax.set_xlim(0, 5/maxf)

        ax.legend(['Right', 'Left'],loc = 'upper right')
        ax.set_title('Frequency Plot')
        ax.set_xlabel('Time')

        canvas.draw()

        # canvas = FigureCanvasTkAgg(fig, master = window)
        # # canvas.draw()
        # # placing the canvas on the Tkinter window
        # canvas.get_tk_widget().pack(side = tkinter.RIGHT,fill=tkinter.Y)

    def close_plot(self,pfig):
        pfig.close()


window = Tk()
instance = WaveGeneratorApp(window)
window.mainloop()
