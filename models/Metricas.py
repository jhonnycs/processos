import statistics
import matplotlib.pyplot as plt

class Metricas:
    def __init__(self, timeline, tempo_final=None, throughput_window_T=None):
        self.timeline = timeline.time_list
        self.tempo_final = tempo_final if tempo_final else max(tp.end for tp in self.timeline)
        self.tempo_vazao = throughput_window_T if throughput_window_T else self.tempo_final

        # Calcular métricas por PID
        self.pids = sorted({tp.pid for tp in self.timeline})
        self.tempos_espera = []
        self.tempos_retorno = []

        self._calculate_metrics()

        # Vazão
        self.concluidos = sum(1 for tp in self.timeline if tp.end <= self.tempo_vazao)
        self.vazao = self.concluidos / self.tempo_vazao if self.tempo_vazao > 0 else 0

    def _calculate_metrics(self):
        pid_first_last = {}
        pid_total_exec = {}

        for tp in self.timeline:
            if tp.pid not in pid_first_last:
                pid_first_last[tp.pid] = [tp.start, tp.end]
            else:
                pid_first_last[tp.pid][1] = tp.end  # atualizar último end
            pid_total_exec[tp.pid] = pid_total_exec.get(tp.pid, 0) + (tp.end - tp.start)

        for pid in self.pids:
            first, last = pid_first_last[pid]
            burst_time = pid_total_exec[pid]
            turnaround = last - first
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
            "tempo_medio_espera": self.tempo_medio_espera,
            "desvio_padrao_espera": self.desvio_padrao_espera,
            "tempo_medio_retorno": self.tempo_medio_retorno,
            "desvio_padrao_retorno": self.desvio_padrao_retorno,
            "vazao": self.vazao
        }


    def plot_tempos(self):
        plt.figure(figsize=(10,5))
        plt.plot(self.tempos_espera, label="Tempo de Espera", marker='o')
        plt.plot(self.tempos_retorno, label="Tempo de Retorno", marker='x')
        plt.xlabel("Processo (PID ordenado)")
        plt.ylabel("Tempo")
        plt.title("Tempos de Espera e Retorno por Processo")
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_vazao(self):
        plt.figure(figsize=(6,4))
        plt.bar(["Vazão"], [self.vazao])
        plt.ylabel("Processos por unidade de tempo")
        plt.title("Vazão")
        plt.show()

    def plot_timeline(self):
        plt.figure(figsize=(12, len(self.pids)*0.5 + 1))
        for i, pid in enumerate(self.pids):
            for tp in self.timeline:
                if tp.pid == pid:
                    plt.hlines(i, tp.start, tp.end, colors='tab:blue', linewidth=6)
        plt.yticks(range(len(self.pids)), self.pids)
        plt.xlabel("Tempo")
        plt.ylabel("PID")
        plt.title("Linha do Tempo (Timeline) dos Processos")
        plt.grid(True)
        plt.show()
