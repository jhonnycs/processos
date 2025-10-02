
from fcfs import fcfs
from sjf import sjf
from round_robin import round_robin
from load_json import JsonData
from calc_metricas import Metricas

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

metricas.plot_tempos_espera()
metricas.plot_tempos_retorno()
metricas.plot_vazao()

# results_fcfs.plot_gantt_classic()
# results_sjf.plot_gantt_classic()

# for result in results_rr:
#     result.plot_gantt_classic()



