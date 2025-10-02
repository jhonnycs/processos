from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.round_robin import round_robin
from load_json import JsonData
from models.Metricas import Metricas

a = JsonData("b.json")
metricas = Metricas()

results_fcfs = fcfs(a.processes, a.context_switch_cost)
results_sjf = sjf(a.processes, a.context_switch_cost)

metricas.adicionar("FCFS" ,results_fcfs)
metricas.adicionar("SJF",results_sjf)

results_rr = []
for q in a.rr_quantums:
    results_rr.append(round_robin(a.processes, a.context_switch_cost, q))


for result in results_rr:
    metricas.adicionar(f"RR - {result.quantum}", result)

# metricas.plot_tempos_espera()
# metricas.plot_tempos_retorno()
# metricas.plot_vazao()

results_fcfs.plot_gantt_classic()
# results_sjf.plot_gantt_classic()
#results_fcfs.show_timeline()

# for result in results_rr:
#     result.plot_gantt_classic()

