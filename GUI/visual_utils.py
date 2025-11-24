import flet as ft
from dataclasses import dataclass
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(ROOT)
from flet import Row, Column
from core.domain import Domain

class Visual_Utils:

    @staticmethod
    def show(page: ft.Page, kind: str, navegation_bar):
        """
        Método controlador que decide qué pantalla mostrar.
        """
        if kind.lower() == "event":
            Visual_Utils._show_events(page, navegation_bar)
        else:
            Visual_Utils._show_resources(page, kind, navegation_bar)

    # =====================================================================
    @staticmethod
    def _show_events(page: ft.Page, navegation_bar):
        """
        Muestra todos los eventos guardados.
        """
        page.clean()
        page.add(navegation_bar)

        dom = Domain()
        events = dom.list_("events")

        if len(events) == 0:
            page.add(ft.Text("No hay eventos registrados", color=ft.Colors.RED))
            return

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
            page.add(event_row)

    # =====================================================================
    @staticmethod
    def _show_resources(page: ft.Page, kind: str, navegation_bar):
        """
        Muestra la lista de workers o resources.
        """
        page.clean()
        page.add(navegation_bar)

        dom = Domain()

        if kind.lower() == "worker":
            items = dom.list_("worker")
        else:
            items = dom.list_("resource")

        if len(items) == 0:
            page.add(ft.Text("No hay elementos para mostrar", color=ft.Colors.RED))
            return

        for l in items:
            if kind.lower() == "worker":
                row = Row([
                    ft.Text(f"id: {l.id}"),
                    ft.Text(f"name: {l.name}"),
                    ft.Text(f"co_requested: {l.co_requested}"),
                    ft.Text(f"specialty: {l.specialty}"),
                    ft.SubmenuButton(leading=ft.Icon(ft.Icons.MORE_VERT))
                ])
            else:
                row = Row([
                    ft.Text(f"id: {l.id}"),
                    ft.Text(f"name: {l.name}"),
                    ft.Text(f"co_requested: {l.co_requested}"),
                    ft.SubmenuButton(leading=ft.Icon(ft.Icons.MORE_VERT))
                ])
            page.add(row)

    