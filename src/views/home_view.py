import flet as ft

class Home_view:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Teoria de la computacion - Kevin Jesus Vazquez Sandria"
        self.page.theme_mode = ft.ThemeMode.DARK
    def build(self) -> ft.View:
        return ft.View(
            route="/",
            controls=[
                ft.Container(
                    content=ft.Column(
                        width=True,
                        controls=[
                            ft.Text(
                                "Automatas Finitos",
                                size=32,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Divider(height=40, color=ft.Colors.TRANSPARENT),

                            ft.ElevatedButton(
                                "Definir/Editar/Visualizar AFD",
                                icon=ft.Icons.BUILD_OUTLINED,
                                on_click=lambda _: self.page.go("/definir_afd"),
                                expand=True,
                                style=ft.ButtonStyle(
                                    padding=20,
                                    bgcolor=ft.Colors.GREY_700,
                                    color=ft.Colors.WHITE,
                                    overlay_color=ft.Colors.GREY_900,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    elevation={"pressed": 2, "hovered": 8, "focused": 4},
                                ),
                            ),

                            ft.ElevatedButton(
                                "Simular AFD",
                                icon=ft.Icons.PLAY_ARROW,
                                on_click=lambda _: self.page.go("/simulacion_afd"),
                                expand=True,
                                style=ft.ButtonStyle(
                                    padding=20,
                                    bgcolor=ft.Colors.ORANGE,
                                    color=ft.Colors.WHITE,
                                    overlay_color=ft.Colors.ORANGE_900,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    elevation={"pressed": 2, "hovered": 8, "focused": 4},
                                ),
                            ),

                            ft.ElevatedButton(
                                "Calcular Subcadenas",
                                icon=ft.Icons.TEXT_FIELDS,
                                on_click=lambda _: self.page.go("/calcular_subcadenas"),
                                expand=True,
                                style=ft.ButtonStyle(
                                    padding=20,
                                    bgcolor=ft.Colors.RED,
                                    color=ft.Colors.WHITE,
                                    overlay_color=ft.Colors.RED_900,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    elevation={"pressed": 2, "hovered": 8, "focused": 4},
                                ),
                            ),

                            ft.ElevatedButton(
                                "Calcular Cerraduras",
                                icon=ft.Icons.FUNCTIONS,
                                on_click=lambda _: self.page.go("/calcular_cerraduras"),
                                expand=True,
                                style=ft.ButtonStyle(
                                    padding=20,
                                    bgcolor=ft.Colors.RED,
                                    color=ft.Colors.WHITE,
                                    overlay_color=ft.Colors.RED_900,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    elevation={"pressed": 2, "hovered": 8, "focused": 4},
                                ),
                            ),

                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    width=600,
                    padding=50,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )