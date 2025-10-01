from Process import Process
from fcfs import fcfs
from fjs import fjs
import json

with open("a.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

processos = []
for processo in dados["workload"]["processes"]:
    processos.append(
        Process(processo["pid"],
                 processo["arrival_time"],
                 processo["burst_time"]))
    
context_switch_cost = dados["metadata"]["context_switch_cost"]
results_fcfs = fcfs(processos, context_switch_cost)

for result in results_fcfs[0]:
    print(result)

fjs(processos, context_switch_cost)

timeline_fcfs = []
timeline_fjs = []