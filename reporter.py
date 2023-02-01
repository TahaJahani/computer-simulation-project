import statistics
import matplotlib.pyplot as plt
import numpy as np


class Reporter:

    def ecdf(self, a):
        x, counts = np.unique(a, return_counts=True)
        cusum = np.cumsum(counts)
        return x, cusum / cusum[-1]
    
    def plot_ecdf(self, a, pos, cap):
        ax = self.fig.add_subplot(pos)
        x, y = self.ecdf(a)
        x = np.insert(x, 0, x[0])
        y = np.insert(y, 0, 0.)
        ax.plot(x, y, drawstyle='steps-post')
        ax.grid(True)
        ax.set_xlabel('$Time$')
        ax.set_ylabel('$F$')
        ax.set_title(cap)
    
    def __init__(self):
        self.fcfs_len = list()
        self.rr1_len = list()
        self.rr2_len = list()
        self.timeouts = list()
        
    def capture_len(self, cpu):
        self.fcfs_len.append(len(cpu.fcfs))
        self.rr1_len.append(len(cpu.roundrobinT1))
        self.rr2_len.append(len(cpu.roundrobinT2))

    def calculate_len_avg(self):
        rr1_len_avg = statistics.mean(self.rr1_len)
        rr2_len_avg = statistics.mean(self.rr2_len)
        fcfs_len_avg = statistics.mean(self.fcfs_len)
        return f'average length of each queue is as follows:\nRR1: {rr1_len_avg}\nRR2: {rr2_len_avg}\nfcfs: {fcfs_len_avg}'
    
    def draw_wait_plot(self, rr1_list, rr2_list, fcfs_list):
        self.fig = plt.figure()
        if len(rr1_list) > 0:
            xvec = np.array(rr1_list)
            self.plot_ecdf(xvec, 131, "RR1")

        if len(rr2_list) >0:
            xvec = np.array(rr2_list)
            self.plot_ecdf(xvec, 132, "RR2")

        if len (fcfs_list) > 0:
            xvec = np.array(fcfs_list)
            self.plot_ecdf(xvec, 133, "FCFS")    

        plt.show()
        return

    def calculate_job_timers(job, time: int):
        rr1_time_j, rr2_time_j, fcfs_time_j = 0,0,0
        if job.enters["RoundRobinT1"] != 0:
            if job.leaves["RoundRobinT1"] != 0:
                rr1_time_j = job.leaves["RoundRobinT1"] - job.enters["RoundRobinT1"]
            else:
                rr1_time_j = time - job.enters["RoundRobinT1"]

        if job.enters["RoundRobinT2"] != 0:
            if job.leaves["RoundRobinT2"] != 0:
                rr2_time_j = job.leaves["RoundRobinT2"] - job.enters["RoundRobinT2"]
            else:
                rr2_time_j = time - job.enters["RoundRobinT2"]

        if job.enters["FCFS"] != 0:
            if job.leaves["FCFS"] != 0:
                fcfs_time_j = job.leaves["FCFS"] - job.enters["FCFS"]
            else:
                fcfs_time_j = time - job.enters["FCFS"]

        return rr1_time_j, rr2_time_j, fcfs_time_j
        
    def calculate_spent_time_queues(self, jobs, time:int):

        rr1_list = list()
        rr2_list = list()
        fcfs_list = list()
        rr1_sum = 0
        rr2_sum = 0
        fcfs_sum = 0

        for job in jobs:
            rr1_time_j, rr2_time_j, fcfs_time_j = Reporter.calculate_job_timers(job, time)
            if rr1_time_j != 0:
                rr1_list.append(rr1_time_j)
                rr1_sum += rr1_time_j
            if rr2_time_j != 0:
                rr2_list.append(rr2_time_j)
                rr2_sum += rr2_time_j
            if fcfs_time_j != 0:
                fcfs_list.append(fcfs_time_j)
                fcfs_sum += fcfs_time_j
        
        if len(rr1_list) == 0:
            print("no job entered RR1")
        else:
            print(f'average time spent in RR1 is {round(rr1_sum / len(rr1_list), 2)}')
        if len(rr2_list) == 0:
            print("no job entered RR2")
        else:
            print(f'average time spent in RR2 is {round(rr2_sum / len(rr2_list), 2)}')
        if len(fcfs_list) == 0:
            print("no job entered RR1")
        else:
            print(f'average time spent in FCFS is {round(fcfs_sum / len(fcfs_list), 2)}')
        self.draw_wait_plot(rr1_list=rr1_list, rr2_list=rr2_list, fcfs_list= fcfs_list)

    def note_timeout(self, time: int):
        self.timeouts.append(time)
    
    def calculate_timeouts(self):
        self.fig = plt.figure()
        print(f'a total of {len(self.timeouts)} jobs timed out...')
        if len (self.timeouts) > 0:
            xvec = np.array(self.timeouts)
            self.plot_ecdf(xvec, 111, "timeouts")    
            plt.show()
        return
        
    def export(self, total_clocks, cpu, jobs, bonus):
        print(self.calculate_len_avg())
        utilization = "%.2f" % (1-(cpu.idle_clocks/total_clocks))
        print(f'cpu utilization was {utilization}')
        self.calculate_spent_time_queues(jobs=jobs, time=total_clocks)
        if bonus == 1: self.calculate_timeouts()
        print("done")
        
