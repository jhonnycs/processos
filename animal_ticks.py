import json
import time

with open("config.json", "r") as f:
    config = json.load(f)

metadata = config["metadata"]
room_config = config["room"]
workload = config["workload"]

animals = workload["animals"]
total_time = sum(a["rest_duration"] for a in animals) + max(a["arrival_time"] for a in animals) + 5

dogs_in_room = []
cats_in_room = []
current_state = room_config["initial_sign_state"]

def update_state():
    global current_state
    if len(dogs_in_room) > 0 and len(cats_in_room) == 0:
        current_state = "DOGS"
    elif len(cats_in_room) > 0 and len(dogs_in_room) == 0:
        current_state = "CATS"
    elif len(dogs_in_room) == 0 and len(cats_in_room) == 0:
        current_state = "EMPTY"

def can_enter(species):
    if current_state == "EMPTY":
        return True
    elif current_state == "DOGS" and species == "DOG":
        return True
    elif current_state == "CATS" and species == "CAT":
        return True
    return False

for a in animals:
    a["remaining_time"] = a["rest_duration"]

waiting_list = []

for tick in range(total_time + 1):
    print(f"\n[TICK {tick}] Estado da sala: {current_state}")

    for a in animals:
        if a["arrival_time"] == tick:
            print(f" -> {a['id']} ({a['species']}) chegou")
            waiting_list.append(a)

    for a in list(waiting_list):
        if can_enter(a["species"]):
            if a["species"] == "DOG":
                dogs_in_room.append(a)
            else:
                cats_in_room.append(a)
            print(f"    {a['id']} entrou na sala")
            update_state()
            waiting_list.remove(a)

    for dog in list(dogs_in_room):
        dog["remaining_time"] -= 1
        if dog["remaining_time"] == 0:
            print(f" <- {dog['id']} saiu da sala")
            dogs_in_room.remove(dog)
            update_state()

    for cat in list(cats_in_room):
        cat["remaining_time"] -= 1
        if cat["remaining_time"] == 0:
            print(f" <- {cat['id']} saiu da sala")
            cats_in_room.remove(cat)
            update_state()

    time.sleep(0.5)
print("\n========= Fim =========")