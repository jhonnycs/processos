import copy
from Process import Process
from collections import deque

def add_to_timeline(timeline, pid, start, end):
    # timeline = lista de eventos [{start, end, pid}, ...]
    # evita criar eventos duplicados do mesmo processo em sequência
    if timeline and timeline[-1]["pid"] == pid:
        timeline[-1]["end"] = end
    else:
        timeline.append({"pid": pid, "start": start, "end": end})

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
    timeline = []

    while lista_de_prontos or lista_de_espera:
        if not lista_de_prontos:
            next_arrival = lista_de_espera[0].arrival_time
            add_to_timeline(timeline, "IDLE", clock, next_arrival)
            clock = next_arrival
            while lista_de_espera and lista_de_espera[0].arrival_time <= clock:
                lista_de_prontos.append(lista_de_espera.popleft())
            quantum_count = 0
            continue

        # Executa o processo atual
        current = lista_de_prontos[0]
        current.remaining_time -= 1
        add_to_timeline(timeline, current.pid, clock, clock+1)
        clock += 1
        quantum_count += 1

        # será que chegou processo novo
        while lista_de_espera and lista_de_espera[0].arrival_time <= clock:
            lista_de_prontos.append(lista_de_espera.popleft())

        # Processo terminou
        if current.remaining_time == 0:
            current.completion_time = clock
            lista_de_prontos.popleft()
            if lista_de_prontos:  # troca de contexto apenas se houver próximo
                clock += context_switch_cost
                add_to_timeline(timeline, "CTX", clock - context_switch_cost, clock)
            quantum_count = 0

        # Quantum estourou
        elif quantum_count >= quantum:
            lista_de_prontos.append(lista_de_prontos.popleft())
            clock += context_switch_cost
            add_to_timeline(timeline, "CTX", clock - context_switch_cost, clock)
            quantum_count = 0

    return timeline
