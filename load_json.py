import json
from models.Process import Process

class JsonData:
    def __init__(self, json_name: str):
        """Carrega os dados do JSON no momento da criação do objeto."""
        self.json_name = json_name
        with open(f"dataset/{json_name}", "r", encoding="utf-8") as f:
            dados = json.load(f)

        self.context_switch_cost: int = dados["metadata"]["context_switch_cost"]
        self.throughput_window_T = dados["metadata"]["throughput_window_T"]
        self.rr_quantums: list[int] = dados["metadata"]["rr_quantums"]

        self.time_unit: str = dados["workload"]["time_unit"]
        self.processes: list[Process] = [
            Process(
                p["pid"],
                p["arrival_time"],
                p["burst_time"],
                self.time_unit,
            )
            for p in dados["workload"]["processes"]
        ]


    def __repr__(self):
        return self.json_name
