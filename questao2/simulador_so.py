import threading
import time
import random


trava = threading.Lock()

condicao = threading.Condition(trava)

compiladores_disponiveis = 1
vagas_bd_disponiveis = 2

class Programador(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def run(self):
        """ O ciclo de vida de um programador, em laço infinito. """
        global compiladores_disponiveis, vagas_bd_disponiveis
        
        while True:
            print(f"Programador {self.id}:    está pensando (descansando).")
            time.sleep(random.uniform(3, 6))

            print(f"Programador {self.id}: -> quer compilar e precisa de recursos.")

            with condicao:
                while compiladores_disponiveis < 1 or vagas_bd_disponiveis < 1:
                    print(f"Programador {self.id}: -- aguardando... (Comp: {compiladores_disponiveis}, BD: {vagas_bd_disponiveis})")
                    condicao.wait() 
                
                compiladores_disponiveis -= 1
                vagas_bd_disponiveis -= 1
                print(f"Programador {self.id}: ++ PEGOU os recursos. (Comp: {compiladores_disponiveis}, BD: {vagas_bd_disponiveis})")

            print(f"Programador {self.id}:    *** COMEÇOU A COMPILAR ***")
            time.sleep(random.uniform(2, 4))
            print(f"Programador {self.id}:    *** TERMINOU DE COMPILAR ***")

            with condicao:
                compiladores_disponiveis += 1
                vagas_bd_disponiveis += 1
                print(f"Programador {self.id}: -- liberou os recursos. (Comp: {compiladores_disponiveis}, BD: {vagas_bd_disponiveis})")
                
                condicao.notify_all()


if __name__ == "__main__":
    programadores = [Programador(i) for i in range(1, 6)]

    print("Iniciando a simulação do laboratório...")
    print("-" * 40)

    for p in programadores:
        p.start()

    for p in programadores:
        p.join()