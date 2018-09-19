#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
from collections import namedtuple, OrderedDict

# GLOBAL DEFINITIONS
# key=srcNode+addressAssign; value=namedtuple(destNode, srcNode, addressAssigned)
addrRecord = namedtuple('msg', 'dest src addr')
# A dictionary of elements: {node:{neighbornode:AMport}}
AMnet = {}
# A dictionary of elements: {node:list of AMaddresses}
AmaruAddress = {}

def assignAmaruIDsWithSyn(net):
	"""
	# A dictionary of elements: {node:{neighbornode:ETport}}
	AMnet = {}
	"""
	# select core nodes

	coreNodeList = []
	for node in net:
		if node.startswith('0s0'):
			coreNodeList.append(node)
	coreNodeList.sort()
	pendingCoreNodeList = list(coreNodeList)

	for node in net.keys():
		if node not in coreNodeList:
			idx = 1
			AMnet[node] = {}
			for neighbor in net[node].keys():
				AMnet[node][neighbor] = str(idx)
				idx = idx + 1 

	i = 1 # ETorii addresses starts by '1'
	for node in coreNodeList:
		addr = str(i) + '.'
		AMnet[node] = {}
		AmaruAddress[node] = []
		#for port in AMnet[node]:
		#	AMnet[node] = addr + AMnet[node]
		AmaruAddress[node].append(addr)
		i += 1
	print 'Core nodes: ', coreNodeList, AmaruAddress

	pendingSetAddressMessages = OrderedDict()
	# key=srcNode+addressAssign; value=namedtuple(destNode, srcNode, addressAssigned)
	addrRecord = namedtuple('msg', 'dest src addr')


	pkt = 0;
	num_pkt = 0; #numero de paquetes en la red
	for coreNode in coreNodeList:
		print '-----------------------'
		print 'Core node: ', coreNode
		print
		
		assignPortsToCoreNeighbors(coreNode, net)
		print 'AMnet[', coreNode, ']', AMnet[coreNode]
		
		#i = 1
		for neighbor in net[coreNode].keys():
			#AMaddress = AmaruAddress[coreNode][0] + AMnet[coreNode][neighbor] + '.'
			AMaddress = AMnet[coreNode][neighbor] + '.'
			print AMaddress,
			setMsgInfo = addrRecord(neighbor, coreNode, AMaddress)
			print setMsgInfo
			pendingSetAddressMessages[neighbor + '+' + AMaddress] = setMsgInfo

		while len(pendingSetAddressMessages):
			node = processSetAddressMessage(pendingSetAddressMessages)
			if not node.startswith('h'):
				num_pkt = num_pkt + 1
				print "num_pkt: ", num_pkt, "From node: ", node
		
	return AmaruAddress, num_pkt

def assignPortsToCoreNeighbors(core, net):

	maxPortInUse = 0
	for neighbor in AMnet[core]:
		port = int(AMnet[core][neighbor].split('.')[1])
		if port > maxPortInUse:
			maxPortInUse = port
	print 'Max port in use', maxPortInUse
	print AMnet[core]

	for neighbor in net[core]:
		if not AMnet[core].has_key(neighbor):
			AMnet[core][neighbor]= AmaruAddress[core][0] + str(maxPortInUse + 1)
			maxPortInUse += 1
			print 'neighbor', neighbor, AMnet[core][neighbor]

def printOrderedTop(top):
	# top is a dict of node:addressList
	nodeList = top.keys()
	nodeList.sort()
	print nodeList  
	for node in nodeList:
		print node,'>>', top[node]

def processSetAddressMessage(msgList):

	# This is a simple dispatcher
	# gets msg from list and delegates processing

	key, val = msgList.popitem(False)     # gets oldest msg
	node = val.dest
	msgSourceNode = val.src
	addr = val.addr

	print '------'
	if node.startswith('0s0'): #Solo se ejecuta como core el controlador
		print 'P-'+ node, ' is a core node,', 'src=', msgSourceNode, 'new assign=', addr
		processAddressInCoreNode(msgList, node, msgSourceNode, addr)
	#elif node.startswith('h'):
	#	print node, ' is a host,', 'new assign=', addr
	else:
		print node, ' is a middle node,', 'new assign=', addr
		processAddressInMiddleNode(msgList, node, msgSourceNode, addr)
	return node;

