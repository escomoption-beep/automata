import flet as ft

class TablaTransiciones:
    def __init__(self, estados: list, alfabeto: list, transiciones: dict = None):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones or {}
    
    def create_dicc_trans(self):
        """Crea una plantilla para el diccionario de transiciones."""
        self.transiciones.clear()
        self.transiciones.update({
            estado: {simbolo: [] for simbolo in self.alfabeto}
            for estado in self.estados
        })
    
    def actualizar_transicion(self, estado, simbolo, e):
        """Actualiza la transición δ(estado, símbolo)."""
        texto = e.control.value.strip()
        destinos = []
        if texto != "":
            destinos = [t.strip() for t in texto.split(",") if t.strip()]
        self.transiciones[estado][simbolo] = destinos
        print(f"δ({estado}, {simbolo}) = {destinos}")
    
    def get_value(self, transicion):
        """Convierte la lista de estados destino a texto legible."""
        if not transicion:
            return ""
        return ",".join(transicion)
    
    def build(self) -> ft.Column:
        """Construye la tabla de transiciones con diseño personalizado."""
        if not self.transiciones:
            self.create_dicc_trans()
        
        # Encabezado
        header_row = ft.Row(
            [
                ft.Container(
                    content=ft.Text("Estado", weight="bold", size=14),
                    width=100,
                    padding=10,
                    bgcolor=ft.Colors.BLUE_GREY_100,
                    border=ft.border.all(1, ft.Colors.GREY_400)
                )
            ] + [
                ft.Container(
                    content=ft.Text(str(simbolo), weight="bold", size=14),
                    width=200,
                    padding=10,
                    bgcolor=ft.Colors.BLUE_GREY_100,
                    border=ft.border.all(1, ft.Colors.GREY_400)
                )
                for simbolo in self.alfabeto
            ],
            spacing=0
        )
        
        # Filas de datos
        data_rows = []
        for estado in self.estados:
            row_cells = [
                ft.Container(
                    content=ft.Text(estado, size=14),
                    width=100,
                    padding=10,
                    border=ft.border.all(1, ft.Colors.GREY_400),
                    bgcolor=ft.Colors.BLUE_GREY_50
                )
            ]
            
            for simbolo in self.alfabeto:
                tf = ft.TextField(
                    value=self.get_value(self.transiciones[estado][simbolo]),
                    text_size=13,
                    on_change=lambda e, est=estado, sim=simbolo: self.actualizar_transicion(est, sim, e),
                    border_color=ft.Colors.GREY_400,
                    focused_border_color=ft.Colors.BLUE_400
                )
                
                row_cells.append(
                    ft.Container(
                        content=tf,
                        width=200,
                        padding=5,
                        border=ft.border.all(1, ft.Colors.GREY_400)
                    )
                )
            
            data_rows.append(ft.Row(row_cells, spacing=0))
        
        # Tabla completa con scroll horizontal
        tabla = ft.Column(
            [header_row] + data_rows,
            spacing=0,
            scroll=ft.ScrollMode.AUTO
        )
        
        return ft.Container(
            content=tabla,
            border=ft.border.all(2, ft.Colors.GREY_400),
            border_radius=5
        )
    
    def obtener_transiciones(self) -> dict:
        """Retorna el diccionario de transiciones."""
        return self.transiciones

