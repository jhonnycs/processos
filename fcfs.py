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
            timeline.add_to_timeline(Timepoint("IDLE", clock, next_arrival))
            clock = next_arrival
            while lista_de_espera and lista_de_espera[0].arrival_time <= clock:
                lista_de_prontos.append(lista_de_espera.popleft())
            continue

        # Pega o processo atual (o mais antigo que chegou)
        current = lista_de_prontos.popleft()

        # Adiciona troca de contexto se não for o primeiro
        if timeline.time_list and timeline.get_last_timepoint().pid != current.pid:
            timeline.add_to_timeline(Timepoint("CTX", clock, clock + context_switch_cost))
            clock += context_switch_cost

        # Define start_time se ainda não tiver
        if current.start_time is None:
            current.start_time = clock

        # Executa o processo completamente
        timeline.add_to_timeline(Timepoint(current.pid, clock, clock + current.burst_time))
        clock += current.burst_time
        current.completion_time = clock

        # Checa chegada de novos processos durante a execução
        while lista_de_espera and lista_de_espera[0].arrival_time <= clock:
            lista_de_prontos.append(lista_de_espera.popleft())

    return timeline