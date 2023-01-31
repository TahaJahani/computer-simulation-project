from typing import Tuple

import display
from job import Job
from reporter import Reporter
from heapq import heappush, heappop
import numpy as np
import math
import time
import pygame


class Cpu:
    priority_queue = []
    roundrobinT1 = []
    roundrobinT2 = []
    fcfs = []
    idle_clocks = 0

    to_execute: Job = None

    def get_job_by_id(self, job_id: int) -> Job:
        for queue in [self.priority_queue, self.roundrobinT1, self.roundrobinT2, self.fcfs]:
            for item in queue:
                if item.id == job_id:
                    return item

    def add_job(self, job: Job):
        heappush(self.priority_queue, job)

    def move_job_to_roundrobinT1(self, time: int):
        if len(self.priority_queue) > 0:
            j = heappop(self.priority_queue)
            self.roundrobinT1.append(j)
            j.enters["RoundRobinT1"] = time

    def move_to_next_queue(self, job: Job, queue: list, time: int):
        queues = [self.roundrobinT1, self.roundrobinT2, self.fcfs]
        index = queues.index(queue) + 1
        queue.remove(job)
        queues[index].append(job)
        if index == 1:
            job.leaves["RoundRobinT1"] = time
            job.enters["RoundRobinT2"] = time
        else:
            job.leaves["RoundRobinT2"] = time
            job.enters["FCFS"] = time

    def job_finished(self, job):
        if job in self.roundrobinT1:
            self.roundrobinT1.remove(job)
        elif job in self.roundrobinT2:
            self.roundrobinT2.remove(job)
        elif job in self.fcfs:
            self.fcfs.remove(job)

    def dispatcher(self):
        self.to_execute = None
        threshold = None
        current_queue = None
        current_queue_name = None
        if len(self.roundrobinT1) != 0:
            self.to_execute = self.roundrobinT1[0]
            threshold = T1
            current_queue = self.roundrobinT1
            current_queue_name = "RoundRobinT1"
        elif len(self.roundrobinT2) != 0:
            self.to_execute = self.roundrobinT2[0]
            threshold = T2
            current_queue = self.roundrobinT2
            current_queue_name = "RoundRobinT2"
        elif len(self.fcfs) != 0:
            self.to_execute = self.fcfs[0]
            current_queue_name = "FCFS"

        if self.to_execute is not None:
            print(f"Executing job {self.to_execute} from queue {current_queue_name}...", end="")
            self.to_execute.execute(1)
            if threshold is not None and self.to_execute.executed_time >= threshold:
                print("job moved to next queue", end="")
                self.move_to_next_queue(self.to_execute, current_queue, time= TIME)
            elif self.to_execute.is_finished():
                self.job_finished(self.to_execute)
                print("job finished!", end="")
            print("")
        else:
            self.idle_clocks += 1

    def count_jobs_in_queues(self):
        return len(self.fcfs) + len(self.roundrobinT1) + len(self.roundrobinT2)


TOTAL_TIME = 100
TIME = 0
AVG_Y = 15
RATE_X = 15
LEN_K = 8
T1 = 10
T2 = 15


class Main:
    cpu = Cpu()
    next_job_arriving_at = 0
    jobs = list()

    def jobCreator(self) -> Tuple[Job, int]:
        interarrival_time = math.ceil(np.random.exponential(RATE_X))  # Or 1/X?
        service_time = math.ceil(np.random.poisson(AVG_Y))
        priority = np.random.choice([1, 2, 3], 1, p=[0.7, 0.2, 0.1])[0]
        j = Job(service_time, priority, TIME)
        Main.jobs.append(j)
        return j, interarrival_time

    def jobLoader(self):
        if self.cpu.count_jobs_in_queues() < LEN_K:
            for i in range(LEN_K):
                self.cpu.move_job_to_roundrobinT1(TIME)

    def check_job_creation(self):
        if TIME == self.next_job_arriving_at:
            j, next_interarrival = self.jobCreator()
            self.cpu.add_job(j)
            self.next_job_arriving_at += next_interarrival
            print(f"Job Created. Next job at {self.next_job_arriving_at}")

    def render_display(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                job_id = display.check_collision()
                display.select_job(self.cpu.get_job_by_id(job_id))

        display.reset_screen()
        display.get_queue_rects()
        for index, item in enumerate(self.cpu.priority_queue):
            display.get_job_rect("priority_queue", item, index)

        for index, item in enumerate(self.cpu.roundrobinT1):
            display.get_job_rect("roundRobinT1_queue", item, index)

        for index, item in enumerate(self.cpu.roundrobinT2):
            display.get_job_rect("roundRobinT2_queue", item, index)

        for index, item in enumerate(self.cpu.fcfs):
            display.get_job_rect("fcfs_queue", item, index)
        display.show_text_data(TIME, self.next_job_arriving_at)
        display.update_screen()

    def run_main_thread(self):
        global TIME
        for TIME in range(TOTAL_TIME):
            reporter.capture_len(self.cpu)
            print(f"{TIME}. Tick")
            self.check_job_creation()
            self.jobLoader()
            self.cpu.dispatcher()
            self.render_display()
            time.sleep(0.25)

    def start_program(self):
        global TOTAL_TIME, AVG_Y, RATE_X, LEN_K, T1, T2
        TOTAL_TIME = int(input("Enter Total Time: "))
        AVG_Y = int(input("Enter Y: "))
        RATE_X = int(input("Enter X: "))
        LEN_K = int(input("Enter K: "))
        T1 = int(input("Enter T1: "))
        T2 = int(input("Enter T2: "))
        display.initialize_display()
        self.run_main_thread()


main = Main()
reporter = Reporter()
main.start_program()
reporter.export(total_clocks=TOTAL_TIME, cpu=main.cpu, jobs=Main.jobs)
