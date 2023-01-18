from typing import Tuple

from job import Job
from heapq import heappush, heappop
import numpy as np
import math
import time


class Cpu:
    priority_queue = []
    roundrobinT1 = []
    roundrobinT2 = []
    fcfs = []

    def add_job(self, job: Job):
        heappush(self.priority_queue, job)

    def move_job_to_roundrobinT1(self):
        j = heappop(self.priority_queue)
        self.roundrobinT1.append(j)

    def move_to_next_queue(self, job: Job, queue: list):
        queues = [self.roundrobinT1, self.roundrobinT2, self.fcfs]
        index = queues.index(queue) + 1
        queue.remove(job)
        queues[index].append(job)

    def dispatcher(self):
        to_execute: Job = None
        threshold = None
        current_queue = None
        if len(self.roundrobinT1) != 0:
            to_execute = self.roundrobinT1.pop(0)
            threshold = T1
            current_queue = self.roundrobinT1
        elif len(self.roundrobinT2) != 0:
            to_execute = self.roundrobinT2.pop(0)
            threshold = T2
            current_queue = self.roundrobinT2
        elif len(self.fcfs) != 0:
            to_execute = self.fcfs.pop(0)

        to_execute.execute(1)
        if threshold is not None and to_execute.executed_time >= threshold:
            self.move_to_next_queue(to_execute, current_queue)

    def count_jobs_in_queues(self):
        return len(self.priority_queue) + len(self.roundrobinT1) + len(self.roundrobinT2)


TOTAL_TIME = 1000
TIME = 0
AVG_Y = 100
RATE_X = 10
LEN_K = 8
T1 = 5
T2 = 10


class Main:
    cpu = Cpu()
    next_job_arriving_at = 0

    def jobCreator(self) -> Tuple[Job, int]:
        interarrival_time = math.ceil(np.random.exponential(RATE_X))  # Or 1/X?
        service_time = math.ceil(np.random.poisson(AVG_Y))
        priority = np.random.choice([1, 2, 3], 1, p=[0.7, 0.2, 0.1])[0]
        j = Job(service_time, priority, TIME)
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
