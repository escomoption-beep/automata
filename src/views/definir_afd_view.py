#frameworks
import flet as ft

#librerias
import os

#Utiles:
from utils.utilidades import Indicador
from utils.tabla_transiciones import TablaTransiciones
from utils.mk_img_automaton import mk_img_automaton
from utils.load_jff import load_jff
from utils.save_jff import save_jff


class Definir_afd_view:
    def __init__(self, page: ft.Page):

    
        self.page = page
        self.page.title = "Definir AFD"
        self.page.theme_mode = ft.ThemeMode.DARK

############################################################################################
####################################################################################################
        #Botones de Inicio
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

        self.load_automata_button = ft.ElevatedButton(
            icon=ft.Icons.UPLOAD,
            text="Cargar un Automata",
            on_click= self.cargar_automata,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN,
                color=ft.Colors.WHITE, 
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation={"pressed": 2, "hovered": 4},
            )
        )

        self.simular_automata_button = ft.ElevatedButton(
            text="Simular Automata",
            icon=ft.Icons.PLAY_ARROW,
            on_click=lambda _: self.page.go("/simulacion_afd"),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.ORANGE,
                color=ft.Colors.WHITE, 
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation={"pressed": 2, "hovered": 4},
            )
        )
        self.div = ft.Divider(height=10, thickness=1, color="grey",leading_indent= 20)
