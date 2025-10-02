import copy
from collections import deque
from Timeline import Timeline
from Timeline import Timepoint

def fcfs(processes, context_switch_cost):
    procs = copy.deepcopy(processes)
    procs.sort(key=lambda x: x.arrival_time)

    clock = procs[0].arrival_time
    ready_queue = deque()
    wait_queue = deque()
    timeline = Timeline("FCFS")

    for proc in procs:
        if proc.arrival_time <= clock:
            ready_queue.append(proc)
        else:
            wait_queue.append(proc)

    while ready_queue or wait_queue:

        if not ready_queue:
            next_arrival = wait_queue[0].arrival_time
            timeline.add_to_timeline(Timepoint("IDLE", clock, next_arrival))
            clock = next_arrival
            while wait_queue and wait_queue[0].arrival_time <= clock:
                ready_queue.append(wait_queue.popleft())
            continue

        current = ready_queue.popleft()

        if timeline.time_list and timeline.get_last_timepoint().pid != current.pid:
            timeline.add_to_timeline(Timepoint("CTX", clock, clock + context_switch_cost))
            clock += context_switch_cost

        if current.start_time is None:
            current.start_time = clock

        timeline.add_to_timeline(Timepoint(current.pid, clock, clock + current.burst_time, current.arrival_time))
        clock += current.burst_time
        current.completion_time = clock

        while wait_queue and wait_queue[0].arrival_time <= clock:
            ready_queue.append(wait_queue.popleft())

    return timeline