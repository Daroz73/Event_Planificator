import flet as ft
from flet import Row
import sys, os
# Importar core
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)
# Importar utilidades externas
from visual_utils import Visual_Utils
from create_utils import Create_Utils


def main(page: ft.Page):
    page.title = "Event Planificator"

    navegation_bar = ft.AppBar(
        leading=ft.Icon(ft.Icons.BUSINESS),
        leading_width=50,
        title=ft.Text("Event Planificator"),
        center_title=False,
        bgcolor=ft.Colors.BLUE_900,
        actions=[
            ft.SubmenuButton(
                content=ft.Text("Events"),
                controls=[
                    # Usa el método externo Create_Utils
                    ft.MenuItemButton(
                        content=ft.Text("Create Event"),
                        on_click=lambda e: Create_Utils.create_event(page, navegation_bar)
                    ),
                    # Usa el método externo Visual_Utils
                    ft.MenuItemButton(
                        content=ft.Text("View Events"),
                        on_click=lambda e: Visual_Utils.show(page, "event", navegation_bar)
                    )
                ]
            ),
            ft.SubmenuButton(
                content=ft.Text("Workers"),
                controls=[
                    ft.MenuItemButton(content=ft.Text("Add Worker")),
                    ft.MenuItemButton(
                        content=ft.Text("View Worker"),
                        on_click=lambda e: Visual_Utils.show(page, "worker", navegation_bar)
                    )
                ]
            ),
            ft.SubmenuButton(
                content=ft.Text("Resources"),
                controls=[
                    ft.MenuItemButton(content=ft.Text("By Resource")),
                    ft.MenuItemButton(
                        content=ft.Text("View Resources"),
                        on_click=lambda e: Visual_Utils.show(page, "resource", navegation_bar)
                    )
                ]
            ),
        ]
    )
    page.add(navegation_bar)

ft.app(main)
