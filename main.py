from job import Job
from heapq import heappush, heappop
import numpy as np
import math
import time

class Cpu:
    priority_queue = []
    roundrobinT1 = []
    roubrobinT2 = []
    fcfs = []

    def add_job(self, job: Job):
        heappush(self.priority_queue, job)


TOTAL_TIME = 1000
TIME = 0
AVG_Y = 100
RATE_X = 10
cpu = Cpu()

class Main:
    next_job_arriving_at = 0
    def jobCreator(self) -> tuple[Job, int]:
        interarrival_time = math.ceil(np.random.exponential(RATE_X)) # Or 1/X?
        service_time = math.ceil(np.random.poisson(AVG_Y))
        priority = np.random.choice([1,2,3], 1, p=[0.7, 0.2, 0.1])[0]
        j =  Job(service_time, priority, TIME)
        return j, interarrival_time
    
    def check_job_creation(self):
        if TIME == self.next_job_arriving_at:
            j, next_interarrival = self.jobCreator()
            cpu.add_job(j)
            self.next_job_arriving_at += next_interarrival
    
    def run_main_thread(self):
        for TIME in range(TOTAL_TIME):
            self.check_job_creation()