def processAddressInCoreNode(msgList, core, src, addr):

	coreSrc = addr[0] # solo me coje el primer digito del prefijo
	#coreSrc = int(addr.split('.')[0]) #JAH: Cambio esta sentencia para coger el prefijo completo
	print 'Core Source->', coreSrc,
	newPort = int(addr.split('.')[1])

	print 'New port->', newPort
 
	if coreSrc < AmaruAddress[core][0][0]: # lower core
		print 'lower core'
		
		if len(AMnet[core]) == 0:
			print 'AMnet de', core, 'vacio'
			AMnet[core][src] = AmaruAddress[core][0] + str(newPort)

		elif not AMnet[core].has_key(src):
			print 'no key', src, AMnet[core]
			
			foundPort = False
			for i in AMnet[core].keys():
				iPort = int(AMnet[core][i].split('.')[1])
				foundPort = iPort == newPort
				print foundPort
				if foundPort: break
			
			if foundPort:  	# we need to create a new self of core
				i = 1
				newId = AmaruAddress[core][0].split('.')[0] + str(i) + '.'
				print 'new id', newId
				while newId in AmaruAddress[core]:
					i = i + 1
					newId = AmaruAddress[core][0].split('.')[0] + str(i) + '.'
				AmaruAddress[core].append(newId)
				print 'New self', AmaruAddress[core]
				AMnet[core][src] = newId + str(newPort)
			else:			# port not found no need to creare a new self
				AMnet[core][src] = AmaruAddress[core][0] + str(newPort)
			print 'No old port, new port =', AMnet[core][src]

		else:
			oldPort = int(AMnet[core][src].split('.')[1])
			print 'old port->', oldPort

			if newPort < oldPort:
				
				foundPort = False
				for i in AMnet[core].keys():
					iPort = int(AMnet[core][i].split('.')[1])
					foundPort = iPort == newPort
					if foundPort: break
				
				if foundPort:  	# we need to create a new self of core
					i = 1
					newId = AmaruAddress[core][0].split('.')[0] + str(i) + '.'
					while newId in AmaruAddress[core]:
						i = i + 1
						newId = AmaruAddress[core][0].split('.')[0] + str(i) + '.'
					AmaruAddress[core].append(newId)
					print 'New self', AmaruAddress[core]
					AMnet[core][src] = newId + str(newPort)
				else:			# port not found no need to creare a new self
					AMnet[core][src] = AmaruAddress[core][0] + str(newPort)

	elif (coreSrc == AmaruAddress[core][0][0]): 	#same core
	
		print 'Same core', 'portAddr=', AMnet[core][src],
		aux1 = int(AMnet[core][src].split('.')[0])
		aux2 = int(coreSrc)
		print aux1, aux2
		if  aux1 == aux2:
			newSelf = coreSrc + AMnet[core][src].split('.')[1] + '.'
			if (newSelf not in AmaruAddress[core]) and (len(AmaruAddress[core]) < len(AMnet[core])):
				print 'NewSelf->', newSelf
				AmaruAddress[core].append(newSelf)

			oldPort = int(AMnet[core][src].split('.')[1])
			print 'old port->', oldPort

			if newPort < oldPort:
				AMnet[core][src] = newSelf + str(newPort)
				AMaddress = newSelf + str(newPort) + '.' 
				setMsgInfo = addrRecord(src, core, AMaddress)
				print setMsgInfo
				msgList[src + '+' + AMaddress] = setMsgInfo
		else:
			print 'Port already unfolded'

			oldPort = int(AMnet[core][src].split('.')[1])
			print 'old port->', oldPort

			if newPort < oldPort:
				AMnet[core][src] = AMnet[core][src].split('.')[0] + '.' + str(newPort)
				AMaddress = AMnet[core][src] + '.' 
				setMsgInfo = addrRecord(src, core, AMaddress)
				print setMsgInfo
				msgList[src + '+' + AMaddress] = setMsgInfo
	else:
		print 'Greater core'

def processNewSuffix(node, addr, src):
	"""
	check if forzed port number is already in use to change it
	"""
	oldPort = int(AMnet[node][src])
	#aux = AmaruAddress[node][0].split('.')
	#newPort = int(addr.split('.')[len(aux)-1])
	aux = addr.split('.')
	newPort = int(aux[len(aux)-3])
	if newPort != oldPort:
		maxPort = 0
		for item in AMnet[node].keys():
			if int(AMnet[node][item]) > maxPort:
				maxPort = int(AMnet[node][item])
		for item in AMnet[node].keys():
			if int(AMnet[node][item]) == newPort:
				AMnet[node][item] = str(maxPort + 1)
		AMnet[node][src] = str(newPort)

