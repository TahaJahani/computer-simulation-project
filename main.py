from job import Job
from heapq import heappush, heappop
import numpy as np
import math

TIME = 0
AVG_Y = 100

class Cpu:
    priority_queue = []
    roundrobinT1 = []
    roubrobinT2 = []
    fcfs = []

    def add_job(self, job: Job):
        heappush(self.priority_queue, job)

class Main:
    def jobCreator(self) -> Job:
        service_time = math.ceil(np.random.poisson(AVG_Y))
        priority = np.random.choice([1,2,3], 1, p=[0.7, 0.2, 0.1])[0]
        return Job(service_time, priority, TIME)