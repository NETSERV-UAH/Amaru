#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
from collections import namedtuple, OrderedDict

# GLOBAL DEFINITIONS
# key=srcNode+addressAssign; value=namedtuple(destNode, srcNode, addressAssigned)
addrRecord = namedtuple('msg', 'dest src addr')
# A dictionary of elements: {node:{neighbornode:AMport}}
Amnet = {}
# A dictionary of elements: {node:list of AMaddresses}
Amaru_Address = {}

def assignAmaruIDsWithOutSyn(net, num_prefijo, num_dir):
	"""
	# A dictionary of elements: {node:{neighbornode:ETport}}
	Amnet = {}
	"""

	# select core nodes, para amaru solo existe un core 0s0
	coreNodeList = []
	for node in net:
		if node.startswith('0s0'):
			coreNodeList.append(node)
	coreNodeList.sort() #orndemos los cores
	pendingCoreNodeList = list(coreNodeList) #los listamos para saber por donde han pasado

	for node in net.keys():
		if node not in coreNodeList:
			idx = 1
			Amnet[node] = {}
			for neighbor in net[node].keys():
				Amnet[node][neighbor] = str(idx)
				idx = idx + 1 

	i = 1 # ETorii addresses starts by '1'
	for node in coreNodeList:
		addr = str(i) + '.'
		Amnet[node] = {}
		Amaru_Address[node] = []
		Amaru_Address[node].append(addr)
		i += 1
	print 'Core nodes: ', coreNodeList, Amaru_Address

	pendingSetAddressMessages = OrderedDict() #diccionario que inidica que elementos quedan por asignar
	addrRecord = namedtuple('msg', 'dest src addr')

	num_pkt = 0; #numero de paquetes en la red
	for coreNode in coreNodeList: #vamos con lo duro, seleccionamos un core
		print '-----------------------'
		print 'Core node: ', coreNode
		print
		
		assignPortsToCoreNeighbors(coreNode, net)
		print 'Amnet[', coreNode, ']', Amnet[coreNode]
		
		for neighbor in net[coreNode].keys():
			AMaddress = Amnet[coreNode][neighbor] + '.'
			print AMaddress ,
			setMsgInfo = addrRecord(neighbor, coreNode, AMaddress )
			print setMsgInfo
			pendingSetAddressMessages[neighbor + '+' + AMaddress ] = setMsgInfo

		while len(pendingSetAddressMessages):
			node = processSetAddressMessage(pendingSetAddressMessages, int(num_prefijo), int(num_dir))
			if not node.startswith('h'):
				num_pkt = num_pkt + 1
		
	return Amaru_Address, num_pkt

def assignPortsToCoreNeighbors(core, net):

	maxPortInUse = 0
	for neighbor in Amnet[core]:
		port = int(Amnet[core][neighbor].split('.')[1])
		if port > maxPortInUse:
			maxPortInUse = port
	print 'Max port in use', maxPortInUse
	print Amnet[core]

	for neighbor in net[core]:
		if not Amnet[core].has_key(neighbor):
			Amnet[core][neighbor]= Amaru_Address[core][0] + str(maxPortInUse + 1)
			maxPortInUse += 1
			print 'neighbor', neighbor, Amnet[core][neighbor]

def processSetAddressMessage(msgList, Amaru_lim_pre, Amaru_lim_dir):

	# This is a simple dispatcher
	# gets msg from list and delegates processing

	key, val = msgList.popitem(False)     # gets oldest msg
	node = val.dest
	msgSourceNode = val.src
	addr = val.addr

	print '------'
	if node.startswith('0s0'):
		print 'P-'+ node, ' is a core node, stop!'
	elif node.startswith('h'):
		print node, ' is a host,', 'Not assign addr'
	else:
		print node, ' is a middle node,', 'new assign=', addr
		processAddressInMiddleNode(msgList, node, msgSourceNode, addr, int(Amaru_lim_pre), int(Amaru_lim_dir))
	return node;

