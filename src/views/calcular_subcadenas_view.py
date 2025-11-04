import flet as ft
from tkinter import Tk, filedialog
from utils.utilidades import Indicador

class Calcular_subcadenas_view:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Calculo de Subcadenas"
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

        self.go_calcular_cerraduras = ft.ElevatedButton(
            icon= ft.Icons.FUNCTIONS,
            text="Calcular Cerraduras",
            on_click= lambda _: self.page.go("/calcular_cerraduras"),
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

        self.ind_cadena = Indicador()
        self.cadena_text = ft.Text("Ingresa una Cadena(w):")
        self.cadena_tf = ft.TextField(
            hint_text="abc",
            expand=True,
            label="Cadena(w)",
            on_submit = self.procesar_subcadenas
        )
        self.cadena_button = ft.IconButton(
            icon=ft.Icons.SAVE,
            on_click = self.procesar_subcadenas 
        )
        self.cadena = ""
        self.substring_list = []
        self.suffix_list = []
        self.prefix_list = []

        self.resultados = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            height=450,
            width=650
        )


    
    def build(self) -> ft.View:
        return ft.View(
            route="/calcular_subcadenas",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    width=700,
                    controls= [
                        
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                self.go_home,
                                self.go_calcular_cerraduras,
                                self.create_automata_button 
                            ]
                        ),

                        ft.Row(
                            controls=[
                                self.ind_cadena,
                                self.cadena_text
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.cadena_tf,
                                self.cadena_button
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
        )
    
    
    
    def prefix(self, cadena: str):
            l = []
            for i in range(len(cadena) + 1):
                    l.append(cadena[:i])

            l = sorted(l, key=lambda x: (len(x), x))
            l = ["λ" if x == "" else x for x in l]

            return l

    def suffix(self, cadena:str):
            l = []
            for i in range(len(cadena)+1):
                    l.append(cadena[i:])
            l = sorted(l, key=lambda x: (len(x), x))
            l = ["λ" if x == "" else x for x in l]
            
            return l

    def substring(self, cadena:str):
            l = set()
            for i in range(len(cadena)):
                    for j in range(i + 1, len(cadena) + 1):
                            #print(s[i:j])
                            l.add(cadena[i:j])
            l = list(l)
            l = sorted(l, key=lambda x: (len(x), x))
            l.insert(0, "λ")
            return l

    def procesar_subcadenas(self, e):

        self.resultados.controls.clear()
        self.ind_cadena.change_color(True)
        self.cadena = self.cadena_tf.value
        self.substring_list = self.substring(self.cadena)
        self.prefix_list = self.prefix(self.cadena)
        self.suffix_list = self.suffix(self.cadena)
        #Subcadenas
        self.agregar_seccion_resultado("Subcadenas", self.substring_list, "#009E00")
        #Prefijos
        self.agregar_seccion_resultado("Prefijos",self.prefix_list, "#000899")       
        #Sufijos
        self.agregar_seccion_resultado("Sufijos",self.suffix_list, "#A40024")
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
    
    def save_txt(self, e):
        try:
            root = Tk()
            root.withdraw()
            root.wm_attributes('-topmost',1)

            file = filedialog.asksaveasfilename(
                title="Guardar Subcadenas",
                defaultextension=".txt",
                filetypes=[("Archivos TXT", "*.txt")],
                initialfile="subcadenas.txt"
            )
            root.destroy()

            if file:
                with open(file, mode='w', encoding='utf-8') as f:
                    f.write("==== Subcadenas ====\n")
                    for palabra in self.substring_list:
                        f.write(f"{palabra}\n")
                    
                    f.write("\n==== Prefijos ====\n")
                    for palabra in self.prefix_list:
                        f.write(f"{palabra}\n")
                    
                    f.write("\n==== Sufijos ====\n")
                    for palabra in self.suffix_list:
                        f.write(f"{palabra}\n")

            else:
                print("❌ Operación cancelada")

        except Exception as ex:
            print(f"❌ Error al guardar: {ex}")