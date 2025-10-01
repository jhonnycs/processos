
from fcfs import fcfs
from fjs import fjs
from round_robin import round_robin
from load_json import load_processes, get_switch_cost

processes = load_processes()
context_switch_cost = get_switch_cost()

results_fcfs = fcfs(processes, context_switch_cost)
results_fjs = fjs(processes, context_switch_cost)
results_rr = round_robin(processes, context_switch_cost)