#! /usr/bin/python
# -*- coding: utf-8 -*-
import os

def parser_brite_to_sim_python(Directorio):
    file_look_for = "RyuFileEdges.txt"

    #obtenemos todos los nombres de todos los directorios
    path = os.getcwd()+"\\"+Directorio
    #name_topo
    folders = os.listdir(path)
    print folders
    for folder in folders:
        topology_original = open(path+"\\"+folder+"\\"+file_look_for, 'r')
        topology_parseada = open(path+"\\..\\Topologias\\"+folder+".top", 'w')
        for line in topology_original:
            datos = line.split(";")
            if (int(datos[0])-1) == 0:
                node1 = "$n(0s0)" #marcamos el controller 
            else:
                node1 = "$n(1s"+str(int(datos[0])-1)+")"
            if (int(datos[1])-1) == 0:
                node2 = "$n(0s0)" #marcamos el controller 
            else:
                node2 = "$n(1s"+str(int(datos[1])-1)+")"
            line = "$topJAC\tduplex-link\t"+str(node1)+"\t"+str(node2)+"\n"
            topology_parseada.write(line)
        topology_original.closed
        topology_parseada.closed


if __name__ == '__main__':
    Directorio = raw_input('Nombre del subdirectorio de topologias[./Topologias_Brite]: ')
    print
    if (Directorio == ''):
        Directorio = "Topologias_Brite"
    parser_brite_to_sim_python(Directorio)