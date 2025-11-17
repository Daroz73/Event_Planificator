import flet as ft
from flet import Row
from datetime import datetime
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(ROOT)
from core.domain import Domain


def main(page: ft.Page):
    page.title = "Event Planificator"
# =============================================================================================================
    # funcion para mostrar los eventos en la interface
    def show_events(e):
        page.clean()
        page.add(navegation_bar)
        dom = Domain()
        events = dom.list_events()
        event_rows = []
        for e in events:
            event_row = Row([
                ft.Text(f"Event ID: {e.id}"),
                ft.Text(f"Event Name: {e.name}"),
                ft.Text(f"Begin: {e.begin}"),
                ft.Text(f"End: {e.end}"),
                ft.SubmenuButton(
                    leading=ft.Icon(ft.Icons.MORE_VERT),
                    controls=[
                        ft.MenuItemButton(content=ft.Text("View Details")),
                        ft.MenuItemButton(content=ft.Text("Delete Event"))
                    ]
                )
            ])
            event_rows.append(event_row)
        for er in event_rows:
            page.add(er)
    # ========================================================================================================
    # funcion para crear un nuevo evento
    def create_event(e):
        page.clean()
        page.add(navegation_bar)
        event_name = ft.TextField(label="Event Name", color=ft.Colors.BLACK, border_color=ft.Colors.BLACK, bgcolor=ft.Colors.WHITE)
        specialist_in_charge = ft.TextField(label="Specialist in Charge")
        begin = ft.Row([
            ft.TextField(label="Year: "),
            ft.TextField(label="Month: "),
            ft.TextField(label="Day: ")
        ])
        end = ft.Row([
            ft.TextField(label="Year: "),
            ft.TextField(label="Month: "),
            ft.TextField(label="Day: ")
        ])
        column = ft.Column([
            event_name,
            specialist_in_charge,
            begin,
            end,
            ft.Text("Ask the personal requested: "),
            ft.Row([
                ft.TextField(label="Specialists: "),
                ft.TextField(label="Count: "),
                ft.FloatingActionButton(icon=ft.Icons.ADD)
            ]),
            ft.Text("Resources requested: "),
            ft.Row([
                ft.TextField(label="Resource: "),
                ft.TextField(label="Count: "),
                ft.FloatingActionButton(icon=ft.Icons.ADD)
            ]),
            ft.Checkbox(label="Is Emergency"),
            ft.ElevatedButton("Create Event")
        ])
        page.add(column)
# ==========================================================================================================

    navegation_bar = ft.AppBar(
        leading=ft.Icon(ft.Icons.BUSINESS),
        leading_width=50,
        title=ft.Text("Navegation Bar"),
        center_title=False,
        bgcolor=ft.Colors.BLUE_900,
        actions=[
            ft.SubmenuButton(
                content=ft.Text("Events"),
                controls=[
                    ft.MenuItemButton(content=ft.Text("Create Event"), on_click=create_event),
                    ft.MenuItemButton(content=ft.Text("View Events"), on_click=show_events),
                ]
            ),
            ft.SubmenuButton(
                content=ft.Text("Workers"),
                controls=[
                    ft.MenuItemButton(content=ft.Text("Add Worker")),
                    ft.MenuItemButton(content=ft.Text("View Worker"))
                ]
            ),
            ft.SubmenuButton(
                content=ft.Text("Resources"),
                controls=[
                    ft.MenuItemButton(content=ft.Text("By Resource")),
                    ft.MenuItemButton(content=ft.Text("View Resources"))
                ]
            ),
        ]                       
                               )
    page.add(navegation_bar)

ft.app(main)