import enum


class JOB_PRIORITY(enum.Enum):
    Low=1
    Normal=2
    High=3

class Job:
    creation_time = None
    start_time = None
    service_time:int = None
    priority: JOB_PRIORITY = None

    def __init__(self, service_time, priority, creation_time) -> None:
        self.service_time = service_time
        self.priority = priority
        self.creation_time = creation_time
    
    def __lt__(self, o):
        if self.priority != o.priority:
            return self.priority > o.priority
        elif self.creation_time != o.creation_time:
            return self.creation_time < o.creation_time
        return False
    
    def __eq__(self, o):
        if self.priority == o.priority:
            return self.creation_time == o.creation_time
        return False
    

    def __str__(self) -> str:
        return f"{self.creation_time}. st: {self.service_time}, pr: {self.priority}"
