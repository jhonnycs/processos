import statistics

def calcular_metricas(processes, tempo_final, throughput_window_T=None):
    tempos_espera = []
    tempos_retorno = []

    concluidos_ate_a_vazao = 0
    tempo_final_vazao = throughput_window_T if throughput_window_T else tempo_final

    for p in processes:
        if p.completion_time is not None and p.completion_time <= tempo_final_vazao:
            concluidos_ate_a_vazao += 1
        turnaround = p.completion_time - p.arrival_time
        waiting = turnaround - p.burst_time
        tempos_retorno.append(turnaround)
        tempos_espera.append(waiting)

    media_espera = statistics.mean(tempos_espera)
    desvio_espera = statistics.pstdev(tempos_espera)

    media_retorno = statistics.mean(tempos_retorno)
    desvio_retorno = statistics.pstdev(tempos_retorno)

    vazao = concluidos_ate_a_vazao / tempo_final_vazao

    return {
        "tempo_medio_espera": media_espera,
        "desvio_padrao_espera": desvio_espera,
        "tempo_medio_retorno": media_retorno,
        "desvio_padrao_retorno": desvio_retorno,
        "vazao": vazao
    }