# Timeline.py
from dataclasses import dataclass

@dataclass
class Timepoint:
    pid: str
    start: int
    end: int

class Timeline:
    def __init__(self):
        self.time_list = []

    def has_timepoints(self) -> bool:
        return len(self.time_list) > 0

    def get_last_timepoint(self):
        if not self.time_list:
            return None
        return self.time_list[-1]

    def add_to_timeline(self, time_point: Timepoint):
        last = self.get_last_timepoint()

        if last is None:
            self.time_list.append(time_point)
            return

        if time_point.pid == last.pid:
            if time_point.end > last.end:
                last.end = time_point.end
            return


        self.time_list.append(time_point)
