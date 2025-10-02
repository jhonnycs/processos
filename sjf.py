
def sjf(procs, context_switch_cost):
    procs = sorted(procs, key=lambda x: x.arrival_time)

    time = 0
    ready_queue = []
    finished = []
    timeline = []
    current = None
    remaining_burst = 0
    last_finished_time = None
    last_finished_pid = None

    while procs or ready_queue or current:
        arriving = [p for p in procs if p.arrival_time == time]

        for p in arriving:
            ready_queue.append(p)

        procs = [p for p in procs if p.arrival_time > time]

        if not current and ready_queue:
            current = min(ready_queue, key=lambda x: x.burst_time)
            ready_queue.remove(current)
            remaining_burst = current.burst_time


            if last_finished_time == time and context_switch_cost > 0:
                time += context_switch_cost

            start = time
            timeline.append({"pid": current.pid, "start": start})

        if current:
            remaining_burst -= 1
            if remaining_burst == 0:
                end = time + 1
                timeline[-1]["end"] = end
                finished.append(current)
                current = None
                last_finished_time = end

        time += 1

    return timeline


