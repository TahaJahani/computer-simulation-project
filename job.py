import enum


class JOB_PRIORITY(enum.Enum):
    Low=1
    Normal=2
    High=3

class Job:
    start_time=None
    service_time: int=None
    priority: JOB_PRIORITY=None

    def __init__(self, service_time, priority) -> None:
        self.service_time = service_time
        self.priority = priority
    