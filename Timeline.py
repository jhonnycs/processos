class Timepoint:
    def __init__(self, pid, start, end):
        self.pid = pid
        self.start = start
        self.end = end


class Timeline:
    def __init__(self):
        self.time_list = []
        
    def add_to_timeline(self, time_point: Timepoint):
        if time_point.pid == self.get_last_timepoint.pid:
            self.get_last_timepoint().end = time_point.end
        else:
            self.time_list.append(time_point)

    def get_last_timepoint(self):
        return self.time_list[-1]