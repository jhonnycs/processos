# Timeline.py
from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

@dataclass
class Timepoint:
    pid: str
    start: int
    end: int
    arrival: int = None

class Timeline:
    def __init__(self, algorithm=None, quantum=None):
        self.time_list = []
        self.algorithm = algorithm
        self.quantum = quantum

    def has_timepoints(self) -> bool:
        return len(self.time_list) > 0

    def get_last_timepoint(self):
        if not self.time_list:
            return None
        return self.time_list[-1]

    def add_to_timeline(self, time_point: Timepoint):
        last = self.get_last_timepoint()

        if last is None:
            self.time_list.append(time_point)
            return

        if time_point.pid == last.pid:
            if time_point.end > last.end:
                last.end = time_point.end
            return


        self.time_list.append(time_point)

    def show_timeline(self):
        for timepoint in self.time_list:
            if timepoint.arrival is None:
                print(f"pid: {timepoint.pid};  início: {timepoint.start};  fim: {timepoint.end}")
            else:
                print(f"pid: {timepoint.pid};  início: {timepoint.start};  fim: {timepoint.end};  chegada: {timepoint.arrival}")


    def plot_gantt_classic(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        # cores fixas para casos especiais
        colors = {
            "CTX": "red",
            "IDLE": "gray"
        }

        # pega todos os processos que não são especiais
        pids = sorted(set(tp.pid for tp in self.time_list if tp.pid not in ("CTX", "IDLE")))
        cmap = plt.get_cmap("tab20")
        for i, pid in enumerate(pids):
            colors[pid] = cmap(i % 20)

        # mapeia cada pid para uma "linha" do gráfico
        all_pids = pids + ["CTX", "IDLE"]  # mantém ctx e idle visíveis
        yticks = []
        ylabels = []

        for i, pid in enumerate(all_pids):
            y = i  # linha correspondente
            yticks.append(y)
            ylabels.append(pid)

            for tp in self.time_list:
                if tp.pid == pid:
                    ax.barh(y, tp.end - tp.start, left=tp.start,
                            height=0.4, color=colors[pid], edgecolor="black")
                    ax.text((tp.start + tp.end)/2, y, f"{tp.start}-{tp.end}",
                            ha="center", va="center", color="white", fontsize=8)

        # formatação do gráfico
        ax.set_yticks(yticks)
        ax.set_yticklabels(ylabels)
        ax.set_xlabel("Tempo")
        if self.algorithm:
            if self.quantum:
                ax.set_title(f"Diagrama de Gantt - {self.algorithm} (q = {self.quantum})")
            else:
                ax.set_title(f"Diagrama de Gantt - {self.algorithm}")

        else:
            ax.set_title("Diagrama de Gantt - Execução de Processos")

        # legenda
        legend_elements = [Patch(facecolor=colors[pid], label=pid) for pid in all_pids]
        ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc="upper left")

        max_time = max(tp.end for tp in self.time_list)
        ax.set_xlim(0, max_time)
        ax.set_xticks(range(0, max_time + 1, 2))
        ax.grid(axis="x", linestyle="--", alpha=0.5)

        plt.tight_layout()
        plt.show()