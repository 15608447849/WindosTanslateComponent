#encoding:utf-8
import psutil, time
import threading
import datetime

class Monitor(threading.Thread):
    def __init__(self):
        super().__init__(name="wtc_monitor")
        self.start()

    def run(self):
        while(True):
            self.getProcessAllInfo()
            time.sleep(10)

    def getProcessAllInfo(self):
        proc_list = psutil.pids()

        for it in proc_list:
            self.getSingerProc(it)

    def getSingerProc(self, pid):
        p = psutil.Process(pid)
        if p.name() == "wtc.exe":
            info = [p.name(),
                    p.pid,
                    p.ppid(),
                    # p.parent(),
                    # p.exe(),
                    # p.cwd(),
                    # p.username(),
                    # p.status(),
                    datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
                    # p.uids(),
                    # p.gids(),
                    # p.cpu_times(),
                    # p.memory_percent(),
                    # p.memory_info(),
                    # p.io_counters(),
                    p.num_threads(),
                    p.connections()
                    ]
            print(info)









