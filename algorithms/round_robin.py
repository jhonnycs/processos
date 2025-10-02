import copy
from models.Process import Process
from collections import deque
from models.Timeline import Timepoint
from models.Timeline import Timeline


def ja_passou_o_quantum(clock, quantum):
    return clock == quantum


def round_robin(processes: list[Process], context_switch_cost, quantum):
    procs = copy.deepcopy(processes)

    procs.sort(key=lambda x: x.arrival_time)
    clock = procs[0].arrival_time

    lista_de_prontos = deque()
    lista_de_espera = deque()

    for proc in procs:
        if proc.arrival_time <= clock:
            lista_de_prontos.append(proc)
        else:
            lista_de_espera.append(proc)

    quantum_count = 0
    timeline = Timeline("RR", quantum=quantum)

    while lista_de_prontos or lista_de_espera:
        if not lista_de_prontos:
            next_arrival = lista_de_espera[0].arrival_time
            timeline.add_to_timeline(Timepoint("IDLE", clock, next_arrival))
            clock = next_arrival
            while lista_de_espera and lista_de_espera[0].arrival_time <= clock:
                lista_de_prontos.append(lista_de_espera.popleft())
            quantum_count = 0
            continue

        current = lista_de_prontos[0]
        current.remaining_time -= 1
        timeline.add_to_timeline(Timepoint(current.pid, clock, clock + 1, current.arrival_time))
        clock += 1
        quantum_count += 1

        while lista_de_espera and lista_de_espera[0].arrival_time <= clock:
            lista_de_prontos.append(lista_de_espera.popleft())

        if current.remaining_time == 0:
            current.completion_time = clock
            lista_de_prontos.popleft()
            if lista_de_prontos:  # troca de contexto apenas se houver próximo
                clock += context_switch_cost
                timeline.add_to_timeline(Timepoint("CTX", clock - context_switch_cost, clock))
            quantum_count = 0

        elif quantum_count >= quantum:
            lista_de_prontos.append(lista_de_prontos.popleft())
            clock += context_switch_cost
            timeline.add_to_timeline(Timepoint("CTX", clock - context_switch_cost, clock))
            quantum_count = 0

    return timeline