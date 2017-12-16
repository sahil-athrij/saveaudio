import pyaudio
import wave
import tkinter
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from os import path
from os import mkdir

class recordaudio:
    def __init__(self):
        self.root = tkinter.Tk()
        self.packet = 1024
        self.format = pyaudio.paInt16
        self.channels = 2
        self.rate = 128000
        self.duration = 1
        self.filename = "output.wav"
        self.p = pyaudio.PyAudio()
        self.speaker = 1
        self.frames = []
        self.getmicrophone()
        self.directory = "audio"
        if not path.exists(self.directory):
            mkdir(self.directory)
        self.ratevalues = [44000, 88000, 128000]

        # frame
        self.frame0 = ttk.Frame(self.root)
        self.frame1 = ttk.Frame(self.root)
        self.frame2 = ttk.Frame(self.root)
        self.frame3 = ttk.Frame(self.root)
        self.frame4 = ttk.Frame(self.root)
        self.frame5 = ttk.Frame(self.root)

        self.frame0.pack(side=tkinter.TOP, pady=5)
        self.frame1.pack(side=tkinter.TOP, pady=5)
        self.frame2.pack(side=tkinter.TOP, pady=5)
        self.frame3.pack(side=tkinter.TOP, pady=5)
        self.frame4.pack(side=tkinter.TOP, pady=5)
        self.frame5.pack(side=tkinter.TOP, pady=5)

        # lable
        self.lable0 = ttk.Label(self.frame0, text="enter file name")
        self.lable1 = ttk.Label(self.frame1, text="enter duration hh:mm:ss")
        self.lable2 = ttk.Label(self.frame2, text="select quality")

        # entry
        self.entry0 = ttk.Entry(self.frame0)
        self.entry1 = ttk.Entry(self.frame1, width=2)
        self.entry2 = ttk.Entry(self.frame1, width=2)
        self.entry3 = ttk.Entry(self.frame1, width=2)

        # combobox
        self.choice = tkinter.StringVar(self.root)
        self.choice.set(44000)
        self.combobox0 = ttk.Combobox(self.frame2, textvariable=self.choice, state="readonly")
        self.combobox0["values"] = self.ratevalues

        # buttons
        self.button0 = ttk.Button(self.frame3, text="change directory", command=self.dire)
        self.button1 = ttk.Button(self.frame4, text="record", command=self.record)
        self.exitbutton = ttk.Button(self.frame5, text="exit", command=self.exit)

        self.root.protocol("WM_DELETE_WINDOW", self.exit)

        # packing
        self.lable0.pack(side=tkinter.LEFT, padx=4)
        self.entry0.pack(side=tkinter.LEFT, padx=4)
        self.lable1.pack(side=tkinter.LEFT, padx=4)
        self.entry1.pack(side=tkinter.LEFT, padx=4)
        self.entry2.pack(side=tkinter.LEFT, padx=4)
        self.entry3.pack(side=tkinter.LEFT, padx=4)
        self.lable2.pack(side=tkinter.LEFT, padx=4)
        self.combobox0.pack(side=tkinter.LEFT, padx=4)
        self.button0.pack(side=tkinter.BOTTOM, padx=4)
        self.button1.pack(side=tkinter.BOTTOM, padx=4)
        self.exitbutton.pack(pady=10, padx=25)

        self.root.mainloop()

    def exit(self):
        if messagebox.showinfo("exit", "saving"):
            self.root.destroy()


    def dire(self):
        self.directory = filedialog.askdirectory()
        if not path.exists(self.directory):
            mkdir(self.directory)

    def getmicrophone(self):
        try:
            for i in range(1, 5):
                SPEAKERS = self.p.get_device_info_by_index(i)  # The part I have modified
                if "stereo mix" in SPEAKERS["name"].lower():
                    self.index = SPEAKERS["index"]
                    self.speaker = 1
                    break
        except:
            self.speaker = 0

    def getinput(self):
        if self.entry0.get():
            self.filename = self.entry0.get() + ".wav"

        if self.entry1.get():
            self.duration += int(self.entry1.get()) * 3600

        if self.entry2.get():
            self.duration += int(self.entry2.get()) * 60

        if self.entry3.get():
            self.duration += int(self.entry3.get())

        self.rate = int(self.choice.get())

    def record(self):
        self.getinput()
        self.frames = []
        stream = self.p.open(format=self.format,
                             channels=self.channels,
                             rate=self.rate,
                             input=True,
                             frames_per_buffer=self.packet,
                             input_device_index=self.index)

        for i in range(0, int(self.rate / self.packet * self.duration)):
            data = stream.read(self.packet)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()
        print("stoped")
        wf = wave.open(self.directory + "\\" + self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()


a = recordaudio()
