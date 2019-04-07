import MBalancer
from multiprocessing import Process

NUM_OF_HOSTS = 1
NUM_OF_SERVER_KEYS = 1000
NUM_OF_HOT_KEYS = 10
HOT_KEYS_RATIO = float(NUM_OF_HOT_KEYS) / NUM_OF_SERVER_KEYS

def foo(i):
    num_of_keys_to_set = NUM_OF_SERVER_KEYS / NUM_OF_HOSTS
    balancer = MBalancer.MBalancer(["10.0.2.2", "10.0.3.3"], NUM_OF_SERVER_KEYS, HOT_KEYS_RATIO, 1)
    balancer.set_keys(i * num_of_keys_to_set, num_of_keys_to_set)

hosts = []
for i in range(NUM_OF_HOSTS):
    hosts.append(Process(target=foo, args=(i,)))
for i in range(NUM_OF_HOSTS):
    hosts[i].start()
for i in range(NUM_OF_HOSTS):
    hosts[i].join()
