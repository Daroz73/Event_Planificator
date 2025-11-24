import flet as ft
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

class Create_Utils:
    @staticmethod
    def create_event(page: ft.Page, navegation_bar):
        """
        Interfaz completa para crear un nuevo evento.
        """

        page.clean()
        page.add(navegation_bar)

        # Campos principales
        event_name = ft.TextField(
            label="Event Name", 
            color=ft.Colors.BLACK, 
            border_color=ft.Colors.BLACK, 
            bgcolor=ft.Colors.WHITE
        )

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
