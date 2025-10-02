import copy
from collections import deque
from Timeline import Timeline
from Timeline import Timepoint

def fcfs(processes, context_switch_cost):
    procs = copy.deepcopy(processes)
    procs.sort(key=lambda x: x.arrival_time)

    clock = procs[0].arrival_time
    lista_de_prontos = deque()
    lista_de_espera = deque()
    timeline = Timeline()

    for proc in procs:
        if proc.arrival_time <= clock:
            lista_de_prontos.append(proc)
        else:
            lista_de_espera.append(proc)

    while lista_de_prontos or lista_de_espera:

        if not lista_de_prontos:
            next_arrival = lista_de_espera[0].arrival_time
            timeline.add_to_timeline(Timepoint("IDLE", clock, next_arrival))
            clock = next_arrival
            while lista_de_espera and lista_de_espera[0].arrival_time <= clock:
                lista_de_prontos.append(lista_de_espera.popleft())
            continue

        current = lista_de_prontos.popleft()

        if timeline.time_list and timeline.get_last_timepoint().pid != current.pid:
            timeline.add_to_timeline(Timepoint("CTX", clock, clock + context_switch_cost))
            clock += context_switch_cost

        if current.start_time is None:
            current.start_time = clock

        timeline.add_to_timeline(Timepoint(current.pid, clock, clock + current.burst_time))
        clock += current.burst_time
        current.completion_time = clock

        while lista_de_espera and lista_de_espera[0].arrival_time <= clock:
            lista_de_prontos.append(lista_de_espera.popleft())

    return timeline