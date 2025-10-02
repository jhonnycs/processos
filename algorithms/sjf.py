from Timeline import Timeline
from Timeline import Timepoint

def sjf(procs, context_switch_cost):
    procs = sorted(procs, key=lambda x: x.arrival_time)

    time = 0
    ready_queue = []
    finished = []
    timeline = Timeline("SJF")

    current = None
    current_remaining = 0

    switching = False
    switch_remaining = 0

    while procs or ready_queue or current or switching:

        arriving = [p for p in procs if p.arrival_time == time]
        for p in arriving:
            ready_queue.append(p)
        procs = [p for p in procs if p.arrival_time > time]


        if current is not None:
            current_remaining -= 1

            time += 1

            if current_remaining == 0:
                end = time
                timeline.get_last_timepoint().end = end
                finished.append(current)
                current = None

                if ready_queue and context_switch_cost and context_switch_cost > 0:
                    switching = True
                    switch_remaining = context_switch_cost

            continue

        if switching:
            switch_remaining -= 1
            time += 1

            if switch_remaining == 0:
                switching = False
                timeline.get_last_timepoint().end = time

                if ready_queue:

                    current = min(ready_queue, key=lambda x: x.burst_time)
                    ready_queue.remove(current)
                    current_remaining = current.burst_time
                    timeline.add_to_timeline(Timepoint(current.pid, time,  None))
            continue

        if current is None and ready_queue:

            current = min(ready_queue, key=lambda x: x.burst_time)
            ready_queue.remove(current)
            current_remaining = current.burst_time
            timeline.add_to_timeline(Timepoint(current.pid, time,  None))
            continue

        time += 1


    return timeline