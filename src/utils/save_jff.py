#Kevin Jesus Vazquez Sandria
#Funcion que crea un un jff a partir de listas de estados, estados__finales, alfabeto y el diccionario de transiciones, 
#Valido para ejecutarlo en JFLAP
#RECIBE: alfabeto: list, estados: list, estados_finales: list, transiciones: dict
#RETORNA: None

from tkinter import Tk, filedialog
import xml.etree.ElementTree as ET

def save_jff(alfabeto: list, estados: list, estados_finales: list, transiciones: dict):
    
    try:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost',1)

        file = filedialog.asksaveasfilename(
            title="Guardar Automata",
            defaultextension=".jff",
            filetypes=[("Archivos JFLAP", "*.jff"),
                        ("Archivos AFD", "*.afd")
                    ],
            initialfile="mi_automata.jff"
        )
        root.destroy()

        if file:
            #crea nodo raiz <structure>
            structure = ET.Element('structure')
            #crea <type>fa</type>
            ET.SubElement(structure, 'type').text = 'fa'
            #crea nodo <automaton>
            automaton = ET.SubElement(structure,'automaton')

            estado_a_id = {estado : str(i) for i, estado in enumerate(estados)}
            x_base, y_base = 100, 100
            x_step = 100

            #Agregar EStados
            for i, estado in enumerate(estados):
                state = ET.SubElement(automaton,'state', id = estado_a_id[estado], name = estado)
                ET.SubElement(state, 'x').text = str(x_base + i * x_step)
                ET.SubElement(state, 'y').text = str(y_base)

                if i == 0:
                    ET.SubElement(state,'initial')
                
                if estado in estados_finales:
                    ET.SubElement(state, 'final')
            
            #Agregar Transiciones
            for estado_desde in transiciones:
                for simbolo in transiciones[estado_desde]:
            
                    destinos = transiciones[estado_desde][simbolo]
                    if destinos:
                        for destino in destinos:
                            trans = ET.SubElement(automaton,'transition')
                            ET.SubElement(trans,'from').text = estado_a_id[estado_desde]
                            ET.SubElement(trans,'to').text = estado_a_id[destino] #mod estado hacia
                            ET.SubElement(trans,'read').text = simbolo if simbolo else ''
            
            tree = ET.ElementTree(structure)
            tree.write(file, encoding='utf-8', xml_declaration=True)
            print(f"✅ Autómata guardado en '{file}'")
            print(f"Automata a guardar:")
            print(alfabeto)
            print(estados)
            print(transiciones)
        else:
            print("❌ Operación cancelada")

    except Exception as ex:
        print(f"❌ Error al guardar: {ex}")
    
#alfabeto = ["0","1"]
#estados = ["q0","q1","q2"]
#estados_finales = ["q2"]
#transiciones = {"q0":{"0":"", "1":"q1"},"q1":{"0":"", "1":"q2"},"q2":{"0":"", "1":"q2"}}
#save_jff(alfabeto= alfabeto, estados=estados, estados_finales=estados_finales, transiciones=transiciones)