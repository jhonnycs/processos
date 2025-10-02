import copy
from collections import deque

def add_to_timeline(timeline, pid, start, end):
    # timeline = lista de eventos [{start, end, pid}, ...]
    # evita criar eventos duplicados do mesmo processo em sequência
    if timeline and timeline[-1]["pid"] == pid:
        timeline[-1]["end"] = end
    else:
        timeline.append({"pid": pid, "start": start, "end": end})


def fcfs(processes, context_switch_cost):
    procs = copy.deepcopy(processes)
    procs.sort(key=lambda x: x.arrival_time)

    clock = procs[0].arrival_time
    lista_de_prontos = deque()
    lista_de_espera = deque()
    timeline = []

    # Inicializa a fila de espera
    for proc in procs:
        if proc.arrival_time <= clock:
            lista_de_prontos.append(proc)
        else:
            lista_de_espera.append(proc)

    while lista_de_prontos or lista_de_espera:

        # Se não houver processo pronto, CPU fica ociosa até o próximo
        if not lista_de_prontos:
            next_arrival = lista_de_espera[0].arrival_time
            add_to_timeline(timeline, "IDLE", clock, next_arrival)
            clock = next_arrival
            while lista_de_espera and lista_de_espera[0].arrival_time <= clock:
                lista_de_prontos.append(lista_de_espera.popleft())
            continue

        # Pega o processo atual (o mais antigo que chegou)
        current = lista_de_prontos.popleft()

        # Adiciona troca de contexto se não for o primeiro
        if timeline and timeline[-1]["pid"] != current.pid:
            add_to_timeline(timeline, "CTX", clock, clock + context_switch_cost)
            clock += context_switch_cost

        # Define start_time se ainda não tiver
        if current.start_time is None:
            current.start_time = clock

        # Executa o processo completamente
        add_to_timeline(timeline, current.pid, clock, clock + current.burst_time)
        clock += current.burst_time
        current.completion_time = clock

        # Checa chegada de novos processos durante a execução
        while lista_de_espera and lista_de_espera[0].arrival_time <= clock:
            lista_de_prontos.append(lista_de_espera.popleft())

    return timeline