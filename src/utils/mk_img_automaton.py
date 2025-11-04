from graphviz import Digraph
import flet as ft
from collections import defaultdict
import time

def mk_img_automaton(transiciones: dict, estados_finales: list):
    dot = Digraph(format="png")
    dot.attr(rankdir="LR")
    dot.attr(size='8,5')
    
    #crear nodos
    for i, estado in enumerate(transiciones):
        if estado in estados_finales:
            shape = 'doublecircle'
        else:
            shape = 'circle'
        if i == 0:
            dot.node(estado, shape=shape, style='filled', fillcolor='lightblue')
        else:
            dot.node(estado, shape=shape)
    
    #crear transiciones
    transiciones_agrupadas = defaultdict(list)
    for estado in transiciones:
        for simbolo in transiciones[estado]:
            destinos = transiciones[estado][simbolo] #Destino es una listaaaaaaaaaa ksdfjakdjgk
            if destinos:
                for destino in destinos:
                    transiciones_agrupadas[(estado, destino)].append(simbolo)
    
    for (origen, destino), simbolos in transiciones_agrupadas.items():
        label = ",".join(simbolos)
        dot.edge(origen, destino, label=label)
    
    
    filename = f'automata_{int(time.time()*1000)}'
    filepath = dot.render(filename=filename, cleanup=True)
    
    return ft.Image(src=filepath, width=600)