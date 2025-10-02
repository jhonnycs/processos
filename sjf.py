from Process import Process

def sjf(procs, context_switch_cost):
    procs = sorted(procs, key=lambda x: x.arrival_time)

    time = 0
    ready_queue = []
    finished = []
    timeline = []
    current = None
    remaining_burst = 0

    while procs or ready_queue or current:
        arriving = [p for p in procs if p.arrival_time == time]

        for p in arriving:
            ready_queue.append(p)

        procs = [p for p in procs if p.arrival_time > time]

        if not current and ready_queue:
            current = min(ready_queue, key=lambda x: x.burst_time)
            ready_queue.remove(current)
            remaining_burst = current.burst_time
            start = time
            timeline.append({"pid": current.pid, "start": start})

        if current:
            remaining_burst -= 1
            if remaining_burst == 0:
                end = time + 1
                timeline[-1]["end"] = end
                finished.append(current)
                current = None

        time += 1

    print("Timeline:", timeline)
    return timeline


