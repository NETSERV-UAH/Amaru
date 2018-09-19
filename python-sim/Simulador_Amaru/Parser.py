#! /usr/bin/python
# -*- coding: utf-8 -*-
import os

def parser_brite_to_sim_python(Directorio):
    file_edges = "node\\recovery_on\\RyuFileEdges.txt"
    file_nodes = "node\\recovery_on\\RyuFileNodes.txt"
    
    #obtenemos todos los nombres de todos los directorios
    path = os.getcwd()+"\\"+Directorio
    #name_topo
    folders = os.listdir(path)
    print folders
    for folder in folders:
        num_nodes_topo = 0;
        #primero leemos el numero de nodos que tiene la topologia
        try:
            file = open(path+"\\"+folder+"\\"+file_nodes, 'r')
            for line in file:
                datos = line.split(";")
                if (num_nodes_topo < int(datos[0])):
                    num_nodes_topo = int(datos[0])
            print "Numero de nodos en la topologia: "+str(num_nodes_topo)
        except:
            print "Error al leer los nodos Archivo: "+path+"\\"+folder+"\\"+file_nodes+" no encontrado"

        try:
            for num_node in range(1,num_nodes_topo+1):
                topology_original = open(path+"\\"+folder+"\\"+file_edges, 'r')
                topology_parseada = open(path+"\\..\\Topologias\\"+folder+"_"+str(num_node)+".top", 'w')
                for line in topology_original:
                    datos = line.split(";")
                    if (int(datos[0]) == num_node):
                        node1 = "$n(0s0)" #marcamos el controller 
                    else:
                        node1 = "$n(1s"+str(int(datos[0]))+")"
                    if (int(datos[1]) == num_node):
                        node2 = "$n(0s0)" #marcamos el controller 
                    else:
                        node2 = "$n(1s"+str(int(datos[1]))+")"
                    line = "$topJAC\tduplex-link\t"+str(node1)+"\t"+str(node2)+"\n"
                    topology_parseada.write(line)
                topology_original.closed
                topology_parseada.closed
        except:
            print "Error al leer los enlaces Archivo: "+path+"\\"+folder+"\\"+file_edges+" no encontrado"


if __name__ == '__main__':
    Directorio = raw_input('Nombre del subdirectorio de topologias[./Topologias_Brite]: ')
    print
    if (Directorio == ''):
        Directorio = "Topologias_Brite"
    parser_brite_to_sim_python(Directorio)