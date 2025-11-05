#terminado
import flet as ft
from router import handle_route_change

def main(page: ft.Page):
    page.on_route_change = handle_route_change
    page.go(page.route)

ft.app(target=main)