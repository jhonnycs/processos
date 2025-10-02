
from fcfs import fcfs
from sjf import sjf
from round_robin import round_robin
from load_json import load_processes, get_switch_cost

processes = load_processes()
context_switch_cost = get_switch_cost()

results_fcfs = fcfs(processes, context_switch_cost)
results_sjf = sjf(processes, context_switch_cost)
results_rr = round_robin(processes, context_switch_cost, 2)