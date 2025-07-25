import sqlite3, os
from util import Alarm, Stopwatch, Timer, Timekeep
import util

class dbAccesser():
    def __init__(self):
        if not os.path.isfile("timekeeper.db"):
            self.con = sqlite3.connect("timekeeper.db")
            self.cur = self.con.cursor()

            self.cur.execute("CREATE TABLE timer(totalTime, timeLeft, paused)")
            self.cur.execute("CREATE TABLE alarm(timeTrigger, paused)")
            self.cur.execute("CREATE TABLE stopwatch(timeElapsed, paused)")

            self.con.commit()
        else:
            self.con = sqlite3.connect("timekeeper.db")
            self.cur = self.con.cursor()
    
    def addItem(self, item : Timekeep):
        print(item)
        if type(item) == Alarm:
            # self.cur.execute("SELECT * FROM alarm WHERE timeTrigger = "+str(item.timeTrigger))
            # for i in self.cur:
            #     return
            # # ^ duplicate checking (only for alarms bcs duplicate stopwatches and timers are fine)

            self.cur.execute("INSERT INTO alarm(timeTrigger, paused) values (?, ?)", (item.timeTrigger, item.paused))
        elif type(item) == Stopwatch:
            for i in self.cur:
                return
            self.cur.execute("INSERT INTO stopwatch(timeElapsed, paused) values (?, ?)", (item.timeElapsed, item.paused))
        elif type(item) == Timer:
            self.cur.execute("INSERT INTO timer(totalTime, timeLeft, paused) values (?, ?, ?)", (util.timerTimeTupleToString(item.totalTime), util.timerTimeTupleToString(item.timeLeft), item.paused))
        self.con.commit()

    def getTimekeeps(self):
        timekeeps = []

        for type in [("alarm", Alarm), ("stopwatch", Stopwatch), ("timer", Timer)]:
            self.cur.execute("SELECT * FROM "+type[0])
            for i in self.cur:
                if type[1] == Alarm:
                    timekeeps.append(type[1](
                        i[0], paused=i[1]
                    ))
                if type[1] == Timer:
                    if i[0] == i[1]:
                        timeL = (-1, -1)
                    else:
                        timeL = i[1]
                    timekeeps.append(type[1](
                        i[0], timeL, paused=i[2]
                    ))
                if type[1] == Stopwatch:
                    timekeeps.append(type[1](
                        paused=i[1], timeElapsed=i[0]
                    ))
        
        return timekeeps