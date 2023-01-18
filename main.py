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
    

    def move_job_to_roundrobinT1(self):
        j = heappop(self.priority_queue)
        self.roundrobinT1.append(j)

    
    def dispatcher(self):
        to_execute :Job = None
        if len(self.roundrobinT1) != 0:
            to_execute = self.roubrobinT1.pop(0)
        elif len(self.roubrobinT2) != 0:
            to_execute = self.roubrobinT2.pop(0)
        elif len(self.fcfs) != 0:
            to_execute = self.fcfs.pop(0)
        # Execute the job
        pass
    

    def count_jobs_in_queues(self):
        return len(self.priority_queue) + len(self.roundrobinT1) + len(self.roubrobinT2)


TOTAL_TIME = 1000
TIME = 0
AVG_Y = 100
RATE_X = 10
LEN_K = 8

class Main:
    cpu = Cpu()
    next_job_arriving_at = 0
    def jobCreator(self) -> tuple[Job, int]:
        interarrival_time = math.ceil(np.random.exponential(RATE_X)) # Or 1/X?
        service_time = math.ceil(np.random.poisson(AVG_Y))
        priority = np.random.choice([1,2,3], 1, p=[0.7, 0.2, 0.1])[0]
        j =  Job(service_time, priority, TIME)
        return j, interarrival_time
    

    def jobLoader(self):
        if self.cpu.count_jobs_in_queues() < LEN_K:
            for i in range(LEN_K):
                self.cpu.move_job_to_roundrobinT1()
    
    def check_job_creation(self):
        if TIME == self.next_job_arriving_at:
            j, next_interarrival = self.jobCreator()
            self.cpu.add_job(j)
            self.next_job_arriving_at += next_interarrival

    
    def run_main_thread(self):
        for TIME in range(TOTAL_TIME):
            self.check_job_creation()
            self.jobLoader()
            self.cpu.dispatcher()