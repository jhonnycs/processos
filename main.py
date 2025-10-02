
from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.round_robin import round_robin
from load_json import load_processes, get_switch_cost
from models.Metricas import Metricas

processes = load_processes()
context_switch_cost = get_switch_cost()

results_fcfs = fcfs(processes, context_switch_cost)
results_sjf = sjf(processes, context_switch_cost)
print(results_sjf)
results_rr = round_robin(processes, context_switch_cost, 2)

metricas_sjf = Metricas(results_sjf)
print("Métricas SJF:", metricas_sjf.to_dict())

# Plots (aparecerão em jupyter/ambiente gráfico)
metricas_sjf.plot_tempos()       # mostra gráfico
metricas_sjf.plot_vazao()        # mostra gráfico
metricas_sjf.plot_timeline()     # mostra timeline

# Se estiver rodando em servidor sem display, salve em arquivo:
metricas_sjf.plot_timeline(show=False, save_path="timeline_sjf.png")
metricas_sjf.plot_tempos(show=False, save_path="tempos_sjf.png")