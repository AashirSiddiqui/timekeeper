from enum import Enum
import math
from datetime import datetime

version = "1.0.0"

class TimekeepTypes(Enum):
    TIMER = 1
    STOPWATCH = 2
    ALARM = 3

class Timekeep():
    def __init__(self):
        self.type = "None"
    def setLabel(self, label):
        self.label = label

class Timer(Timekeep):
    def __init__(self, time, timeLeft=(-1,-1), paused=True):
        self.type = "Timer"
        self.totalTime = timerTimeStringToTuple(time)
        if timeLeft[0] == -1:
            self.timeLeft = timerTimeStringToTuple(time)
        else:
            self.timeLeft = timeLeft
        self.paused = paused
    
    def tick(self, timeFromLastTickSecs):
        if not self.paused:
            seconds = self.timeLeft[1]
            minutes = self.timeLeft[0]
            seconds -= timeFromLastTickSecs
            secondsLess = False

            if seconds < 0:
                seconds = 59 + seconds
                minutes -= 1
                secondsLess = True
            
            self.timeLeft = (minutes, seconds)
            if minutes < 0 and secondsLess:
                self.restart()
                return True
            else:
                return False

    def restart(self):
        self.timeLeft = self.totalTime

class Alarm(Timekeep):
    def __init__(self, time, paused=True):
        self.type = "Alarm"
        self.timeTrigger = time
        self.paused = paused
    def is_time(self):
        now = datetime.now()
        targetTime = clockTimeToTuple(str(self.timeTrigger))
        if now.hour == targetTime[0] and now.minute == targetTime[1]:
            return True
        else:
            return False

class Stopwatch(Timekeep):
    def __init__(self, timeElapsed = 0, paused=True):
        self.type = "Stopwatch"
        self.timeElapsed = timeElapsed
        self.paused = paused
    
    def tick(self, secondsSinceLastTick):
        if not self.paused:
            self.timeElapsed += secondsSinceLastTick
    
    def restart(self):
        self.timeElapsed = 0

# class Alarm(Timekeep):
#     pass

def basefloor(x, base=5):
    return base * math.floor(x/base)

def formatClockTime(time : str): # example time is 1930, output would be 7:30pm
    if len(time) == 3 or len(time) == 4:
        output = ""
        pm = False
        hours = int(time[:-2])
        if hours < 12:
            output += str(hours) + ":"
        elif hours == 12:
            output += str(hours) + ":"
            pm = True
        else:
            output += str(hours-12) + ":"
            pm = True
        output+= time[-2:]
        if (pm == True):
            output += " pm"
        else:
            output += " am"
        return output
    elif len(time) == 2: # this means it is 12 am and some minutes (>10)
        return "12:" + time + " am"
    elif len(time) == 1: # this means it is 12 am and no minutes or some minutes under ten
        return "12:0" + time + " am"
    else:
        print("invalid clock time int")
        return "INVALID TIME"
    
def clockTimeToTuple(time : str): # example time is 1930, output would be 7:30pm
    minutes = 0
    hours = 0
    if len(time) == 3 or len(time) == 4:
        pm = False
        hours = int(time[:-2])
        minutes = int(time[-2:])
    elif len(time) == 2: # this means it is 12 am and some minutes (>10)
        hours = 0
        minutes = int(time)
    elif len(time) == 1: # this means it is 12 am and no minutes or some minutes under ten
        hours = 0
        minutes = int(time)
    else:
        print("invalid clock time str")
        return "INVALID TIME"
    return (hours, minutes)

def formatTimerTimeTuple(time : tuple[int, int], abbreviate : bool = False): # (min, sec)
    minutes = int(time[0]) % 60
    minutes = str(minutes)
    hours = str(math.floor(int(time[0]) / 60))
    seconds = str(math.ceil(time[1]))

    output = ""
    zeroes = 0
    if abbreviate:
        if (hours != "0"):
            output = hours + " hr "
        else:
            zeroes += 1
        if (minutes != "0"):
            output += minutes + " min " 
        else:
            zeroes += 1
        if (seconds != "0"):
            output += seconds + " sec "
        else:
            zeroes += 1
            if (zeroes == 3):
                output = " 0 sec "
    else:
        if (hours != "0"):
            output = hours + " hours "
        else:
            zeroes += 1
        if (minutes != "0"):
            output += minutes + " minutes " 
        else:
            zeroes += 1
        if (seconds != "0"):
            output += seconds + " seconds "
        else:
            zeroes += 1
            if (zeroes == 3):
                output = " 0 seconds "

    output = output[:-1] # removes trailing space
    return output

def timerTimeTupleToString(time : tuple[int, int]): # eg input:(5, 30) output:"5|30"
    return str(time[0])+"|"+str(time[1])

def timerTimeStringToTuple(time : str) -> tuple[int, int]: # eg input:"5|30" ouput:(5, 30)
    inputSplit = time.split("|")
    return (int(inputSplit[0]), int(inputSplit[1]))

def clockTimeIntSeparated(time : int) -> tuple[int, int]: # example time is 1930, output would be (19, 30)
    pass