import tkinter
from tkinter import ttk
from util import Alarm, Stopwatch, Timer, formatClockTime, formatTimerTimeTuple, TimekeepTypes
from pygame import mixer
import time
import database as db

mixer.init()

class AlarmWindow():
    def on_close(self):
        print("alarm window closed")
        mixer.music.stop()
        self.root.destroy()
    def tick(self):
        if (not self.instance.paused):
            if (self.instance.is_time()):
                mixer.music.load("sounds/default.wav")
                mixer.music.play(-1)
                self.instance.paused = True
                self.pauseButton.config(text="Stop Sound")
                self.soundPlaying = True
            else:
                self.root.after(1000, self.tick)

    def toggle_pause(self):
        if self.soundPlaying:
            mixer.music.stop()
            self.soundPlaying = False
            self.instance.paused = True
            self.pauseButton.config(text="Start")
            return
        
        self.instance.paused = not self.instance.paused
        if self.instance.paused:
            self.pauseButton.config(text="Start")
        else:
            self.pauseButton.config(text="Pause")
            self.root.after(1000, self.tick)

    def __init__(self, master, alarmInstance : Alarm):
        self.instance = alarmInstance
        self.soundPlaying = False

        self.root = tkinter.Toplevel(master)
        # self.root.geometry("450x450")
        self.root.title("Timekeeper Alarm")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.timeDisplay = ttk.Label(self.root, text="Alarm for "+formatClockTime(str(self.instance.timeTrigger)))
        self.timeDisplay.pack(pady=(10, 10), padx=(20, 20))

        if self.instance.paused:
            self.pauseButton = ttk.Button(self.root, text="Start", command=self.toggle_pause)
        else:
            self.pauseButton = ttk.Button(self.root, text="Pause", command=self.toggle_pause)
        self.pauseButton.pack(pady=(0, 10), padx=(10, 10))

        self.root.after(1000, self.tick)

class TimerWindow():
    def on_close(self):
        print("timer window closed")
        mixer.music.stop()
        self.root.destroy()

    def updateDisplay(self):
        self.timeDisplay.config(text=formatTimerTimeTuple(self.instance.timeLeft, abbreviate=True)+" left")

    def tick(self):
        if (not self.instance.paused):
            now = time.time()
            finished = self.instance.tick(now - self.timeSinceTick)
            self.timeSinceTick = now
            if (finished):
                mixer.music.load("sounds/default.wav")
                mixer.music.play(-1)
                self.instance.paused = True
                self.pauseButton.config(text="Stop Sound")
                self.soundPlaying = True
            else:
                self.root.after(200, self.tick)
            self.updateDisplay()
    
    def reset(self):
        self.instance.restart()
        self.instance.paused = True
        self.toggle_pause(change_pause_value = False)
        self.updateDisplay()

    def toggle_pause(self, change_pause_value = True):
        if self.soundPlaying:
            mixer.music.stop()
            self.soundPlaying = False
            self.instance.paused = True
            self.pauseButton.config(text="Start")
            return
        
        if change_pause_value:
            self.instance.paused = not self.instance.paused
        if self.instance.paused:
            self.pauseButton.config(text="Start")
        else:
            self.timeSinceTick = time.time()
            self.pauseButton.config(text="Pause")
            self.root.after(100, self.tick)

    def __init__(self, master, timerInstance : Timer):
        self.instance = timerInstance
        self.soundPlaying = False

        self.root = tkinter.Toplevel(master)
        # self.root.geometry("450x450")
        self.root.title("Timekeeper Timer")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.timeDisplay = ttk.Label(self.root, text="Timer for "+formatTimerTimeTuple(self.instance.totalTime, abbreviate=True))
        self.timeDisplay.pack(pady=(10, 10), padx=(20, 20))

        self.timeDisplay = ttk.Label(self.root, text=formatTimerTimeTuple(self.instance.timeLeft, abbreviate=True)+" left")
        self.timeDisplay.pack(pady=(0, 10), padx=(20, 20))

        self.btnFrame = ttk.Frame(self.root)

        if self.instance.paused:
            self.pauseButton = ttk.Button(self.btnFrame, text="Start", command=self.toggle_pause)
        else:
            self.pauseButton = ttk.Button(self.btnFrame, text="Pause", command=self.toggle_pause)
            self.timeSinceTick = time.time()
        self.pauseButton.grid(row=1, column=1, pady=(0, 10), padx=(10, 5))

        self.resetButton = ttk.Button(self.btnFrame, text="Reset", command=self.reset)
        self.resetButton.grid(row=1, column=2, pady=(0, 10), padx=(5, 10))

        self.btnFrame.pack()

        self.root.after(200, self.tick)

