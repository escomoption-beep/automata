import flet as ft
from tkinter import Tk, filedialog
from utils.utilidades import Indicador

class Calcular_cerraduras_view:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Calculo de Cerraduras"
        self.page.theme_mode = ft.ThemeMode.DARK

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

        self.go_calcular_subcadenas = ft.ElevatedButton(
            icon= ft.Icons.FUNCTIONS,
            text="Calcular Subcadenas",
            on_click= lambda _: self.page.go("/calcular_subcadenas"),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.RED,
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

        self.ind_alfabeto = Indicador()
        self.alfabeto_text = ft.Text("Ingresa un alfabeto(Σ):")
        self.alfabeto_tf = ft.TextField(
            hint_text="a,b,c",
            label="Alfabeto:",
            expand=True
        )
        self.alfabeto_button = ft.IconButton(
            icon=ft.Icons.SAVE,
            on_click = self.procesar_alfabeto
        )
        self.alfabeto = []
        self.positiva = []
        self.kleene = []

        
        self.ind_longitud = Indicador()
        self.longitud_tf = ft.TextField(
            hint_text="3",
            label="Longitud:",
            width=100
        )
        self.longitud = None

        self.resultados = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            height=450,
            width=650
        )
    
    def build(self) -> ft.View:
        return ft.View(
            route="/calcular_cerraduras",
            controls=[
                ft.Column(
                    width=700,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls= [
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                self.go_home,
                                self.go_calcular_subcadenas,
                                self.create_automata_button
                            ]
                        ),

                        ft.Row(
                            controls = [
                                self.ind_alfabeto,
                                self.alfabeto_text
                            ]
                        ),

                        ft.Row(
                            controls = [
                                self.alfabeto_tf,
                                self.longitud_tf,
                                self.alfabeto_button,
                            ]
                        ),

                        ft.Row(
                            controls= [
                                ft.Card(    
                                    content= ft.Container(
                                        content= ft.Column(             
                                            controls= [
                                                ft.Row(
                                                    controls = [
                                                        ft.Text(
                                                            "Resultado:",
                                                            weight=ft.FontWeight.BOLD,
                                                            size=18
                                                        ),
                                                        ft.TextButton(
                                                            icon=ft.Icons.SAVE_AS,
                                                            text="Guardar como...",
                                                            on_click=self.save_txt
                                                        )
                                                    ]
                                                ),
                                                self.resultados
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
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    def parse_symbol_groups(self, cadena):
        elementos = cadena.split(',')
        return list(dict.fromkeys([x.replace(' ', '') for x in elementos]))
    
    def procesar_alfabeto(self, e):
        self.resultados.controls.clear()
        self.alfabeto = []
        flag = False
        #Si no hay ningun elemento en el alfabeto
        self.longitud = int(self.longitud_tf.value)
        if (not self.alfabeto_tf.value.strip()) or (not self.longitud):
            self.alfabeto_tf.error_text = "No puede estar vacio"
            self.longitud_tf.error_text = "Ingresa un numero entero"
            self.ind_alfabeto.change_color(False)
            flag = False
        #Creamos el alfabeto
        else:
            self.alfabeto_tf.error_text = None
            self.longitud_tf.error_text = None
            self.alfabeto = self.parse_symbol_groups(self.alfabeto_tf.value)
            self.longitud = int(self.longitud_tf.value)
            self.ind_alfabeto.change_color(True)
            print(self.alfabeto) 
            print(self.longitud) 
            flag = True
            
        if flag:
            self.positiva = self.generar_cerraduras(alfabeto=self.alfabeto, longitud=self.longitud)
            self.kleene = self.positiva.copy()
            self.kleene.insert(0,'λ')
            #Cerradura de Kleene
            self.agregar_seccion_resultado("Cerradura de Kleene (Σ*)", self.kleene, "#009E00")
            #Cerradura Positiva
            self.agregar_seccion_resultado("Cerradura Positiva (Σ+)", self.positiva, "#000899") 
    
        self.page.update()

    def agregar_seccion_resultado(self, titulo, elementos, color_fondo):
        seccion = ft.Container(
            content=ft.Column([
                ft.Text(f"{titulo} ({len(elementos)} elementos):", 
                    size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Text(
                        ", ".join([f"'{elem}'"  for elem in elementos]),
                        selectable=True,
                        color=ft.Colors.BLACK
                    ),
                    bgcolor="#D5D5D5",
                    padding=10,
                    border_radius=3,
                    border=ft.border.all(1, "#161616")
                )
            ]),
            bgcolor=color_fondo,
            padding=10,
            border_radius=5,
            margin=ft.margin.only(bottom=10)
        )
        self.resultados.controls.append(seccion)

    
    def generar_cerraduras(self, alfabeto:list, longitud:int):
        def backtrack(actual):
            if 0 < len(actual) <= longitud:
                resultado.append(actual)
            if len(actual) == longitud:
                return
            for letra in alfabeto:
                backtrack(actual + letra)
        resultado = []
        backtrack('')
        return sorted(resultado, key=lambda x: (len(x), x))
    
    def save_txt(self, e):
        try:
            root = Tk()
            root.withdraw()
            root.wm_attributes('-topmost',1)

            file = filedialog.asksaveasfilename(
                title="Guardar Cerraduras",
                defaultextension=".txt",
                filetypes=[("Archivos TXT", "*.txt")],
                initialfile="cerraduras.txt"
            )
            root.destroy()

            if file:
                with open(file, mode='w', encoding='utf-8') as f:
                    f.write("==== Cerradura de Kleene (Σ*) ====\n")
                    for palabra in self.kleene:
                        f.write(f"{palabra}\n")
                    
                    f.write("\n==== Cerradura Positiva (Σ⁺) ====\n")
                    for palabra in self.positiva:
                        f.write(f"{palabra}\n")

            else:
                print("❌ Operación cancelada")

        except Exception as ex:
            print(f"❌ Error al guardar: {ex}")