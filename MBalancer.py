import memcached_udp
import argparse
import time

MAX_NUMBER_OF_RETRIES = 10

class MBalancer(object):
    MEMCACHED_PORT = 11111
    KEY_LENGTH = 16

    def __init__(self, server_ips, number_of_keys, hot_keys_fraction, timeout):
        self.servers = server_ips
        self.client  = memcached_udp.Client([(server_ip, self.MEMCACHED_PORT) for server_ip in server_ips], response_timeout=timeout)
        # self.client1 = memcached_udp.Client([(server_ips[0], self.MEMCACHED_PORT)], response_timeout=timeout)
        # self.client2 = memcached_udp.Client([(server_ips[1], self.MEMCACHED_PORT)], response_timeout=timeout)
        self.number_of_keys = number_of_keys
        # hot keys
        self.hot_keys = [("Hot"*self.KEY_LENGTH)[:self.KEY_LENGTH - 3] + "{:03d}".format(i) for i in range(int(number_of_keys * hot_keys_fraction))]
        # normal keys
        self.normal_keys = [("Normal"*self.KEY_LENGTH)[:self.KEY_LENGTH - 7] + "{:07d}".format(i) for i in range(number_of_keys - len(self.hot_keys))]

    def _get_key_by_index(self, key_idx):
        if key_idx < len(self.hot_keys):
            key = self.hot_keys[key_idx]
        else:
            key = self.normal_keys[key_idx - len(self.hot_keys)]
        return key

    def set_keys(self, offset = 0, number_of_keys = None):
        if number_of_keys is None:
            number_of_keys = self.number_of_keys
        for key_idx in range(offset, offset + number_of_keys):
            key = self._get_key_by_index(key_idx)
            while True:
                try:
                    if key in self.normal_keys:
                        self.client.set(key, "server {} value of {}".format(self.servers.index(self.client._pick_server(key)[0]) + 1, key))
                    if key in self.hot_keys:
                        self.client1.set(key, "server 1 value of {}".format(key))
                        self.client2.set(key, "server 2 value of {}".format(key))
                    break
                except:
                    pass

    def query_keys(self, key_idx_query_list):
        for key_idx in key_idx_query_list:
            key = self._get_key_by_index(key_idx)
            server = self.servers.index(self.client._pick_server(key)[0]) + 1
            attempt_number = 0
            while(True):
                try:
                    value = self.client.get(key)
                    print "(from server {}) get {} : {}".format(server, key, value)
                    break
                except:
                    print "mini failure"
                    if attempt_number >= MAX_NUMBER_OF_RETRIES:
                        print "failed to get key {} from server {}".format(key, server)
                        break
                    attempt_number += 1

    def query_keys_simulated(self, key_query_list):
        results = []
        for key in key_query_list:
            server = self.servers.index(self.client._pick_server(key)[0])
            results.append(server)
        return results
