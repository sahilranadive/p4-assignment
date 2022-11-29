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
    register<bit<32>>(2) counter_ingress_A;
    register<bit<32>>(2) counter_ingress_B;
    register<bit<9>>(1) ingress_port_for_counter_A;
    register<bit<9>>(1) ingress_port_for_counter_B;
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
        bit<32> temp;
        // bit<9> ignored_port;
        // ignore_on_port_ingress.read(ignored_port, 0);
        bit<9> port_counter_A;
        ingress_port_for_counter_A.read(port_counter_A, 0);
        bit<9> port_counter_B;
        ingress_port_for_counter_B.read(port_counter_B, 0);
        if (hdr.ipv4.ecn == 0 && port_counter_A == standard_metadata.ingress_port) {
            counter_ingress_A.read(temp, 0);
            counter_ingress_A.write(0, temp+1);
        }
        if (hdr.ipv4.ecn == 1 && port_counter_A == standard_metadata.ingress_port) {
            counter_ingress_A.read(temp, 1);
            counter_ingress_A.write(1, temp+1);
        }
        if (hdr.ipv4.ecn == 0 && port_counter_B == standard_metadata.ingress_port) {
            counter_ingress_B.read(temp, 0);
            counter_ingress_B.write(0, temp+1);
        }
        if (hdr.ipv4.ecn == 1 && port_counter_B == standard_metadata.ingress_port) {
            counter_ingress_B.read(temp, 1);
            counter_ingress_B.write(1, temp+1);
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
    register<bit<32>>(2) counter_egress_A;
    register<bit<32>>(2) counter_egress_B;
    register<bit<9>>(1) egress_port_for_counter_A;
    register<bit<9>>(1) egress_port_for_counter_B;
    register<bit<32>>(1) active_counter_index_A;
    register<bit<32>>(1) active_counter_index_B;
    // register<bit<9>>(1) ignore_on_port_egress;
    // counter_egress.write(0, 0);
    // counter_egress.write(1, 0);
    // active_counter_index.write(0, 0);

    apply {
        /* TODO: This is where you need to increment the active counter */
        bit<32> temp;
        bit<32> index;
        // active_counter_index.read(index, 0);
        // bit<9> ignored_port;
        // ignore_on_port_egress.read(ignored_port, 0);
        // if (ignored_port != standard_metadata.egress_port) {
        //     counter_egress.read(temp, index);
        //     counter_egress.write(index, temp+1);
        // }
        bit<9> port_counter_A;
        egress_port_for_counter_A.read(port_counter_A, 0);
        bit<9> port_counter_B;
        egress_port_for_counter_B.read(port_counter_B, 0);
        if (port_counter_A == standard_metadata.egress_port) {
            active_counter_index_A.read(index, 0);
            counter_egress_A.read(temp, index);
            counter_egress_A.write(index, temp + 1);
        }
        if (port_counter_B == standard_metadata.egress_port) {
            active_counter_index_B.read(index, 0);
            counter_egress_B.read(temp, index);
            counter_egress_B.write(index, temp + 1);
        }

        /* TODO: You also need to add the values of the active counter in every data packet using the ipv4 ecn field */
        hdr.ipv4.ecn = (bit<2>)(index);
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