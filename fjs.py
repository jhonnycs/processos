import copy

def fjs(processes,  context_switch_cost):
	procs = copy.deepcopy(processes)

	timeline = [] # {"pid": "P01", "start": 0, "end": 5},
	time = 0

	#procs.sort(key=lambda x: x.burst_time)
	# problema: criar ordenação para fila de prontos