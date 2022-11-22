/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

//My includes
#include "include/metadata.p4"
#include "include/headers.p4"
#include "include/parsers.p4"

/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    /* TODO: Define the register array(s) that you will use in the ingress pipeline */
    inout register<bit<32>>(2) counter_ingress;
    // counter_ingress.write(0, 0);
    // counter_ingress.write(1, 0);

    action forward(bit<9> egress_port){
        standard_metadata.egress_spec = egress_port;
    }

    table repeater {
        key = {
            standard_metadata.ingress_port: exact;
        }
        actions = {
            forward;
            NoAction;
        }
        size = 2;
        default_action = NoAction;
    }

    apply {
      /* TODO: This is where you need to increment the active counter */
        inout bit<32> temp;
        if (hdr.ipv4.ecn == 0) {
            counter_ingress.read(temp, 0);
            counter_ingress.write(0, temp+1);
        }
        if (hdr.ipv4.ecn == 1) {
            counter_ingress.read(temp, 1);
            counter_ingress.write(1, temp+1);
        }

        repeater.apply();
    }
}

/***********************Receive**************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {

    /* TODO: Define the register array(s) that you will use in the ingress pipeline */
    inout register<bit<32>>(2) counter_egress;
    inout register<bit<32>>(1) active_counter_index;
    // counter_egress.write(0, 0);
    // counter_egress.write(1, 0);
    // active_counter_index.write(0, 0);

    apply {
        /* TODO: This is where you need to increment the active counter */
        inout bit<32> temp;
        inout bit<2> index;
        active_counter_index.read((bit<32>)index, 0);
        counter_egress.read(temp, (bit<32>)index);
        counter_egress.write((bit<32>)index, temp+1);
        /* TODO: You also need to add the values of the active counter in every data packet using the ipv4 ecn field */
        hdr.ipv4.ecn = index;
    }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers  hdr, inout metadata meta) {
    apply { 

    }
}


/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;