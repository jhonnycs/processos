import json
import threading
import time
from queue import Queue

waiting_queue = Queue()

with open("processos/config.json", "r") as f:
    config = json.load(f)

metadata = config["metadata"]
room_config = config["room"]
workload = config["workload"]

room_count = metadata["room_count"]
animals = workload["animals"]

total_time = sum(a["rest_duration"] for a in animals) + max(a["arrival_time"] for a in animals) + 5

room_sem = threading.Semaphore(1)
dogs_in_room = 0
cats_in_room = 0
current_state = room_config["initial_sign_state"]

def update_state():
    global current_state, dogs_in_room, cats_in_room
    if dogs_in_room > 0 and cats_in_room == 0:
        current_state = "DOGS"
    elif cats_in_room > 0 and dogs_in_room == 0:
        current_state = "CATS"
    elif dogs_in_room == 0 and cats_in_room == 0:
        current_state = "EMPTY"
    print(f"Estado atual da sala: {current_state}")

def can_enter(species):
    if current_state == "EMPTY":
        return True
    elif current_state == "DOGS" and species == "DOG":
        return True    
    elif current_state == "CATS" and species == "CAT":
        return True
    return False

def animal_process(animal):
    global dogs_in_room, cats_in_room

    # tempo de chegada
    time.sleep(animal["arrival_time"])
    waiting_queue.put(animal)
    print("Chegou: ", animal['id'])

    while True:
        room_sem.acquire()
        first_in_queue = waiting_queue.queue[0]
        if (current_state == "EMPTY" and first_in_queue["id"] == animal["id"]) \
           or (current_state == "DOGS" and animal["species"] == "DOG") \
           or (current_state == "CATS" and animal["species"] == "CAT"):

            waiting_queue.get()  # remove da fila
            if animal["species"] == "DOG":
                dogs_in_room += 1
            else:
                cats_in_room += 1

            update_state()
            print(f"[{animal['id']}] entrou na sala")
            room_sem.release()
            break

        room_sem.release()
        time.sleep(0.1)

    time.sleep(animal["rest_duration"])

    room_sem.acquire()
    if animal["species"] == "DOG":
        dogs_in_room -= 1
    else:
        cats_in_room -= 1
    update_state()
    print(f"[{animal['id']}] saiu da sala")
    room_sem.release()

threads = []
for a in animals:
    t = threading.Thread(target=animal_process, args=(a,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\n========= Fim =========")