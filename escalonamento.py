import Process
import json

with open("a.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

processos = []
for processo in dados["workload"]["processes"]:
    processos.append(
        Process(processo["pid"],
                 processo["arrival_time"],
                 processo["burst_time"]))
    
timeline_fcfs = []
timeline_fjs = []