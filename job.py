import enum


class JOB_PRIORITY(enum.Enum):
    Low = 1
    Normal = 2
    High = 3


LAST_ID = 1


class Job:
    id = None
    creation_time = None
    service_time: int = None
    executed_time: int = 0
    priority: JOB_PRIORITY = None

    def execute(self, time):
        self.executed_time += time

    def time_remaining(self) -> int:
        return self.service_time - self.executed_time

    def is_finished(self):
        return self.time_remaining() <= 0

    def done_percent(self):
        return self.executed_time / self.service_time

    def __init__(self, service_time, priority, creation_time) -> None:
        global LAST_ID
        self.service_time = service_time
        self.priority = priority
        self.creation_time = creation_time
        self.id = LAST_ID
        self.enters = {"RoundRobinT1":0, "RoundRobinT2": 0, "FCFS": 0}
        self.leaves = {"RoundRobinT1":0, "RoundRobinT2": 0, "FCFS": 0}
        LAST_ID += 1

    def __lt__(self, o):
        if self.priority != o.priority:
            return self.priority > o.priority
        elif self.creation_time != o.creation_time:
            return self.creation_time < o.creation_time
        return False

    def __eq__(self, o):
        if o is not None:
            if self.priority == o.priority:
                return self.creation_time == o.creation_time
        return False

    def __str__(self) -> str:
        return f"{self.id}"
        # return f"{self.creation_time}. st: {self.service_time}, pr: {self.priority}"
