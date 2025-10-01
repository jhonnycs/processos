import copy

def add_to_timeline(timeline, pid, start, end):
    # timeline = lista de eventos [{start, end, pid}, ...]
    # evita criar eventos duplicados do mesmo processo em sequência
    if timeline and timeline[-1]["pid"] == pid:
        timeline[-1]["end"] = end
    else:
        timeline.append({"pid": pid, "start": start, "end": end})


def fcfs(processes, context_switch_cost):
    procs = copy.deepcopy(processes)

    timeline = [] # {"pid": "P01", "start": 0, "end": 5},
    time = 0

    procs.sort(key=lambda x: x.arrival_time)

    for i, p in enumerate(procs):
    # se o processo ainda não chegou, avança o relógio
        if time < p.arrival_time:
            time = p.arrival_time
    
        if i > 0:
            add_to_timeline(timeline, "CTX", time, time + context_switch_cost)
            time += context_switch_cost
    

        if p.start_time is None:
            p.start_time = time
        
        add_to_timeline(timeline, p.pid, time, time + p.burst_time)
        time += p.burst_time

        p.completion_time = time

    return timeline, procs