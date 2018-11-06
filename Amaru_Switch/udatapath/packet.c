/* Copyright (c) 2011, TrafficLab, Ericsson Research, Hungary
 * Copyright (c) 2012, CPqD, Brazil  
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *   * Redistributions of source code must retain the above copyright notice,
 *     this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *   * Neither the name of the Ericsson Research nor the names of its
 *     contributors may be used to endorse or promote products derived from
 *     this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 */

#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <sys/types.h>
#include "datapath.h"
#include "dp_buffers.h"
#include "packet.h"
#include "packets.h"
#include "action_set.h"
#include "ofpbuf.h"
#include "oflib/ofl-structs.h"
#include "oflib/ofl-print.h"
#include "util.h"

#include "dp_actions.h"


struct packet *
packet_create(struct datapath *dp, uint32_t in_port,
    struct ofpbuf *buf, bool packet_out) {
    struct packet *pkt;

    pkt = xmalloc(sizeof(struct packet));

    pkt->dp         = dp;
    pkt->buffer     = buf;
    pkt->in_port    = in_port;
    pkt->action_set = action_set_create(dp->exp);

    pkt->packet_out       = packet_out;
    pkt->out_group        = OFPG_ANY;
    pkt->out_port         = OFPP_ANY;
    pkt->out_port_max_len = 0;
    pkt->out_queue        = 0;
    pkt->buffer_id        = NO_BUFFER;
    pkt->table_id         = 0;

    pkt->handle_std = packet_handle_std_create(pkt);
	
    return pkt;
}

struct packet *
packet_clone(struct packet *pkt) {
    struct packet *clone;

    clone = xmalloc(sizeof(struct packet));
    clone->dp         = pkt->dp;
    clone->buffer     = ofpbuf_clone(pkt->buffer);
    clone->in_port    = pkt->in_port;
    /* There is no case we need to keep the action-set, but if it's needed
     * we could add a parameter to the function... Jean II
     * clone->action_set = action_set_clone(pkt->action_set);
     */
    clone->action_set = action_set_create(pkt->dp->exp);


    clone->packet_out       = pkt->packet_out;
    clone->out_group        = OFPG_ANY;
    clone->out_port         = OFPP_ANY;
    clone->out_port_max_len = 0;
    clone->out_queue        = 0;
    clone->buffer_id        = NO_BUFFER; // the original is saved in buffer,
                                         // but this buffer is a copy of that,
                                         // and might be altered later
    clone->table_id         = pkt->table_id;

    clone->handle_std = packet_handle_std_clone(clone, pkt->handle_std);

    return clone;
}

void
packet_destroy(struct packet *pkt) {
    /* If packet is saved in a buffer, do not destroy it,
     * if buffer is still valid */
     
    if (pkt->buffer_id != NO_BUFFER) {
        if (dp_buffers_is_alive(pkt->dp->buffers, pkt->buffer_id)) {
            return;
        } else {
            dp_buffers_discard(pkt->dp->buffers, pkt->buffer_id, false);
        }
    }

    action_set_destroy(pkt->action_set);
    ofpbuf_delete(pkt->buffer);
    packet_handle_std_destroy(pkt->handle_std);
    free(pkt);
}

char *
packet_to_string(struct packet *pkt) {
    char *str;
    size_t str_size;
    FILE *stream = open_memstream(&str, &str_size);

    fprintf(stream, "pkt{in=\"");
    ofl_port_print(stream, pkt->in_port);
    fprintf(stream, "\", actset=");
    action_set_print(stream, pkt->action_set);
    fprintf(stream, ", pktout=\"%u\", ogrp=\"", pkt->packet_out);
    ofl_group_print(stream, pkt->out_group);
    fprintf(stream, "\", oprt=\"");
    ofl_port_print(stream, pkt->out_port);
    fprintf(stream, "\", buffer=\"");
    ofl_buffer_print(stream, pkt->buffer_id);
    fprintf(stream, "\", std=");
    packet_handle_std_print(stream, pkt->handle_std);
    fprintf(stream, "}");

    fclose(stream);
    return str;
}

/* UAH Modifica */
struct packet * packet_Amaru(struct datapath *dp, uint32_t in_port, bool packet_out, uint8_t level, uint8_t port_out, uint8_t AMAC[AMAC_LEN])
{
	struct packet *pkt = NULL;
	struct ofpbuf *buf = NULL;
	
	uint8_t MAC_BC[ETH_ADDR_LEN] = {0xFF,0xFF,0xFF,0xFF,0xFF,0xFF} , type_array[2] = {0xAA, 0xAA};
	uint8_t Total[LEN_BASIC_PKT], i = 0;
	
	//introducimos la modificacion en la AMAC
	AMAC[level] = port_out; //menos uno para adaptarlo

	for (i=0; i<LEN_BASIC_PKT; i++)
		Total[i]=0x00;
	
	//Creamos el buffer del paquete
	buf = ofpbuf_new(LEN_BASIC_PKT); //(sizeof(struct Amaru_header)+sizeof(struct eth_header)); //sizeof(struct eth_header));
	//lo rellenamos con la broadcast
	ofpbuf_put(buf, MAC_BC,ETH_ADDR_LEN);
	//lo rellenamos con la mac switch       
	ofpbuf_put(buf, dp->ports[1].conf->hw_addr, ETH_ADDR_LEN);
	//le metemos el eth Type
	ofpbuf_put(buf, type_array, 2);
	
	//debemos rellenar el buf de AMARU tambien
	//introducimos el nivel
	ofpbuf_put(buf, &level, 1);
	//introducimos la AMAC en el paquete
	ofpbuf_put(buf, AMAC, AMAC_LEN);
	
	//rellenamos para no tener problems con el paquete
	ofpbuf_put(buf, Total, sizeof(Total));
	
	//Creamos el buffer del paquete
	pkt = packet_create(dp, in_port, buf, packet_out);
	
	//creamos la cabeceras de eth y amaru
	pkt->handle_std->proto->eth = xmalloc(sizeof(struct eth_header));
	memcpy(pkt->handle_std->proto->eth->eth_dst, MAC_BC, ETH_ADDR_LEN);
	memcpy(pkt->handle_std->proto->eth->eth_src, dp->ports[1].conf->hw_addr, ETH_ADDR_LEN);
	pkt->handle_std->proto->eth->eth_type = ETH_TYPE_AMARU;
	
	pkt->handle_std->proto->amaru = xmalloc(sizeof(struct Amaru_header));
	pkt->handle_std->proto->amaru->level = level;
	memcpy(pkt->handle_std->proto->amaru->amac, AMAC, AMAC_LEN);
	
	pkt->handle_std->valid = false;
	
	packet_handle_std_validate(pkt->handle_std); //perdemos la cabecera AMARU

    return pkt;
}

struct packet * packet_Amaru_as_root(struct datapath *dp, uint32_t in_port, bool packet_out)
{
	//creamos la mac todo a 0
	uint8_t AMAC_send[AMAC_LEN] = {0}, level = 0, port_out = 1; //el root tiene level 0 -> por lo tanto el que envia es 1
	
	struct packet * pkt = packet_Amaru(dp, in_port, packet_out, level, port_out, AMAC_send);
	
	return pkt;
}

void packet_Amaru_send(struct packet *pkt, uint32_t out_port)
{
	//dp_actions_output_port(pkt, out_port, pkt->out_queue, pkt->out_port_max_len, 0xffffffffffffffff);
	dp_ports_output_random(pkt->dp, pkt->buffer, pkt->in_port, out_port == OFPP_RANDOM, pkt);
}
