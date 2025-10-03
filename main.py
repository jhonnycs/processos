from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.round_robin import round_robin
from load_json import JsonData
from models.Metricas import Metricas

def main(json):
    a = JsonData(json)
    metricas = Metricas()

    results_fcfs = fcfs(a.processes, a.context_switch_cost)
    results_sjf = sjf(a.processes, a.context_switch_cost)

    metricas.adicionar("FCFS" ,results_fcfs, throughput_window_T=a.throughput_window_T)
    metricas.adicionar("SJF",results_sjf, throughput_window_T=a.throughput_window_T)

    results_rr = []
    for q in a.rr_quantums:
        results_rr.append(round_robin(a.processes, a.context_switch_cost, q))

    for result in results_rr:
        metricas.adicionar(f"RR - {result.quantum}", result, throughput_window_T=a.throughput_window_T)

    results_fcfs.plot_gantt_classic()
    results_sjf.plot_gantt_classic()
    for r in results_rr:
        r.plot_gantt_classic()

    metricas.show_metricas_de_todos()
    metricas.plot_tempos_espera()
    metricas.plot_tempos_retorno()
    metricas.plot_vazao()
    metricas.plot_todos()

main("c.json")
#main("d.json")
# main("e.json")
# main("f.json")