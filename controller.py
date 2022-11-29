from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI # Not needed anymore
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI

import time

topo = load_topo('topology.json')
controllers = {}
counter_index = 0

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

controllers['s1'].register_write('counter_ingress_A', 0, 0)
controllers['s1'].register_write('counter_ingress_A', 1, 0)
controllers['s2'].register_write('counter_ingress_A', 0, 0)
controllers['s2'].register_write('counter_ingress_A', 1, 0)
controllers['s3'].register_write('counter_ingress_A', 0, 0)
controllers['s3'].register_write('counter_ingress_A', 1, 0)
controllers['s4'].register_write('counter_ingress_A', 0, 0)
controllers['s4'].register_write('counter_ingress_A', 1, 0)

controllers['s1'].register_write('counter_ingress_B', 0, 0)
controllers['s1'].register_write('counter_ingress_B', 1, 0)
controllers['s2'].register_write('counter_ingress_B', 0, 0)
controllers['s2'].register_write('counter_ingress_B', 1, 0)
controllers['s3'].register_write('counter_ingress_B', 0, 0)
controllers['s3'].register_write('counter_ingress_B', 1, 0)
controllers['s4'].register_write('counter_ingress_B', 0, 0)
controllers['s4'].register_write('counter_ingress_B', 1, 0)

controllers['s1'].register_write('counter_egress_A', 0, 0)
controllers['s1'].register_write('counter_egress_A', 1, 0)
controllers['s2'].register_write('counter_egress_A', 0, 0)
controllers['s2'].register_write('counter_egress_A', 1, 0)
controllers['s3'].register_write('counter_egress_A', 0, 0)
controllers['s3'].register_write('counter_egress_A', 1, 0)
controllers['s4'].register_write('counter_egress_A', 0, 0)
controllers['s4'].register_write('counter_egress_A', 1, 0)

controllers['s1'].register_write('counter_egress_B', 0, 0)
controllers['s1'].register_write('counter_egress_B', 1, 0)
controllers['s2'].register_write('counter_egress_B', 0, 0)
controllers['s2'].register_write('counter_egress_B', 1, 0)
controllers['s3'].register_write('counter_egress_B', 0, 0)
controllers['s3'].register_write('counter_egress_B', 1, 0)
controllers['s4'].register_write('counter_egress_B', 0, 0)
controllers['s4'].register_write('counter_egress_B', 1, 0)

controllers['s1'].register_write('active_counter_index_A', 0, 0)
controllers['s2'].register_write('active_counter_index_A', 0, 0)
controllers['s3'].register_write('active_counter_index_A', 0, 0)
controllers['s4'].register_write('active_counter_index_A', 0, 0)

controllers['s1'].register_write('active_counter_index_B', 0, 0)
controllers['s2'].register_write('active_counter_index_B', 0, 0)
controllers['s3'].register_write('active_counter_index_B', 0, 0)
controllers['s4'].register_write('active_counter_index_B', 0, 0)

controllers['s1'].register_write('ingress_port_for_counter_A', 0, 3)
controllers['s1'].register_write('ingress_port_for_counter_B', 0, 2)
controllers['s1'].register_write('egress_port_for_counter_A', 0, 2)
controllers['s1'].register_write('egress_port_for_counter_B', 0, 3)

controllers['s2'].register_write('ingress_port_for_counter_A', 0, 1)
controllers['s2'].register_write('ingress_port_for_counter_B', 0, 2)
controllers['s2'].register_write('egress_port_for_counter_A', 0, 2)
controllers['s2'].register_write('egress_port_for_counter_B', 0, 1)

controllers['s3'].register_write('ingress_port_for_counter_A', 0, 1)
controllers['s3'].register_write('ingress_port_for_counter_B', 0, 3)
controllers['s3'].register_write('egress_port_for_counter_A', 0, 3)
controllers['s3'].register_write('egress_port_for_counter_B', 0, 1)

controllers['s4'].register_write('ingress_port_for_counter_A', 0, 1)
controllers['s4'].register_write('ingress_port_for_counter_B', 0, 2)
controllers['s4'].register_write('egress_port_for_counter_A', 0, 2)
controllers['s4'].register_write('egress_port_for_counter_B', 0, 1)


def print_link(s1, s2, index):
    # We recommend to implement a function that prints the value of the
    # counters used for a particular link and direction.
    # It will help you to debug.
    # However, this is not mandatory. If you do not do it,
    # we won't deduct points.
    counter_s1_A = controllers[s1].register_read('counter_egress_A', index)
    counter_s1_B = controllers[s1].register_read('counter_ingress_B', index)
    
    counter_s2_A = controllers[s2].register_read('counter_ingress_A', index)
    counter_s2_B = controllers[s2].register_read('counter_egress_B', index)
    print ("On link from ",s1, " to ",s2)
    print("previously active egress counter A: ", s1, " ", counter_s1_A) 
    print("previously active ingress counter A: ", s2, " ", counter_s2_A) 

    print ("On link from ",s2, " to ",s1)
    print("previously active egress counter B: ", s2, " ", counter_s2_B) 
    print("previously active ingress counter B: ", s1, " ", counter_s1_B, "\n") 

