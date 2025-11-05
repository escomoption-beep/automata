import flet as ft
import os
from utils.mk_img_automaton import mk_img_automaton
from utils.load_jff import load_jff
from utils.utilidades import Indicador


class Simulacion_afd_view:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Simulacion y Validacion de Cadenas"
        self.page.theme_mode = ft.ThemeMode.DARK

        self.div = ft.Divider(height=10, thickness=1, color="grey",leading_indent= 20)


        self.alfabeto = None
        self.estados = None
        self.estados_fin = None
        self.transiciones = None
        
        self.go_home = ft.ElevatedButton(
            icon= ft.Icons.HOME,
            text="Ir a la pantalla principal",
            on_click= lambda _: self.page.go("/"),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE,
                color=ft.Colors.WHITE, 
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation={"pressed": 2, "hovered": 4},
            )
        )

        self.load_automata_button = ft.FilledButton(
            icon=ft.Icons.UPLOAD,
            text="Cargar un Autómata",
            on_click=self.cargar_automata,

            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN,
                color=ft.Colors.WHITE, 
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation={"pressed": 2, "hovered": 4},
            )
        )


        self.create_automata_button = ft.ElevatedButton(
            text="Definir/Editar/Visualizar AFD",
            icon=ft.Icons.BUILD_OUTLINED,
            on_click=lambda _: self.page.go("/definir_afd"),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREY_700,
                color=ft.Colors.WHITE, 
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation={"pressed": 2, "hovered": 4},
            )
        )

        self.img_automaton_container = ft.Container(
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            height=300,  
            width=600,
            border=ft.border.all(2, ft.Colors.BLACK),
            border_radius=10,
            padding=15,
            alignment=ft.alignment.top_center, 
            bgcolor=ft.Colors.GREY_600,  
        )

        #Cadena
        self.cadena_text = ft.Text("Ingresa una cadena (w)")
        self.ind_cadena = Indicador()
        self.cadena = ""
        self.cadena_tf = ft.TextField(
            hint_text = "Cadena a validar",
            expand=True,
            read_only= True,
            on_submit=self.procesar_cadena
        )
        self.cadena_button =ft.IconButton(
            icon=ft.Icons.SAVE,
            on_click = self.procesar_cadena,
        )

        self.estado_aceptacion = None
        self.estado_aceptacion_text = ft.Text(
            "",
            color=ft.Colors.ORANGE
        )

        self.resultado_simulacion = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            height=300,
            width=650,
        )


        
    
    def build(self) -> ft.View:
        return ft.View(
            route="/simulacion_afd",
            scroll="Auto",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    width=700,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[

                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                self.go_home,
                                self.load_automata_button,
                                self.create_automata_button 
                            ]
                        ),

                        self.div,
                        self.img_automaton_container,
                        self.div,

                        ft.Row(
                            controls= [
                                self.ind_cadena,
                                self.cadena_text,
                            ]
                        ),
                        ft.Row(
                            controls = [
                                self.cadena_tf,
                                self.cadena_button,
                            ]
                        ),

                        self.estado_aceptacion_text,
                        
                        ft.Row(
                            controls= [
                                ft.Card(    
                                    content= ft.Container(
                                        content= ft.Column(             
                                            controls= [
                                                ft.Text(
                                                    "Resultado de la Simulacion:",
                                                    weight=ft.FontWeight.BOLD,
                                                    size=18
                                                ),
                                                self.resultado_simulacion
                                            ]
                                        ),
                                    padding = 15
                                    ),
                            expand= True
                                ),
                            ]
                        ),
                        

                    ]
                )
            ],
        )
    
    def cargar_automata(self, e):
        self.alfabeto, self.estados, self.estados_fin,self.transiciones = load_jff()
        print("**Automata Cargado:**")
        print(self.alfabeto)
        print(self.estados)
        print(self.estados_fin)
        print(self.transiciones)

        self.ind_cadena.change_color(True)
        self.cadena_tf.read_only = False
        self.generar_imagen(e)
        self.page.update()

    
    def generar_imagen(self, e):
        
        for archivo in os.listdir('.'):
            if archivo.startswith('automata_') and archivo.endswith('.png'):
                try:
                    os.remove(archivo)
                except:
                    pass

        self.img_automaton_container.content.controls.clear()
        
        self.img_automaton = mk_img_automaton(
            transiciones=self.transiciones, 
            estados_finales=self.estados_fin
        )
        
        self.img_automaton_container.content.controls.append(self.img_automaton)
        self.page.update() 
    
    def procesar_cadena(self, e):
        self.cadena = self.cadena_tf.value.replace(' ','')
        print(f"cadena = {self.cadena}")
        self.resultado_simulacion.controls.clear()
    
        self.estado_aceptacion = self.traza_simulacion(cadena=self.cadena, transiciones=self.transiciones, estado_inicial=self.estados[0], estados_finales=self.estados_fin)
        #Texto de rechazo o aceptacion
        if self.estado_aceptacion:
            self.estado_aceptacion_text.value = "Cadena Aceptada"
            self.estado_aceptacion_text.color = ft.Colors.GREEN
        else:
            self.estado_aceptacion_text.value = "Cadena Rechazada"
            self.estado_aceptacion_text.color = ft.Colors.RED

        self.page.update()

    def epsilon_closure(self, estados: list, transiciones: dict):
        clausura = set(estados)
        pila = list(estados)
        
        while pila:
            estado_actual = pila.pop()
            
            # Buscar transiciones lambda desde el estado actual
            if estado_actual in transiciones and 'λ' in transiciones[estado_actual]:
                for estado_destino in transiciones[estado_actual]['λ']:
                    if estado_destino not in clausura:
                        clausura.add(estado_destino)
                        pila.append(estado_destino)
        
        return sorted(clausura)  # Retorna ordenado para consistencia


    def traza_simulacion(self, cadena: str, transiciones: dict, estado_inicial: str, estados_finales: list):
        # Estado inicial con epsilon-closure
        estados_actuales = self.epsilon_closure([estado_inicial], transiciones)
        print(" ↓")
        self.resultado_simulacion.controls.append(ft.Text(" ↓"))
        
        # Configuración inicial
        print(f"({estados_actuales}, {cadena})")
        self.resultado_simulacion.controls.append(ft.Text(f"({estados_actuales}, {cadena})"))
        
        # Procesar cada símbolo en la cadena
        for i, simbolo in enumerate(cadena):
            nuevos_estados = set()  # Usar set para evitar duplicados automáticamente
            
            # Procesar cada estado actual
            for estado in estados_actuales:
                # Verificar si el estado existe en transiciones
                if estado not in transiciones:
                    continue
                
                # Verificar si existe transición con el símbolo
                if simbolo in transiciones[estado] and transiciones[estado][simbolo]:
                    # Agregar estados alcanzables
                    nuevos_estados.update(transiciones[estado][simbolo])
            
            # Si no hay transiciones válidas, rechazar
            if not nuevos_estados:
                print(f" ⊢ RECHAZADA (no hay transición con '{simbolo}')")
                self.resultado_simulacion.controls.append(
                    ft.Text(f" ⊢ RECHAZADA (no hay transición con '{simbolo}')")
                )
                return False
            
            # Aplicar epsilon-closure a los nuevos estados
            estados_con_closure = set()
            for estado in nuevos_estados:
                estados_con_closure.update(self.epsilon_closure([estado], transiciones))
            
            # Actualizar estados actuales (ordenados para consistencia)
            estados_actuales = sorted(estados_con_closure)
            
            # Mostrar transición
            cadena_restante = cadena[i+1:] if i+1 < len(cadena) else "λ"
            print(f" ⊢ ({estados_actuales}, {cadena_restante})")
            self.resultado_simulacion.controls.append(
                ft.Text(f" ⊢ ({estados_actuales}, {cadena_restante})")
            )
        
        # Verificar si algún estado final está en los estados actuales
        aceptada = any(estado in estados_finales for estado in estados_actuales)
        
        
        return aceptada
