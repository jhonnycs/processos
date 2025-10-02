import json
from models.Process import Process

with open("dataset/a.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

def load_processes():
    processes: list[Process] = []

    for process in dados["workload"]["processes"]:
        processes.append(Process(process["pid"], process["arrival_time"], process["burst_time"], dados["workload"]["time_unit"]))

    return processes

def get_switch_cost() -> int:
    return dados["metadata"]["context_switch_cost"]
