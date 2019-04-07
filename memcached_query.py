import MBalancer
from multiprocessing import Process
import time
import numpy as np

NUM_OF_ITERATIONS = 1
NUM_OF_KEYS  = 50
NUM_OF_HOSTS = 1
NUM_OF_SERVER_KEYS = 1000
NUM_OF_HOT_KEYS = 10
HOT_KEYS_RATIO = float(NUM_OF_HOT_KEYS) / NUM_OF_SERVER_KEYS

def foo(query_list):
    balancer = MBalancer.MBalancer(["10.0.2.2", "10.0.3.3"], NUM_OF_SERVER_KEYS, HOT_KEYS_RATIO, 1)
    balancer.query_keys(query_list)

results = []
for j in range(NUM_OF_ITERATIONS):
    hosts = []
    for i in range(NUM_OF_HOSTS):
        host_keys_to_query = []
        for i_key in range(NUM_OF_KEYS):
            key_idx = NUM_OF_SERVER_KEYS
            while key_idx >= NUM_OF_SERVER_KEYS:
                key_idx = np.random.zipf(1.01) - 1
                # make it so no special handling of hot keys is done
                # key_idx += NUM_OF_HOT_KEYS
            host_keys_to_query.append(key_idx)
        hosts.append(Process(target=foo, args=(host_keys_to_query,)))
    start = time.time()
    for i in range(NUM_OF_HOSTS):
        hosts[i].start()
    for i in range(NUM_OF_HOSTS):
        hosts[i].join()
    end = time.time()
    results.append(end-start)
    # print results[-1]
