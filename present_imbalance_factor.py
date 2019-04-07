import MBalancer
from collections import Counter
import numpy as np
import random
import string
import matplotlib.pyplot as plt

NUM_OF_SERVERS = 20
NUM_OF_SERVER_KEYS = 1000
NUM_OF_HOT_KEYS = 50
HOT_KEYS_RATIO = float(NUM_OF_HOT_KEYS) / NUM_OF_SERVER_KEYS
NUM_OF_KEYS_QUERIED  = 2000
NUM_OF_ITERATIONS = 200

def random_key_generator():
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(16))

for servers_available in range(2, NUM_OF_SERVERS + 1):
    balancer = MBalancer.MBalancer(["10.0.{0}.{0}".format(i) for i in range(servers_available)], NUM_OF_SERVER_KEYS, HOT_KEYS_RATIO, 1)
    average_imbalance_factor = [0] * (NUM_OF_HOT_KEYS + 1)
    for iteration_number in range(NUM_OF_ITERATIONS):
        host_keys = [random_key_generator() for i in range(NUM_OF_SERVER_KEYS)]
        host_key_idxs_to_query = []
        for i_key in range(NUM_OF_KEYS_QUERIED):
            key_idx = NUM_OF_SERVER_KEYS
            while key_idx >= NUM_OF_SERVER_KEYS:
                key_idx = np.random.zipf(1.01) - 1
            host_key_idxs_to_query.append(key_idx)
        host_keys_to_query = map(lambda key_idx: host_keys[key_idx], host_key_idxs_to_query)
        servers_queried = balancer.query_keys_simulated(host_keys_to_query)
        imbalance_factors = []
        for current_number_of_hot_keys in range(NUM_OF_HOT_KEYS + 1):
            host_keys_to_query_is_hot = map(lambda key_idx: key_idx < current_number_of_hot_keys, host_key_idxs_to_query)
            servers_queried_after_balancing = []
            current_server_for_hot_key = 0
            for i,server_queried in enumerate(servers_queried):
                if host_keys_to_query_is_hot[i]:
                    servers_queried_after_balancing.append(current_server_for_hot_key)
                    current_server_for_hot_key = (current_server_for_hot_key + 1) % servers_available
                else:
                    servers_queried_after_balancing.append(server_queried)

            c = Counter(servers_queried_after_balancing)
            server_loads = [c[server_idx]/float(NUM_OF_KEYS_QUERIED) for server_idx in c]
            busiest_server_load = max(server_loads)
            imbalance_factor = 1.0 / (servers_available * busiest_server_load)
            imbalance_factors.append(imbalance_factor)

        average_imbalance_factor = np.add(average_imbalance_factor, imbalance_factors)
    average_imbalance_factor = average_imbalance_factor / NUM_OF_ITERATIONS
    plt.plot(range(NUM_OF_HOT_KEYS + 1), average_imbalance_factor, linewidth=2.0, label="for {} servers".format(servers_available))

plt.axis([0, NUM_OF_HOT_KEYS, 0, 1])
plt.xlabel('number of hot keys')
plt.ylabel('imbalance factor')
plt.legend()
plt.show()
