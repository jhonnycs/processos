# Timeline.py
from dataclasses import dataclass

@dataclass
class Timepoint:
    pid: str
    start: int
    end: int

class Timeline:
    def __init__(self):
        self.time_list = []

    def has_timepoints(self) -> bool:
        return len(self.time_list) > 0

    def get_last_timepoint(self):
        """Retorna o último Timepoint ou None se vazio."""
        if not self.time_list:
            return None
        return self.time_list[-1]

    def add_to_timeline(self, time_point: Timepoint):
        """
        Adiciona um timepoint.
        Se o PID do novo timepoint for igual ao último, podemos mesclar extendendo o end.
        Caso contrário, somente append.
        """
        last = self.get_last_timepoint()

        # Se não existe último, apenas adiciona
        if last is None:
            self.time_list.append(time_point)
            return

        # Se o novo timepoint tem mesmo pid do último, mescla (estende o end)
        if time_point.pid == last.pid:
            # garante que o último end seja o mínimo entre o existente e o novo? 
            # Normalmente você quer setar last.end para o novo 'end' se este for maior.
            if time_point.end > last.end:
                last.end = time_point.end
            # se preferir somar, ou outra lógica, adapte aqui
            return

        # Caso contrário, apenas adiciona
        self.time_list.append(time_point)