def processNewSuffix(node, addr, src):
	"""
	check if forzed port number is already in use to change it
	"""
	oldPort = int(Amnet[node][src])
	#aux = Amaru_Address[node][0].split('.')
	#newPort = int(addr.split('.')[len(aux)-1])
	aux = addr.split('.')
	newPort = int(aux[len(aux)-3])
	if newPort != oldPort:
		maxPort = 0
		for item in Amnet[node].keys():
			if int(Amnet[node][item]) > maxPort:
				maxPort = int(Amnet[node][item])
		for item in Amnet[node].keys():
			if int(Amnet[node][item]) == newPort:
				Amnet[node][item] = str(maxPort + 1)
		Amnet[node][src] = str(newPort)

def processAddressInMiddleNode(msgList, node, src, addr, Amaru_lim_pre, Amaru_lim_dir):

    print "Amnet[node]: ", Amnet[node]
    # We accept all addr except if addr has the same prefix
    sameprefix, pos_newaddr = compareOldAndNewAddresses(addr, node, int(Amaru_lim_pre), int(Amaru_lim_dir))
    if sameprefix:
        print "Discart addr, the new addr has the same prefix";
    else:
		# acceptNewPrimaryAddr(addr, node, 'primary')
		# 1. 
		# 2. Discard previous address/es, accept new primary address
		# 3. Forward address to neighbors
        if pos_newaddr == 0:
            Amaru_Address[node] = []
            Amaru_Address[node].append(addr)
            print 'New primary', Amaru_Address[node]
            if (len(addr.split('.'))-1) > (int(node[0]) + 1):
                processNewSuffix(node, addr, src) 
        else:
            print 'Swap Virtual Mac', Amaru_Address[node]
            Amaru_Address[node].append(addr)
            #ordenamos
            Amaru_Address[node] = sorted(Amaru_Address[node], key=lambda hlmac: len(hlmac), reverse=False)

        for item in Amnet[node].keys():
            if item != src:
                AMaddress = Amaru_Address[node][pos_newaddr] + Amnet[node][item] + '.'
                setMsgInfo = addrRecord(item, node, AMaddress )
                print setMsgInfo
                msgList[item + '+' + AMaddress ] = setMsgInfo

        print Amnet[node]

def compareOldAndNewAddresses(newAddr, node, Amaru_lim_pre, Amaru_lim_dir):

    prefixIsEqual = False
    diffcore = True
    pos = 0
    oldAddr = ""

    if Amaru_Address.has_key(node):
        #introducimos el numero maximo de direcciones que podemos obtener
        print "len(Amaru_Address[node]):",len(Amaru_Address[node])
        if ( len(Amaru_Address[node]) >= Amaru_lim_dir and Amaru_lim_dir != 0):
            prefixIsEqual = True;
        elif newAddr in Amaru_Address[node]: #si existe tal cual en la lista lo eliminamos
            prefixIsEqual = True;
        else: 
		    #Debemos comprar direcciones del mismo nodo si es que existen
            print "newAddr ",newAddr
            for i in range(0,len(Amaru_Address[node])):
                #print "Amaru_Address[",node,"][",i,"]: ",Amaru_Address[node][i]
                pos = pos + 1;
                if samePreffixes(newAddr, Amaru_Address[node][i], int(Amaru_lim_pre)):
                    oldAddr = Amaru_Address[node][i]
                    prefixIsEqual = True;
                    break;

    #Comparar Prefijo
    if Amaru_Address.has_key(node):
        if len(Amaru_Address[node]) >= Amaru_lim_dir and Amaru_lim_dir != 0:
            print node, 'has the max number of addr,', oldAddr,'not insert!'
    if prefixIsEqual: 
        print newAddr, 'has the same addr than', oldAddr

    return prefixIsEqual, pos;

def samePreffixes(new, old, Amaru_lim_pre):
    areSame = True

    newList = new.split('.')
    oldList = old.split('.')

    iter = len(oldList) - 1 
    if len(newList) < len(oldList):
        iter = len(newList) - 1;

    #introducimos el limite de logitud de prefijos
    if (iter  > Amaru_lim_pre and Amaru_lim_pre != 0 ):
        iter =  Amaru_lim_pre 
    #recorro los array para comprobar parte por parte si son iguales
    for pos in range(0, iter ): #quitamos el espacio del final
        if (newList[pos] != oldList[pos]):
            areSame = False
            break;		

    return areSame;

