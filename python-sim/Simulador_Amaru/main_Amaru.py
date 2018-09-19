#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
from collections import namedtuple, OrderedDict
from AmaruAddressAssignWithOutSyn import *
from AmaruAddressAssignWithSyn import *
import time

def readNetFromFile(fn):
	"""
	Creates the network dictionary of nodes and vertices from a given readNetFromFile
	"""
		
	In = {}
	aux1 = {}
	aux2 = {}

	f = open(fn, 'r')

	for line in f:
		foundEdge = False
		claves = line.split()
		if len(claves) > 3 and claves[1] == 'duplex-link':
			foundEdge = True
			nodo1 = str(claves[2].strip('$ns()'))
			nodo2 = str(claves[3].strip('$ns()'))
			#print 'nodo1', nodo1, 'nodo2', nodo2
		elif len(claves) > 8 and claves[8] == 'E_RT':
			foundEdge = True
			nodo1 = str(claves[1])
			nodo2 = str(claves[2])
			#vacia los dict aux1 y aux 2
		if foundEdge:
			for x in aux1.keys():
					del aux1[x]
			for x in aux2.keys():
					del aux2[x]

			#si ya existe la clave 'nodo' se copia su contenido a aux, y se borra
			if In.has_key(nodo1):
					for x in In[nodo1].keys():
							aux1[x] = In[nodo1][x]
			In[nodo1] = {}
			if In.has_key(nodo2):
					for x in In[nodo2].keys():
							aux2[x] = In[nodo2][x]
			In[nodo2] = {}
			#print In
			#print 'aux1', aux1
			#print 'aux2', aux2
			# se incluyen en aux los nuevos edges
			aux1[nodo2] = 1000
			aux2[nodo1] = 1000
			# se copian los aux a I,  
			for x in aux1.keys():
					In[nodo1][x] = aux1[x]
			for x in aux2.keys():
					In[nodo2][x] = aux2[x]
			#print In

	f.close()

	return In

def printNetworkByNodes(M):
		lista = sorted(M.keys())
		for x in lista:
				print x, M[x]

def printOrderedTop(top):
	# top is a dict of node:addressList
	nodeList = top.keys()
	nodeList.sort()
	print nodeList
	text = ""
	for node in nodeList:
		#print node,'>>', top[node]
		text += str(node)+" >> "+ str(top[node])+"\n"
	return text

def cal_media (topologia):
    Suma_direcciones = 0
    for node in topologia.keys():
        Suma_direcciones += len(topologia[node])
        
    return float(float(Suma_direcciones-1)/float(len(topologia.keys())-1))

def save_data_into_file(file, topology,Syn_amaru, prefijo, num_max_dir):
    aux = "Con-Sincronismo"
    if Syn_amaru != 'y' and Syn_amaru != 'Y':
        aux = "Sin-Sincronismo"
    #open file to save the data
    f_save = open("Resultados/"+str(file)+"_"+str(prefijo)+"_"+str(num_max_dir)+"_"+str(aux)+".txt", 'w');
    f_save.write(topology)
    f_save.closed

def save_stats(main_data, num_pkt, Syn_amaru, prefijo, num_max_dir, topologia):
    aux = "Con-Sincronismo"
    if Syn_amaru != 'y' and Syn_amaru != 'Y':
        aux = "Sin-Sincronismo"
    #open file to save the data
    f_save = open("Resultados/stats.txt", "a+");
    name_topology = main_data.split("-")[0]+"-"+main_data.split("-")[1]
    num_nodes = main_data.split("-")[2]
    nodes_grades = main_data.split("-")[3].split("_")[0]
    semillas = main_data.split("-")[3].split("_")[1].split(".")[0]
    media = cal_media(topologia)
    f_save.write(str(name_topology)+"|"+str(semillas)+"|"+str(num_nodes)+"|"+str(nodes_grades)+"|"+str(num_pkt)+"|"+str(prefijo)+"|"+str(num_max_dir)+"|"+str(aux)+"|"+str(media)+"\n")
    f_save.closed


if __name__ == '__main__':

    # BEGIN
    filepath = raw_input('Nombre del subdirectorio de topologias[./Topologias]: ')
    print
    if (filepath == ''):
        filepath = "Topologias"

    Syn_amaru = raw_input('Aplicar Amaru CON sincronismo (y/n)[N]?: ')
    print
    if (Syn_amaru == ''):
        Syn_amaru = 'N'

    if Syn_amaru != 'y' and Syn_amaru != 'Y':
        num_max_prefijo = raw_input('Longitud Maxima Prefijo [5]: ')
        print
        if (num_max_prefijo == ''):
            num_max_prefijo = 5
    
        num_max_direcciones = raw_input('Numero de Máximo de Direcciones por nodo [5]: ')
        print 
        if (num_max_direcciones == ''):
            num_max_direcciones = 5
        num_max_prefijo = int(num_max_prefijo)+1
        num_max_direcciones = int(num_max_direcciones)+1
    else:
        num_max_prefijo = 3
        num_max_direcciones = 3

    path = os.getcwd() + '/' + filepath
    filenames = os.listdir(path)
    #filenames = ['Irregular_50nodos_media8.top']
    for num_prefijo in range(2, num_max_prefijo):
        for num_dir in range(2, num_max_direcciones):
            #print filenames
            for name in sorted(filenames):
                filename = path + '/' + name
                print
                print '==============================================================='
                print 'Archivo de topologia: ', name
                print
                # Desde el fichero de entrada lee la topologia de enlaces
                I = readNetFromFile(filename)
                printNetworkByNodes(I)
                if Syn_amaru == 'y' or Syn_amaru == 'Y':
                    AmaruAddress, num_pkt = assignAmaruIDsWithSyn(I)
                    num_prefijo = 0
                    num_dir = 0
                else:
                    AmaruAddress, num_pkt = assignAmaruIDsWithOutSyn(I, num_prefijo, num_dir)
                print "Num pkt en la red = ", num_pkt
                #guardamos los datos obtenidos
                #save_data_into_file(filename.split("/")[2].split(".")[0], printOrderedTop(AmaruAddress), Syn_amaru, num_prefijo, num_dir)
                save_stats(filename.split("/")[2], num_pkt, Syn_amaru, num_prefijo, num_dir, AmaruAddress)
