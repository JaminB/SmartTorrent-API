import loadbalancer

loadbalancer.set_ip_list()
#print loadbalancer.get_ip_list()
print loadbalancer.get_next_ip()
print loadbalancer.get_next_ip()
print loadbalancer.get_next_ip_json()