def processAddressInMiddleNode(msgList, node, src, addr):

	shorterAddress, lowerAddress, lowerSuffix, equalLengthAddress, equalSuffix, diff_core, pos_newaddr, equalAddr = compareOldAndNewAddresses(addr, node)

	print "AMnet[node]: ", AMnet[node]
	if equalAddr:
		print "Reciev the samen direcction"
		return

	elif shorterAddress or (lowerAddress and equalLengthAddress):
		# acceptNewPrimaryAddr(addr, node, 'primary')
			# 1. 
			# 2. Discard previous address/es, accept new primary address
			# 3. Forward address to neighbors
		if pos_newaddr == 0:
			AmaruAddress[node] = []
			AmaruAddress[node].append(addr)
			print 'New primary', AmaruAddress[node]
			if (len(addr.split('.'))-1) > (int(node[0]) + 1):
				processNewSuffix(node, addr, src) 
		else:
			print 'Swap Virtual Mac', AmaruAddress[node]
			AmaruAddress[node].pop(pos_newaddr)
			AmaruAddress[node].insert(pos_newaddr,addr)
			#deberiamos propagar el nuevo
		
		for item in AMnet[node].keys():
			if item != src:
				AMaddress = AmaruAddress[node][pos_newaddr] + AMnet[node][item] + '.'
				setMsgInfo = addrRecord(item, node, AMaddress)
				print setMsgInfo
				msgList[item + '+' + AMaddress] = setMsgInfo
		
			
		print AMnet[node]
	elif equalLengthAddress:
		if equalSuffix or diff_core:
		# acceptSecondaryAddr(addr, node, 'secondary')
			# 0. Check if the Suffix is the same, if not we put the same and send up
			# 1. accept new secondary address
			# 2. forward address to neighbors			

			AmaruAddress[node].append(addr)
			print 'New secondary', AmaruAddress[node]  
			for item in AMnet[node].keys():
				if item != src:
					AMaddress = addr + AMnet[node][item] + '.' 
					setMsgInfo = addrRecord(item, node, AMaddress)
					print setMsgInfo
					msgList[item + '+' + AMaddress] = setMsgInfo

		else:
			#si no son iguales los sufijos descartamos paquete pero asignamos nuevo puerto al switch
			# 1 Buscamos puerto de entrada
			# 2 Asingamos el Swicth a ese puerto en nuestra entrada
			# 2.1 Buscamos si existe otro switch con ese puerto
			# 2.2 Asignamos el nuevo switch al puerto
			# 3 Descartamos el reenvio
			port_in = 0;
			print "No equalSuffix"
			if (int(AmaruAddress[node][0].split('.')[0]) >= int(addr.split('.')[0])) and (len(AmaruAddress[node][0].split('.')) == len(addr.split('.'))):
				if int(AMnet[node][src]) > int(addr.split('.')[int(len(addr.split('.'))/2)]) or (int(addr.split('.')[0]) == 1):
					port_in = addr.split('.')[int(len(addr.split('.'))/2)]
					print "port_in :", port_in;
			if port_in != 0:
				for switch, port in AMnet[node].iteritems():
					if port == port_in and src != switch:
						port_up = puerto_max(AMnet[node])
						AMnet[node][switch] = str(port_up)
					AMnet[node][src] = port_in #asignamos ese valor
			print AMnet[node]
			
	elif lowerSuffix: # or equalSuffix:
		# acceptNewSuffix(addr, node, 'suffix')
			# 1. process suffix to update port numbers if necessary
			# 2. forward address to 'upper' neighbors
		print 'New Suffix', addr
		if (int(AmaruAddress[node][0].split('.')[0]) >= int(addr.split('.')[0])) and (len(addr.split('.')) - len(AmaruAddress[node][0].split('.')) <= 2 ):
			processNewSuffix(node, addr, src)
			print AMnet[node]
		for item in AMnet[node].keys():
			if item != src and item[0] < node[0]:
				AMaddress = addr + AMnet[node][item] + '.' 
				print "len(AmaruAddress[node][0].split('.'))):", len(AmaruAddress[node][0].split('.')), "len(AMaddress.split('.'): ", len(AMaddress.split('.'))
				print "len(AMaddress.split('.')) - len(AmaruAddress[node][0].split('.'))", len(AMaddress.split('.')) - len(AmaruAddress[node][0].split('.'))
				if (len(AMaddress.split('.')) - len(AmaruAddress[node][0].split('.'))) <= 3:
					setMsgInfo = addrRecord(item, node, AMaddress)
					print setMsgInfo
					msgList[item + '+' + AMaddress] = setMsgInfo
		
	else: print 'nothing to do', addr, 'is greater than', AmaruAddress[node]

