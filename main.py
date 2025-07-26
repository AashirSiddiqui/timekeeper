import tkinter, math, util
from tkinter import ttk, font
from util import Alarm, Stopwatch, Timer
from database import dbAccesser
import timekeep_windows as tkw
from functools import partial
from time import sleep

def openAlarmWindow(alarmInstance):
    tkw.AlarmWindow(root, alarmInstance)

def openTimerWindow(timerInstance):
    tkw.TimerWindow(root, timerInstance)

def openStopwatchWindow(stopwatchInstance):
    tkw.StopwatchWindow(root, stopwatchInstance=stopwatchInstance)

def openCreateTimekeepGUI():
    createWin = tkw.CreateTimekeepWindow(root)
    createWin.onDeath = partial(whenCreateTimekeepDestroyed, createWin)

def whenCreateTimekeepDestroyed(createWin):
    updateBtnFrame()
    createWin.root.destroy()

def deleteTimekeep(firstVal, type, _):
    print(firstVal)
    print(type)
    type = type.lower()
    access = dbAccesser()
    access.removeItem(firstVal, type)
    updateBtnFrame()

def updateBtnFrame(loop = False):
    global btnFrame, timekeeps

    # print("updating btnframe")

    db = dbAccesser()
    oldtimekeeplen = len(timekeeps)
    timekeeps = db.getTimekeeps()
    for child in btnFrame.winfo_children():
        child.destroy()

    buttons = []
    for i in range(len(timekeeps)): # wrapping timekeep display
        thisTimekeep = timekeeps[i]
        row = math.floor(i/(3))
        column = i - util.basefloor(i, base=3)
        buttons.append(0)
        if (type(thisTimekeep) == Alarm):
            firstVal = thisTimekeep.timeTrigger
            buttons[i] = tkinter.Button(btnFrame, text=thisTimekeep.type+" "+util.formatClockTime(str(thisTimekeep.timeTrigger)), command=partial(openAlarmWindow,thisTimekeep))
        elif (type(thisTimekeep) == Timer):
            firstVal = util.timerTimeTupleToString(thisTimekeep.timeLeft)
            buttons[i] = tkinter.Button(btnFrame, text=thisTimekeep.type+" "+util.formatTimerTimeTuple(thisTimekeep.totalTime, abbreviate=True), command=partial(openTimerWindow,thisTimekeep))
        else:
            firstVal = thisTimekeep.timeElapsed
            buttons[i] = tkinter.Button(btnFrame, text=thisTimekeep.type, command=partial(openStopwatchWindow,thisTimekeep))
        buttons[i].grid(row = row, column = column, padx=(0, 10), pady=(0, 10))
        buttons[i].bind("<Button-2>", partial(deleteTimekeep, firstVal, thisTimekeep.type))
    
    if loop:
        root.after(60000, updateBtnFrame)

root = tkinter.Tk()
root.title("Timekeeper v" + util.version)
root.geometry("600x500")

buttonFont = font.Font(font="", size=25)
timekeeps = []

header = tkinter.Frame(root)
tkinter.Label(header, text="Timekeeper", font=("Yrsa", 25)).grid(pady=(20, 20), column=1, row=1)
tkinter.Button(header, text="Refresh", command=updateBtnFrame).grid(padx=(20, 20), column=2, row=1)
header.pack()

btnFrame = ttk.Frame(root)
updateBtnFrame(loop=True)
btnFrame.pack(pady=(0, 15), padx=(20, 20))

createTimekeepButton = tkinter.Button(root, text="Create Timekeep", font=('15'), bg="black", fg="white", command=openCreateTimekeepGUI)
createTimekeepButton.pack(pady=(0, 20), padx=(20,20))

print(util.formatClockTime(str(2020)))

# sv_ttk.set_theme("dark")
root.mainloop()