####################################################################################################
####################################################################################################
        #Alfabeto
        self.alfabeto = []
        self.ind_alfabeto = Indicador()
        self.alfabeto_tf = ft.TextField(
            hint_text = "0,1", 
            on_submit=self.mk_alfabeto,
            expand=True
        )
        
        #Estados
        self.estados = []
        self.ind_estados = Indicador()
        self.estados_tf  = ft.TextField(
            hint_text = "q0, q1, q2", 
            on_submit=self.mk_estados,
            expand=True
        )
        
        #Estados finales
        self.estados_fin = []
        self.ind_estados_fin = Indicador()
        self.estados_fin_tf = ft.TextField(
            hint_text = "q0, q1",
            on_submit=self.mk_estados_fin,
            expand=True     
        )

        #Transiciones
        self.transiciones = {}
        self.transiciones_text = ft.Text(value = "", color=ft.Colors.GREY, style=ft.TextStyle(weight=ft.FontWeight.BOLD))

        #Tabla de inputs
        self.table_container = ft.Row(scroll="horizontal", alignment= ft.MainAxisAlignment.CENTER)
        self.tabla_transiciones = None
        self.table_buttons = ft.Row()

        #Imagen del automata
        self.img_automaton = None

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
        
        self.img_generar_boton = ft.TextButton(
                text= "Generar Imagen del Automata",
                icon=ft.Icons.AUTO_AWESOME_MOSAIC_OUTLINED,
                on_click= self.generar_imagen,
                visible= False
            )
        
        #Boton para Guardar Automata:
        self.save_automaton_button = ft.TextButton(
            visible= False,
            icon = ft.Icons.SAVE_AS,
            text= "Guardar Automata como...",
            on_click= self.guardar_automata
        )



    def build(self) -> ft.View:
        return ft.View(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll= "Auto",
            route="/definir_afd",
            controls=[    
                ft.Column(
                    width = 700,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls= [

                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls = [
                                self.go_home,
                                self.load_automata_button,
                                self.simular_automata_button
                            ]
                            
                        ),

                        #Definicion del Afabeto
                        ft.Row(
                            controls = [
                                self.ind_alfabeto, 
                                ft.Text(" Alfabeto (Σ)")
                            ]
                        ),
                        ft.Row(
                            controls = [
                                self.alfabeto_tf,
                                ft.IconButton(
                                    icon=ft.Icons.SAVE,
                                    on_click= self.mk_alfabeto
                                )
                            ]
                        ),
                        
                        #Definicion del conjunto de estados
                        #El primer elemento sera nuestro estado incial
                        ft.Row(
                            controls = [
                                self.ind_estados,
                                ft.Text(" Conjunto de estados (Q) -> (El primer estado sera el inicial)")
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.estados_tf,
                                ft.IconButton(
                                    icon=ft.Icons.SAVE,
                                    on_click=self.mk_estados
                                )
                            ]
                        ), 

                        #Definicion del conjunto de estados finales
                        ft.Row(
                            controls = [
                                self.ind_estados_fin,
                                ft.Text(" Conjunto de estados Finales (F)"),
                            ]
                        ),
                        
                        ft.Row(
                            controls=[
                                self.estados_fin_tf,
                                ft.IconButton(
                                    icon=ft.Icons.SAVE,
                                    on_click=self.mk_estados_fin
                                )
                            ]
                        ), 

                        self.div,

                        ft.Row(
                            controls = [
                                ft.Text(" Tabla de transiciones (δ): λ", selectable=True),
                                ft.ElevatedButton(
                                text="Crear Tabla de Transiciones/Resetear",
                                on_click= self.mkTabla
                                ),
                                self.transiciones_text,
                            ]
                        ),

                        self.table_container,

                        ft.Row(
                            controls= [
                                self.img_generar_boton,
                                self.save_automaton_button
                            ]
                        ),
                        self.div,
                        self.img_automaton_container,
                        self.div,  
                        
                    ]
                )
            ]
            
        )

    #Convierte un string a lista, limpia el string
    def parse_symbol_groups(self, cadena):
        elementos = cadena.split(',')
        return list(dict.fromkeys([x.replace(' ', '') for x in elementos]))
    
    #ALFABETO
    def mk_alfabeto(self, e):
        self.alfabeto = []
        #Si no hay ningun elemento en el alfabeto
        if not self.alfabeto_tf.value.strip():
            self.alfabeto_tf.error_text = "No puede estar vacio"
            self.ind_alfabeto.change_color(False)
        #Creamos el alfabeto
        else:
            self.alfabeto_tf.error_text = None
            self.alfabeto = self.parse_symbol_groups(self.alfabeto_tf.value)
            self.alfabeto += ['λ']
            self.ind_alfabeto.change_color(True)
            #Resetear las transiciones para forzar la creacion de uno nuevo
            self.transiciones = {}
            
        print(self.alfabeto)
        
        self.page.update()

    #ESTADOS
    def mk_estados(self, e):
        self.estados = []
        #El conjunto de estados no puede estar vacio      
        if not self.estados_tf.value.strip():
            self.estados_tf.error_text = "No puede estar vacio"
            self.ind_estados.change_color(False)
        #Creamos el conjunto de estados, EL ESTADO INICIAL SERA EL PRIMER ESTADO EN LA LISTA
        else:
            self.estados_tf.error_text = None
            self.estados = self.parse_symbol_groups(self.estados_tf.value)
            self.ind_estados.change_color(True)
            #Resetear las transiciones para forzar la creacion de uno nuevo
            self.transiciones = {}
            
        print(self.estados)   
        self.page.update()

    #ESTADOS FINALES
    def mk_estados_fin(self, e): 
        self.estados_fin = []
        #Checamos si los estados base han sido definidos y que el conjunto de estados finales no se nulo
        self.ind_estados_fin.change_color(False)
        if not self.estados_fin_tf.value.strip():
            self.estados_fin_tf.error_text = "No puede estar vacio"  
        if not self.estados:
            self.estados_fin_tf.error_text = "Primero define los estados"
        
        else:
            self.estados_fin_tf.error_text = None
            aux = self.parse_symbol_groups(self.estados_fin_tf.value)
            remove_estados = aux.copy()
            #Checamos que los estados finales esten definidos en los estados base
            for estado in aux:
                if estado not in self.estados:
                    self.estados_fin_tf.error_text = f"Advertencia: {estado} ∉Q, {estado} no se incluyo en la lista de estados finales"
                    remove_estados.remove(estado)
            aux = remove_estados.copy()
            if aux:
                self.ind_estados_fin.change_color(True)
                self.estados_fin = aux.copy()
            
        print(self.estados_fin)
        self.page.update()

    #Crea la Tabla para definir las transiciones;
    def mkTabla(self, e):          
        if(self.ind_alfabeto.status and self.ind_estados.status and self.ind_estados_fin.status):
            
            self.transiciones_text.value = "¡Tabla creada!"
            self.transiciones_text.color = ft.Colors.GREEN
            self.table_container.controls.clear()
            
            # Crear la tabla
            self.tabla_transiciones = TablaTransiciones(
                estados=self.estados, 
                alfabeto=self.alfabeto, 
                transiciones=self.transiciones
            )
            
            if not self.transiciones:
                self.tabla_transiciones.create_dicc_trans()
            
            self.table_container.controls.append(self.tabla_transiciones.build())
            print(self.transiciones)
            self.img_generar_boton.visible = True
            
            self.page.update()
        else: 
            self.transiciones_text.value = "¡Antes llene los campos correctamente!"
            self.transiciones_text.color = ft.Colors.RED
            self.page.update()

    def generar_imagen(self, e):
        # Limpiar imágenes anteriores
        for archivo in os.listdir('.'):
            if archivo.startswith('automata_') and archivo.endswith('.png'):
                try:
                    os.remove(archivo)
                except:
                    pass

        self.img_automaton_container.content.controls.clear()
        
        # IMPORTANTE: Obtener las transiciones actualizadas de la tabla
        transiciones_actualizadas = self.tabla_transiciones.obtener_transiciones()
        
        self.img_automaton = mk_img_automaton(
            transiciones=transiciones_actualizadas, 
            estados_finales=self.estados_fin
        )
        
        self.img_automaton_container.content.controls.append(self.img_automaton)
        self.save_automaton_button.visible = True
        self.page.update() 

    

    def guardar_automata(self, e):
        save_jff(self.alfabeto, self.estados, self.estados_fin, self.transiciones)        

    def cargar_automata(self, e):
        self.alfabeto, self.estados, self.estados_fin,self.transiciones = load_jff()

        print("**Automata Cargado:**")
        print(self.alfabeto)
        print(self.estados)
        print(self.estados_fin)

        #Alfabeto
        self.alfabeto_tf.value = ",".join(str(x) for x in self.alfabeto)
        self.ind_alfabeto.change_color(True)
        #Estados
        self.estados_tf.value = ",".join(str(x) for x in self.estados)
        self.ind_estados.change_color(True)
        #Estados Finales
        self.estados_fin_tf.value = ",".join(str(x) for x in self.estados_fin)
        self.ind_estados_fin.change_color(True)
        #Transiciones
        print(self.transiciones)
        self.mkTabla(e)
        self.generar_imagen(e)
        
        self.page.update()