def puerto_max(d):
    #""" a) create a list of the dict's keys and values; 
    #    b) return the key with the max value"""  
	max_port = 0
	for switch, port in d.iteritems():
		if max_port < port:
			max_port = int(port);
	return max_port + 1 
	
def compareOldAndNewAddresses(newAddr, node):
	
	EqualAddr = False
	addrIsShorter = True
	addrIsLower = True
	addrIsEqualLength = False
	suffixIsLower = True
	suffixIsEqual = False
	diffcore = True
	pos = 0

	if AmaruAddress.has_key(node):
		#Debemos comprar direcciones del mismo nodo si es que existen
		oldAddr = ""
		pos = 0
		for i in range(0,len(AmaruAddress[node])):
			if not comparePreffixes(newAddr, AmaruAddress[node][i]):
				oldAddr = AmaruAddress[node][i]
				pos = i
				break;
		if oldAddr == "": #si no tenemos coincidencia en el core entonces cogemos la mas prioritaria
			oldAddr = AmaruAddress[node][0]
			pos = 0
		addrIsShorter = newAddr.count('.') < oldAddr.count('.')
		addrIsEqualLength = newAddr.count('.') == oldAddr.count('.')
		addrIsLower = addrIsShorter or (addrIsEqualLength and compareAddresses(newAddr, oldAddr))
		diffcore = comparePreffixes(newAddr, oldAddr)
		if oldAddr == newAddr:
			EqualAddr = True
		
        #Comparar Prefijo
		compSuffixes = compareSuffixes(newAddr, oldAddr)
		if compSuffixes == 'isLower': 
			suffixIsLower = True
			suffixIsEqual = False
		elif compSuffixes == 'isEqual': 
			suffixIsLower = False
			suffixIsEqual = True
		else:
			suffixIsLower = False
			suffixIsEqual = False
				
		if addrIsShorter: print newAddr, 'is shorter than', oldAddr
		if addrIsLower: print newAddr, 'is lower than', oldAddr
		if addrIsEqualLength: print newAddr, 'is equal length than', oldAddr
		if suffixIsLower: print newAddr, 'has a lower suffix than', oldAddr
		if suffixIsEqual: print newAddr, 'has an equal suffix than', oldAddr

		if diffcore: print newAddr, 'has different core than', oldAddr
		if EqualAddr: print newAddr, "is the same direccion than", oldAddr

		
	return addrIsShorter, addrIsLower, suffixIsLower, addrIsEqualLength, suffixIsEqual, diffcore, pos, EqualAddr

def compareAddresses(new, old):
	isLower = False
	
	newList = new.split('.')
	oldList = old.split('.')
	
	newPref = newList.pop(0)
	newList.pop()
	
	oldPref = oldList.pop(0)
	oldList.pop()
	
	if newPref[0] <= oldPref[0]: 
		
		n = min(len(newList),len(oldList))
		i = 0
		while i<n:
			if int(newList[i]) < int(oldList[i]): 
				isLower = True
				break
			elif int(newList[i]) > int(oldList[i]):
				break
			else: i = i + 1

	return isLower

def compareSuffixes(new, old):
	isLower = False
	isEqual = False

	newList = new.split('.')
	oldList = old.split('.')
	newList.pop(0)
	newList.pop()
	oldList.pop(0)
	oldList.pop()
	
	n = min(len(newList),len(oldList))
	
	i = 0
	while i<n:
		if int(newList[i]) < int(oldList[i]): 
			isLower = True
			isEqual = False
			break
		elif int(newList[i]) > int(oldList[i]):
			isLower = False
			isEqual = False
			break
		else: 
			isEqual = True
			i = i + 1

	if isLower: result = 'isLower'
	elif isEqual: result ='isEqual'
	else: result = 'isGreater'

	return result

def comparePreffixes(new, old):
	isdiff = False
	
	newList = new.split('.')
	oldList = old.split('.')
	
	Core_new = newList.pop(0)
	Core_old = oldList.pop(0)

	if int(Core_new) != int(Core_old):
		isdiff = True

	return isdiff