while True:
    counter_index = 1-counter_index
    # This is where you need to write most of your code.
    controllers['s1'].register_write('active_counter_index_A', 0, counter_index)
    controllers['s2'].register_write('active_counter_index_B', 0, counter_index)

    counter_s1_egress = controllers['s1'].register_read('counter_egress_A', 1-counter_index)
    counter_s2_ingress = controllers['s2'].register_read('counter_ingress_A', 1-counter_index)

    counter_s1_ingress = controllers['s1'].register_read('counter_ingress_B', 1-counter_index)
    counter_s2_egress = controllers['s2'].register_read('counter_egress_B', 1-counter_index)
    
    print_link('s1','s2', 1-counter_index)
    controllers['s1'].register_write('counter_egress_A', 1-counter_index, 0)
    controllers['s2'].register_write('counter_ingress_A', 1-counter_index, 0)

    controllers['s1'].register_write('counter_ingress_B', 1-counter_index, 0)
    controllers['s2'].register_write('counter_egress_B', 1-counter_index, 0)
    if counter_s1_egress != counter_s2_ingress:
        print("Packets were lost on the link from port 2 of s1 to port 1 of s2")
    if counter_s1_ingress != counter_s2_egress:
        print("Packets were lost on the link from port 1 of s2 to port 2 of s1")
    



    controllers['s2'].register_write('active_counter_index_A', 0, counter_index)
    controllers['s3'].register_write('active_counter_index_B', 0, counter_index)

    counter_s2_egress = controllers['s2'].register_read('counter_egress_A', 1-counter_index)
    counter_s3_ingress = controllers['s3'].register_read('counter_ingress_A', 1-counter_index)

    counter_s2_ingress = controllers['s2'].register_read('counter_ingress_B', 1-counter_index)
    counter_s3_egress = controllers['s3'].register_read('counter_egress_B', 1-counter_index)
    
    print_link('s2','s3', 1-counter_index)

    controllers['s2'].register_write('counter_egress_A', 1-counter_index, 0)
    controllers['s3'].register_write('counter_ingress_A', 1-counter_index, 0)

    controllers['s2'].register_write('counter_ingress_B', 1-counter_index, 0)
    controllers['s3'].register_write('counter_egress_B', 1-counter_index, 0)
    if counter_s2_egress != counter_s3_ingress:
        print("Packets were lost on the link from port 2 of s2 to port 1 of s3")
    if counter_s2_ingress != counter_s3_egress:
        print("Packets were lost on the link from port 1 of s3 to port 2 of s2")

    

    controllers['s3'].register_write('active_counter_index_A', 0, counter_index)
    controllers['s4'].register_write('active_counter_index_B', 0, counter_index)

    counter_s3_egress = controllers['s3'].register_read('counter_egress_A', 1-counter_index)
    counter_s4_ingress = controllers['s4'].register_read('counter_ingress_A', 1-counter_index)

    counter_s3_ingress = controllers['s3'].register_read('counter_ingress_B', 1-counter_index)
    counter_s4_egress = controllers['s4'].register_read('counter_egress_B', 1-counter_index)
    
    print_link('s3','s4', 1-counter_index)
    controllers['s3'].register_write('counter_egress_A', 1-counter_index, 0)
    controllers['s4'].register_write('counter_ingress_A', 1-counter_index, 0)

    controllers['s3'].register_write('counter_ingress_B', 1-counter_index, 0)
    controllers['s4'].register_write('counter_egress_B', 1-counter_index, 0)
    if counter_s3_egress != counter_s4_ingress:
        print("Packets were lost on the link from port 3 of s3 to port 1 of s4")
    if counter_s3_ingress != counter_s4_egress:
        print("Packets were lost on the link from port 1 of s4 to port 3 of s3")

    

    controllers['s4'].register_write('active_counter_index_A', 0, counter_index)
    controllers['s1'].register_write('active_counter_index_B', 0, counter_index)

    counter_s4_egress = controllers['s4'].register_read('counter_egress_A', 1-counter_index)
    counter_s1_ingress = controllers['s1'].register_read('counter_ingress_A', 1-counter_index)

    counter_s4_ingress = controllers['s4'].register_read('counter_ingress_B', 1-counter_index)
    counter_s1_egress = controllers['s1'].register_read('counter_egress_B', 1-counter_index)
    
    print_link('s4','s1', 1-counter_index)
    controllers['s4'].register_write('counter_egress_A', 1-counter_index, 0)
    controllers['s1'].register_write('counter_ingress_A', 1-counter_index, 0)

    controllers['s4'].register_write('counter_ingress_B', 1-counter_index, 0)
    controllers['s1'].register_write('counter_egress_B', 1-counter_index, 0)
    if counter_s4_egress != counter_s1_ingress:
        print("Packets were lost on the link from port 2 of s4 to port 3 of s1")
    if counter_s4_ingress != counter_s1_egress:
        print("Packets were lost on the link from port 3 of s1 to port 2 of s4")
        
    time.sleep(1)