class StopwatchWindow():
    def updateDisplay(self):
        self.timeDisplay.config(text=str(round(self.instance.timeElapsed, 1))+" passed")

    def tick(self):
        if (not self.instance.paused):
            now = time.time()
            finished = self.instance.tick(now - self.timeSinceTick)
            self.timeSinceTick = now
            self.root.after(100, self.tick)
            self.updateDisplay()
    
    def reset(self):
        self.instance.restart()
        self.instance.paused = True
        self.toggle_pause(change_pause_value=False)
        self.updateDisplay()

    def toggle_pause(self, change_pause_value=True):
        if change_pause_value:
            self.instance.paused = not self.instance.paused
        if self.instance.paused:
            self.pauseButton.config(text="Start")
        else:
            self.timeSinceTick = time.time()
            self.pauseButton.config(text="Pause")
            self.root.after(100, self.tick)

    def __init__(self, master, stopwatchInstance : Stopwatch):
        self.instance = stopwatchInstance
        self.soundPlaying = False

        self.root = tkinter.Toplevel(master)
        # self.root.geometry("450x450")
        self.root.title("Timekeeper Stopwatch")

        self.timeDisplay = ttk.Label(self.root, text="Stopwatch: LABEL HERE")
        self.timeDisplay.pack(pady=(10, 10), padx=(20, 20))

        self.timeDisplay = ttk.Label(self.root, text=str(round(self.instance.timeElapsed, ndigits=1))+" passed")
        self.timeDisplay.pack(pady=(0, 10), padx=(20, 20))

        self.btnFrame = ttk.Frame(self.root)

        if self.instance.paused:
            self.pauseButton = ttk.Button(self.btnFrame, text="Start", command=self.toggle_pause)
        else:
            self.pauseButton = ttk.Button(self.btnFrame, text="Pause", command=self.toggle_pause)
            self.timeSinceTick = time.time()
        self.pauseButton.grid(row=1, column=1, pady=(0, 10), padx=(10, 5))

        self.resetButton = ttk.Button(self.btnFrame, text="Reset", command=self.reset)
        self.resetButton.grid(row=1, column=2, pady=(0, 10), padx=(5, 10))

        self.btnFrame.pack()

        self.root.after(100, self.tick)

class CreateTimekeepWindow():
    def verifyAlarmHoursCorrect(self, input : str):
        return (input.isdigit() and (0 <= int(input) <= 23)) or input == ""
    def verifyAlarmMinutesCorrect(self, input : str):
        return (input.isdigit() and (0 <= int(input) <= 59) and len(input) <= 2) or input == ""
    def verifyLabelLength(self, input : str):
        return (0 < len(input) < 20)
    def verifyIsNum(self, input : str):
        return input.isdigit() and len(input) <= 4
    
    def updateVisibleWidgets(self, a=""):
        for i in self.inputsFrame.winfo_children():
            i.grid_forget()

        typeA = self.typeVar.get()
        toGrid = [self.label]
        
        if typeA == "Alarm":
            toGrid.append(self.alarmInputs)
        elif typeA == "Timer":
            toGrid.append(self.timerInputs)
        
        row = 1
        col = 1
        for l in toGrid:
            for i in l:
                i.grid(row=row, column=col)
                col += 1
            row += 1
            col = 1

    def create(self):
        timekeepType = self.typeVar.get()
        access = db.dbAccesser()

        label = self.label[1].get()
        if label == "" or label == " ":
            label = timekeepType + " "

        if timekeepType == "Alarm":
            hours = self.alarmInputs[1].get()
            minutes = self.alarmInputs[3].get()
            if len(minutes) == 1:
                minutes = "0" + minutes
            elif len(minutes) == 0:
                minutes = "00"
            timekeep = Alarm(int(hours+minutes))
        elif timekeepType == "Timer":
            minutes = self.timerInputs[1].get()
            seconds = self.timerInputs[3].get()
            if len(seconds) == 0:
                seconds = "0"
            elif len(minutes) == 0:
                minutes = "0"
            timekeep = Timer(minutes+"|"+seconds)
        else:
            timekeep = Stopwatch()

        access.addItem(timekeep)
        self.onDeath()
        self.root.destroy()

    def __init__(self, master):
        self.root = tkinter.Toplevel(master)
        self.root.title("Create Timekeep")
        self.title = ttk.Label(self.root, text="Create Timekeep", font=('Yrsa', 20))
        self.title.pack(padx=(15,15), pady=(15, 0))

        self.types = ["Alarm", "Timer", "Stopwatch"]
        self.typeVar = tkinter.StringVar(self.root, value="Alarm")

        self.typeDropdown = ttk.OptionMenu(self.root, self.typeVar, "Alarm", "Alarm", "Stopwatch", "Timer", command=self.updateVisibleWidgets)
        self.typeDropdown.pack(pady=(15, 15), padx=(15, 15))

        VAHCcmd = (self.root.register(self.verifyAlarmHoursCorrect))
        VAMCcmd = (self.root.register(self.verifyAlarmMinutesCorrect))
        VLLcmd = (self.root.register(self.verifyLabelLength))
        VINcmd = (self.root.register(self.verifyIsNum))

        self.labelInputFrame = ttk.Frame(self.root)
        self.inputsFrame = ttk.Frame(self.root)

        self.label = [ttk.Label(self.labelInputFrame, text="Timekeep Label: "), ttk.Entry(self.labelInputFrame, validate='all', validatecommand=(VLLcmd, "%P"))]
        self.alarmInputs = [ttk.Label(self.inputsFrame, text="Time (military format): "), ttk.Entry(self.inputsFrame, validate='all', width=2, validatecommand=(VAHCcmd, '%P')), ttk.Label(self.inputsFrame, text=" : "), ttk.Entry(self.inputsFrame, validate='all', width=2, validatecommand=(VAMCcmd, '%P'))]
        self.timerInputs = [ttk.Label(self.inputsFrame, text="Minutes: "), ttk.Entry(self.inputsFrame, validate='all', width=4, validatecommand=(VINcmd, '%P')), ttk.Label(self.inputsFrame, text="   Seconds: "), ttk.Entry(self.inputsFrame, validate='all', width=2, validatecommand=(VAMCcmd, '%P'))]

        self.updateVisibleWidgets()

        self.labelInputFrame.pack(pady=(0, 15), padx=(10,10))
        self.inputsFrame.pack(pady=(0, 15))

        self.createButton = tkinter.Button(self.root, text="Create", padx=5, pady=5, command=self.create)
        self.createButton.pack(padx=(0,0), pady=(0, 15))