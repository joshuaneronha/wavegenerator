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
        window.geometry("600x400+10+20")

        self.title = Label(win, text = 'Wave Generator App', font = ("Arial",25))
        self.title.place(x = 180, anchor = "center", y=25)
        self.course = Label(win, text = 'ENGN 1735: Vibrations')
        self.course.place(x = 180, anchor = "center", y=50)
        # self.authors = Label(win, text = 'Jack-William Barotta, Johnny Boustany, Maya Lewis, and Joshua Neronha')
        # self.authors.place(x = 300, anchor = "center", y=70)
        self.btn=Button(win, text="Go")
        self.btn.bind('<Button-1>', self.generate_tone)
        self.btn.place(x=180, y=180, anchor = "center")

        self.freqfld=Entry(win, text="Frequency")
        self.freqfld.place(x=80, y=110, width = 80, anchor = "center")
        self.freqlabel = Label(win, text = "Frequency (Hz)")
        self.freqlabel.place(x=80, y=140, width = 100, anchor = "center")

        self.durfld=Entry(win, text="Duration")
        self.durfld.place(x=180, y=110, width = 80, anchor = "center")
        self.durlabel = Label(win, text = "Duration (s)")
        self.durlabel.place(x=180, y=140, width = 100, anchor = "center")

        self.speakfld=Entry(win, text="Speaker")
        self.speakfld.place(x=280, y=110, width = 80, anchor = "center")
        self.speakerlabel = Label(win, text = "Speaker")
        self.speakerlabel.place(x=280, y=140, width = 100, anchor = "center")
        self.speakerlabel = Label(win, text = "0: left, 1: right")
        self.speakerlabel.place(x=280, y=180, anchor = "center")
        self.speakerlabel = Label(win, text = "2: both")
        self.speakerlabel.place(x=280, y=200, anchor = "center")

        self.fig, self.ax = plt.subplots(figsize = (2,3))


#####################################

        self.btn1=Button(win, text="Go1")
        self.btn1.bind('<Button-1>', self.generate_tone1)
        self.btn1.place(x=180, y=300, anchor = "center")

        self.freqfld1=Entry(win, text="Frequency1")
        self.freqfld1.place(x=80, y=230, width = 80, anchor = "center")
        self.freqlabel1 = Label(win, text = "Frequency (Hz)")
        self.freqlabel1.place(x=80, y=260, width = 100, anchor = "center")

        self.durfld1=Entry(win, text="Duration1")
        self.durfld1.place(x=180, y=230, width = 80, anchor = "center")
        self.durlabel1 = Label(win, text = "Duration (s)")
        self.durlabel1.place(x=180, y=260, width = 100, anchor = "center")

        self.speakfld1=Entry(win, text="Speaker1")
        self.speakfld1.place(x=280, y=230, width = 80, anchor = "center")
        self.speakerlabel1 = Label(win, text = "Speaker")
        self.speakerlabel1.place(x=280, y=250, width = 100, anchor = "center")
        self.speakerlabel1 = Label(win, text = "0: left, 1: right")
        self.speakerlabel1.place(x=280, y=300, anchor = "center")
        self.speakerlabel1 = Label(win, text = "2: both")
        self.speakerlabel1.place(x=280, y=320, anchor = "center")

        self.fig1, self.ax1 = plt.subplots(figsize = (2,3))


        
        self.canvas = FigureCanvasTkAgg(self.fig, master = window)
        self.canvas.get_tk_widget().pack(side = tkinter.RIGHT,fill=tkinter.Y)


        #self.canvas1 = FigureCanvasTkAgg(self.fig1, master = window)
        #self.canvas1.get_tk_widget().pack(side = tkinter.LEFT,fill=tkinter.Y)
        #NavigationToolbar2Tk(self.canvas, win)
        #NavigationToolbar2Tk(self.canvas1, win)


    def generate_tone(self,win):
        p = pyaudio.PyAudio()
        volume = 1     # range [0.0, 1.0]
        self.fs = 41000       # sampling rate, Hz, must be integer
        self.duration = int(self.durfld.get())   # in seconds, may be float
        self.f = int(self.freqfld.get())      # sine frequency, Hz, may be float

        self.time_array = np.arange(self.fs*self.duration)

        self.wave = np.sin(2*np.pi*self.time_array*self.f/self.fs).astype(np.float32)
        self.waveplot = np.sin(2*np.pi*self.time_array*self.f/self.fs).astype(np.float32)

        self.plot_function(self.fig, self.ax)

        signal = volume*self.wave
        channels = 1

        self.speaker = int(self.speakfld.get())

        if self.speaker == 0 or self.speaker == 1:
            signal = volume*self.wave
            channels = 2
            stereo_signal = np.zeros([len(signal), 2])
            stereo_signal[:, self.speaker] = signal[:]
            signal = stereo_signal

        if self.speaker == 0 or self.speaker == 1 or self.speaker == 2:
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

    def generate_tone1(self,win):
        p = pyaudio.PyAudio()
        volume = 1     # range [0.0, 1.0]
        self.fs1 = 41000       # sampling rate, Hz, must be integer
        self.duration1 = int(self.durfld1.get())   # in seconds, may be float
        self.f1 = int(self.freqfld1.get())      # sine frequency, Hz, may be float

        self.time_array1 = np.arange(self.fs1*self.duration1)

        self.wave1 = np.sin(2*np.pi*self.time_array1*self.f1/self.fs1).astype(np.float32)
        #self.waveplot1 = np.sin(2*np.pi*self.time_array1*self.f1/self.fs1).astype(np.float32)

        #self.plot_function(self.fig1, self.ax1)

        signal = volume*self.wave1
        channels = 1

        self.speaker1 = int(self.speakfld1.get())

        if self.speaker1 == 0 or self.speaker1 == 1:
            signal = volume*self.wave1
            channels = 2
            stereo_signal = np.zeros([len(signal), 2])
            stereo_signal[:, self.speaker1] = signal[:]
            signal = stereo_signal

        if self.speaker1 == 0 or self.speaker1 == 1 or self.speaker1 == 2:
            stream = p.open(format=pyaudio.paFloat32,
                            channels=channels,
                            rate=self.fs1,
                            output=True)
            chunks = []
            chunks.append(signal)
            chunk = np.concatenate(chunks)*0.1
            stream.write(chunk.astype(np.float32).tobytes())
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
