from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI # Not needed anymore
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI

import time

topo = load_topo('topology.json')
controllers = {}

# Note: we now use the SimpleSwitchThriftAPI to communicate with the switches
# and not the P4RuntimeAPI anymore.
for p4switch in topo.get_p4switches():
    thrift_port = topo.get_thrift_port(p4switch)
    controllers[p4switch] = SimpleSwitchThriftAPI(thrift_port)

# The following lines enable the forwarding as required for assignment 0.
controllers['s1'].table_add('repeater', 'forward', ['1'], ['2'])
controllers['s1'].table_add('repeater', 'forward', ['3'], ['1'])

controllers['s2'].table_add('repeater', 'forward', ['1'], ['2'])
controllers['s2'].table_add('repeater', 'forward', ['2'], ['1'])

controllers['s4'].table_add('repeater', 'forward', ['1'], ['2'])
controllers['s4'].table_add('repeater', 'forward', ['2'], ['1'])

controllers['s3'].table_add('repeater', 'forward', ['1'], ['2'])
controllers['s3'].table_add('repeater', 'forward', ['2'], ['3'])

controllers['s1'].register_write('counter_ingress', 0, 0)
controllers['s1'].register_write('counter_ingress', 1, 0)
controllers['s2'].register_write('counter_ingress', 0, 0)
controllers['s2'].register_write('counter_ingress', 1, 0)
controllers['s3'].register_write('counter_ingress', 0, 0)
controllers['s3'].register_write('counter_ingress', 1, 0)
controllers['s4'].register_write('counter_ingress', 0, 0)
controllers['s4'].register_write('counter_ingress', 1, 0)

controllers['s1'].register_write('counter_egress', 0, 0)
controllers['s1'].register_write('counter_egress', 1, 0)
controllers['s2'].register_write('counter_egress', 0, 0)
controllers['s2'].register_write('counter_egress', 1, 0)
controllers['s3'].register_write('counter_egress', 0, 0)
controllers['s3'].register_write('counter_egress', 1, 0)
controllers['s4'].register_write('counter_egress', 0, 0)
controllers['s4'].register_write('counter_egress', 1, 0)

controllers['s1'].register_write('active_counter_index', 0, 0)
controllers['s2'].register_write('active_counter_index', 0, 0)
controllers['s3'].register_write('active_counter_index', 0, 0)
controllers['s4'].register_write('active_counter_index', 0, 0)

controllers['s1'].register_write('ignore_on_port_ingress', 0, 1)
controllers['s1'].register_write('ignore_on_port_egress', 0, 1)

controllers['s2'].register_write('ignore_on_port_ingress', 0, 0)
controllers['s2'].register_write('ignore_on_port_egress', 0, 0)

controllers['s3'].register_write('ignore_on_port_ingress', 0, 2)
controllers['s3'].register_write('ignore_on_port_egress', 0, 2)

controllers['s4'].register_write('ignore_on_port_ingress', 0, 0)
controllers['s4'].register_write('ignore_on_port_egress', 0, 0)

def print_link(s1, s2, index):
    # We recommend to implement a function that prints the value of the
    # counters used for a particular link and direction.
    # It will help you to debug.
    # However, this is not mandatory. If you do not do it,
    # we won't deduct points.
    counter_s1_0 = controllers[s1].register_read('counter_egress', 0)
    counter_s1_1 = controllers[s1].register_read('counter_egress', 1)
    counter_s2_0 = controllers[s2].register_read('counter_ingress', 0)
    counter_s2_1 = controllers[s2].register_read('counter_ingress', 1)
    print (index)
    print("counter 0: ", s1, " ", counter_s1_0) 
    print("counter 1: ", s1, " ", counter_s1_1) 
    print("counter 0: ", s2, " ", counter_s2_0) 
    print("counter 1: ", s2, " ", counter_s2_1, "\n") 

while True:
    
    # This is where you need to write most of your code.
    index_register_s1 = controllers['s1'].register_read('active_counter_index', 0)
    print(controllers['s1'].register_read('active_counter_index', 0))
    new_index_register_value_s1 = 0
    if index_register_s1 == 0:
        print("I am in if")
        controllers['s1'].register_write('active_counter_index', 0, 1)
    else :
        print("I am in else")
        controllers['s1'].register_write('active_counter_index', 0, 0)
    # print(new_index_register_value_s1)
    # controllers['s1'].register_write('active_counter_index', 0, new_index_register_value_s1)
    print(controllers['s1'].register_read('active_counter_index', 0))

    counter_s1 = controllers['s1'].register_read('counter_egress', index_register_s1)
    counter_s2 = controllers['s2'].register_read('counter_ingress', index_register_s1)
    
    print_link('s1','s2', index_register_s1)
    controllers['s1'].register_write('counter_egress', index_register_s1, 0)
    controllers['s2'].register_write('counter_ingress', index_register_s1, 0)
    if counter_s1 != counter_s2:
        print("Packets were lost on the link from port 2 of s1 to port 1 of s2")
    

    index_register = controllers['s2'].register_read('active_counter_index', 0)
    new_index_register_value = 0
    if index_register == 0:
        new_index_register_value = 1
    controllers['s2'].register_write('active_counter_index', 0, new_index_register_value)

    counter_s2 = controllers['s2'].register_read('counter_egress', index_register)
    counter_s3 = controllers['s3'].register_read('counter_ingress', index_register)
    
    print_link('s2','s3',index_register)

    controllers['s2'].register_write('counter_egress', index_register, 0)
    controllers['s3'].register_write('counter_ingress', index_register, 0)
    
    if counter_s2 != counter_s3:
        print("Packets were lost on the link from port 2 of s2 to port 1 of s3")

    index_register = controllers['s3'].register_read('active_counter_index', 0)
    new_index_register_value = 0
    if index_register == 0:
        new_index_register_value = 1
    controllers['s3'].register_write('active_counter_index', 0, new_index_register_value)

    counter_s3 = controllers['s3'].register_read('counter_egress', index_register)
    counter_s4 = controllers['s4'].register_read('counter_ingress', index_register)
    
    print_link('s3','s4', index_register)

    controllers['s3'].register_write('counter_egress', index_register, 0)
    controllers['s4'].register_write('counter_ingress', index_register, 0)
    
    if counter_s3 != counter_s4:
        print("Packets were lost on the link from port 3 of s3 to port 1 of s4")

    index_register = controllers['s4'].register_read('active_counter_index', 0)
    new_index_register_value = 0
    if index_register == 0:
        new_index_register_value = 1
    controllers['s4'].register_write('active_counter_index', 0, new_index_register_value)

    counter_s4 = controllers['s4'].register_read('counter_egress', index_register)
    counter_s1 = controllers['s1'].register_read('counter_ingress', index_register)
    
    print_link('s4','s1', index_register)
    
    controllers['s4'].register_write('counter_egress', index_register, 0)
    controllers['s1'].register_write('counter_ingress', index_register, 0)

    if counter_s4 != counter_s1:
        print("Packets were lost on the link from port 2 of s4 to port 3 of s1")
        
    print("Before Sleep: ", controllers['s1'].register_read('active_counter_index', 0))
    print("Before Sleep: ", controllers['s2'].register_read('active_counter_index', 0))
    print("Before Sleep: ", controllers['s3'].register_read('active_counter_index', 0))
    print("Before Sleep: ", controllers['s4'].register_read('active_counter_index', 0))
    time.sleep(1)