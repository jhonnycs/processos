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

        # Vazão: apenas Timepoints de processos válidos
        self.concluidos = sum(
            1 for tp in self.timeline if tp.end <= self.tempo_vazao and tp.pid is not None and tp.arrival is not None)
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

        # Estatísticas
        self.tempo_medio_espera = statistics.mean(self.tempos_espera) if self.tempos_espera else 0
        self.desvio_padrao_espera = statistics.pstdev(self.tempos_espera) if len(self.tempos_espera) > 1 else 0
        self.tempo_medio_retorno = statistics.mean(self.tempos_retorno) if self.tempos_retorno else 0
        self.desvio_padrao_retorno = statistics.pstdev(self.tempos_retorno) if len(self.tempos_retorno) > 1 else 0

    def to_dict(self):
        return {
            "algoritmo": self.nome_algoritmo,
            "tempo_medio_espera": self.tempo_medio_espera,
            "desvio_padrao_espera": self.desvio_padrao_espera,
            "tempo_medio_retorno": self.tempo_medio_retorno,
            "desvio_padrao_retorno": self.desvio_padrao_retorno,
            "vazao": self.vazao
        }


class Metricas:
    def __init__(self):
        self.metricas = []

    def adicionar(self, nome_algoritmo, timeline, tempo_final=None, throughput_window_T=None):
        metrica = Metrica(nome_algoritmo, timeline, tempo_final, throughput_window_T)
        self.metricas.append(metrica)

    def to_list(self):
        return [m.to_dict() for m in self.metricas]

    def to_dict(self):
        return {m.nome_algoritmo: m.to_dict() for m in self.metricas}

    def plot_tempos_espera(self):
        nomes = [m.nome_algoritmo for m in self.metricas]
        valores = [m.tempo_medio_espera for m in self.metricas]

        plt.bar(nomes, valores, color="skyblue")
        plt.title("Tempo Médio de Espera")
        plt.ylabel("Tempo")
        plt.xlabel("Algoritmos")
        plt.show()

    def plot_tempos_retorno(self):
        nomes = [m.nome_algoritmo for m in self.metricas]
        valores = [m.tempo_medio_retorno for m in self.metricas]

        plt.bar(nomes, valores, color="orange")
        plt.title("Tempo Médio de Retorno")
        plt.ylabel("Tempo")
        plt.xlabel("Algoritmos")
        plt.show()

    def plot_vazao(self):
        nomes = [m.nome_algoritmo for m in self.metricas]
        valores = [m.vazao for m in self.metricas]

        plt.bar(nomes, valores, color="green")
        plt.title("Vazão")
        plt.ylabel("Processos por unidade de tempo")
        plt.xlabel("Algoritmos")
        plt.show()

    def plot_todos(self):
        """Mostra os três gráficos juntos em uma grade 1x3"""
        nomes = [m.nome_algoritmo for m in self.metricas]

        espera = [m.tempo_medio_espera for m in self.metricas]
        retorno = [m.tempo_medio_retorno for m in self.metricas]
        vazao = [m.vazao for m in self.metricas]

        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        axes[0].bar(nomes, espera, color="skyblue")
        axes[0].set_title("Tempo Médio de Espera")
        axes[0].set_ylabel("Tempo")

        axes[1].bar(nomes, retorno, color="orange")
        axes[1].set_title("Tempo Médio de Retorno")
        axes[1].set_ylabel("Tempo")

        axes[2].bar(nomes, vazao, color="green")
        axes[2].set_title("Vazão")
        axes[2].set_ylabel("Processos por unidade de tempo")

        plt.tight_layout()
        plt.show()