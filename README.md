# MBalancer
Code relevant for the Memcached Load Balancer. It is meant to run in a Mininet simulated environment.
h1 is a Memcached client that sends requests to the Memcached servers h2 and h3.
s1 should have various rules in place to load balance the request to hot keys, and round robin those to h2 and h3.

1. Run h2_server.sh on h2.
2. Run h3_server.sh on h3.
3. run memcached_set.py on h1, to set some keys to servers h2 and h3.
4. run memcached_query.py on h1, to get some keys from servers h2 and h3.
