import flet as ft

def main(page : ft.Page):
    page.title = "Event Gestor"
    page.window_width = 400
    page.window_height = 300
    # page.theme_mode = ft.ThemeMode.LIGHT

    # Codigo para la barra de navegacion
    page.appbar = ft.AppBar(
        bgcolor=ft.Colors.GREY_700,
        actions=[
            ft.PopupMenuButton(content=ft.Text("Resources"),
                               items=[
                                   ft.PopupMenuItem(text="See Resources"),
                                   ft.PopupMenuItem(text="Add Resource"),
                                   ft.PopupMenuItem(text="Delete Resource")
                               ]),
            ft.PopupMenuButton(content=ft.Text("Personal"),
                               items=[
                                   ft.PopupMenuItem(text="See Personal"),
                                   ft.PopupMenuItem(text="Add a Parson"),
                                   ft.PopupMenuItem(text="Delete a Person")
                               ]),
            ft.PopupMenuButton(content=ft.Text("Event"),
                             items = [
                                 ft.PopupMenuItem(text="New Event"),
                                 ft.PopupMenuItem(text="List Event"),
                                 ft.PopupMenuItem(text="Delete Event")
                             ]),
            ft.PopupMenuButton(icon=ft.Icons.MENU,
                               items=[
                                #    ft.PopupMenuItem(),#Separador
                                   ft.PopupMenuItem(text="Exit", on_click=lambda e:
                                                    page.window.destroy())
                               ]),
        ],
    )
    page.add(

    )

ft.app(target=main)