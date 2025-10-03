import statistics
import matplotlib.pyplot as plt
from models.Timeline import Timeline

class Metrica:
    def __init__(self, nome_algoritmo, timeline, tempo_final=None, throughput_window_T=None):
        self.nome_algoritmo = nome_algoritmo
        self.timeline = timeline.time_list
        self.tempo_final = tempo_final if tempo_final else max(tp.end for tp in self.timeline)
        self.tempo_vazao = throughput_window_T if throughput_window_T else self.tempo_final

        # PIDs válidos (com arrival definido)
        self.pids = sorted({tp.pid for tp in self.timeline if tp.pid is not None and tp.arrival is not None})
        self.tempos_espera = []
        self.tempos_retorno = []

        self._calculate_metrics()

        completion_by_pid = {}
        for tp in self.timeline:
            if tp.pid is None or tp.arrival is None:
                continue
            completion_by_pid[tp.pid] = max(completion_by_pid.get(tp.pid, -float('inf')), tp.end)

        completed_pids = [pid for pid, comp in completion_by_pid.items() if comp <= self.tempo_vazao]
        self.concluidos = len(completed_pids)
        self.vazao = self.concluidos / self.tempo_vazao if self.tempo_vazao > 0 else 0

    def _calculate_metrics(self):
        pid_first_last = {}
        pid_total_exec = {}
        pid_arrival = {}

        for tp in self.timeline:
            if tp.pid is None or tp.arrival is None:
                continue  # ignora idle / troca de contexto

            if tp.pid not in pid_first_last:
                pid_first_last[tp.pid] = [tp.start, tp.end]
                pid_arrival[tp.pid] = tp.arrival
            else:
                pid_first_last[tp.pid][1] = tp.end
            pid_total_exec[tp.pid] = pid_total_exec.get(tp.pid, 0) + (tp.end - tp.start)

        for pid in self.pids:
            first, last = pid_first_last[pid]
            burst_time = pid_total_exec[pid]
            arrival_time = pid_arrival[pid]

            turnaround = last - arrival_time
            waiting = turnaround - burst_time

            self.tempos_retorno.append(turnaround)
            self.tempos_espera.append(waiting)

        self.tempo_medio_espera = statistics.mean(self.tempos_espera) if self.tempos_espera else 0
        self.tempo_medio_retorno = statistics.mean(self.tempos_retorno) if self.tempos_retorno else 0

    def to_dict(self):
        return {
            "algoritmo": self.nome_algoritmo,
            "tempo_medio_espera": self.tempo_medio_espera,
            "tempo_medio_retorno": self.tempo_medio_retorno,
            "vazao": self.vazao
        }
    
    def show_metricas(self):
        print("=================================")
        print(self.nome_algoritmo)
        print(f"Tempo médio de espera: {self.tempo_medio_espera:.2f}")
        print(f"Tempo médio de retorno: {self.tempo_medio_retorno:.2f}")
        print(f"vazão: {self.vazao:.3f}\n")


class Metricas:
    def __init__(self):
        self.metricas: list[Metrica] = []

    def adicionar(self, nome_algoritmo, timeline, tempo_final=None, throughput_window_T=None):
        metrica = Metrica(nome_algoritmo, timeline, tempo_final, throughput_window_T)
        self.metricas.append(metrica)

    def to_list(self):
        return [m.to_dict() for m in self.metricas]

    def to_dict(self):
        return {m.nome_algoritmo: m.to_dict() for m in self.metricas}

    def show_metricas_de_todos(self):
        for metrica in self.metricas:
            metrica.show_metricas()

    def plot_tempos_espera(self):
        nomes = [m.nome_algoritmo for m in self.metricas]
        valores = [m.tempo_medio_espera for m in self.metricas]

        bars = plt.bar(nomes, valores, color="skyblue")
        plt.title("Tempo Médio de Espera")
        plt.ylabel("Tempo")
        plt.xlabel("Algoritmos")

        # adiciona rótulos no topo
        plt.bar_label(bars, fmt="%.2f", padding=3)

        plt.savefig("./graficos/tempos_espera")
        plt.show()


    def plot_tempos_retorno(self):
        nomes = [m.nome_algoritmo for m in self.metricas]
        valores = [m.tempo_medio_retorno for m in self.metricas]

        bars = plt.bar(nomes, valores, color="orange")
        plt.title("Tempo Médio de Retorno")
        plt.ylabel("Tempo")
        plt.xlabel("Algoritmos")
        plt.bar_label(bars, fmt="%.2f", padding=3)
        plt.savefig("./graficos/tempo_retorno")
        plt.show()

    def plot_vazao(self):
        nomes = [m.nome_algoritmo for m in self.metricas]
        valores = [m.vazao for m in self.metricas]

        bars = plt.bar(nomes, valores, color="green")
        plt.title("Vazão")
        plt.ylabel("Processos por unidade de tempo")
        plt.xlabel("Algoritmos")
        plt.bar_label(bars, fmt="%.3f", padding=3)
        plt.savefig("./graficos/vazao")
        plt.show()

    def plot_todos(self):
        """Mostra os três gráficos juntos em uma grade 1x3"""
        nomes = [m.nome_algoritmo for m in self.metricas]

        espera = [m.tempo_medio_espera for m in self.metricas]
        retorno = [m.tempo_medio_retorno for m in self.metricas]
        vazao = [m.vazao for m in self.metricas]

        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        bars1 = axes[0].bar(nomes, espera, color="skyblue")
        axes[0].set_title("Tempo Médio de Espera")
        axes[0].set_ylabel("Tempo")
        axes[0].bar_label(bars1, fmt="%.2f", padding=3)

        bars2 = axes[1].bar(nomes, retorno, color="orange")
        axes[1].set_title("Tempo Médio de Retorno")
        axes[1].set_ylabel("Tempo")
        axes[1].bar_label(bars2, fmt="%.2f", padding=3)

        bars3 = axes[2].bar(nomes, vazao, color="green")
        axes[2].set_title("Vazão")
        axes[2].set_ylabel("Processos por unidade de tempo")
        axes[2].bar_label(bars3, fmt="%.3f", padding=3)

        plt.tight_layout()
        plt.savefig("./graficos/tres_metricas_juntas")
        plt.show()
