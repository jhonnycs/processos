import json
from Process import Process

with open("a.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

def load_processes():
    processes: list[Process] = []

    for process in dados["workload"]["processes"]:
        processes.append(Process(process["pid"], process["arrival_time"], process["burst_time"]))

    return processes

def get_switch_cost() -> int:
    return dados["metadata"]["context_switch_cost"]
