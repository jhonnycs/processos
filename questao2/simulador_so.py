import threading
import time
import random


# Mutex pra proteger as variaveis
trava = threading.Lock()

# Variável de condição para os programadores esperarem pelos recursos
condicao = threading.Condition(trava)

# Contagem de recursos disponíveis
compiladores_disponiveis = 1
vagas_bd_disponiveis = 2

# Representação dos programadores
class Programador(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def run(self):
        """ O ciclo de vida de um programador, em laço infinito. """
        global compiladores_disponiveis, vagas_bd_disponiveis
        
        while True:
            # Pensar / descansar
            print(f"Programador {self.id}:    está pensando (descansando).")
            time.sleep(random.uniform(3, 6))

            print(f"Programador {self.id}: -> quer compilar e precisa de recursos.")

            # Adquirir recursos
            with condicao:
                while compiladores_disponiveis < 1 or vagas_bd_disponiveis < 1:
                    print(f"Programador {self.id}: -- aguardando... (Comp: {compiladores_disponiveis}, BD: {vagas_bd_disponiveis})")
                    condicao.wait() # Espera (libera a trava e dorme)
                
                # Se chegou nessa parte do código quer dizer que os recursos estão disponíveis.
                compiladores_disponiveis -= 1
                vagas_bd_disponiveis -= 1
                print(f"Programador {self.id}: ++ PEGOU os recursos. (Comp: {compiladores_disponiveis}, BD: {vagas_bd_disponiveis})")

            # Compilar 
            print(f"Programador {self.id}:    *** COMEÇOU A COMPILAR ***")
            time.sleep(random.uniform(2, 4))
            print(f"Programador {self.id}:    *** TERMINOU DE COMPILAR ***")

            # Liberar os recursos
            with condicao:
                compiladores_disponiveis += 1
                vagas_bd_disponiveis += 1
                print(f"Programador {self.id}: -- liberou os recursos. (Comp: {compiladores_disponiveis}, BD: {vagas_bd_disponiveis})")
                
                # Notifica todas as outras threads que estão esperando
                # que o estado dos recursos mudou e elas devem verificar novamente.
                condicao.notify_all()


if __name__ == "__main__":
    # criação das threads (programadores)
    programadores = [Programador(i) for i in range(1, 6)]

    print("Iniciando a simulação do laboratório...")
    print("-" * 40)

    # Inicia todas as threads
    for p in programadores:
        p.start()

    # Como o laço é infinito, o programa principal pode apenas esperar.
    for p in programadores:
        p.join()