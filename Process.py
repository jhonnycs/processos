class Process:
    def __init__(self, pid, arrival_time, burst_time, time_unit=None):
        self.pid = pid
        self.time_unit = time_unit
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None

    def turnaround_time(self):
        """tempo de retorno"""
        return self.completion_time - self.arrival_time

    def waiting_time(self):
        """tempo de espera"""
        return self.turnaround_time() - self.burst_time

