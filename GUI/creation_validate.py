from dataclasses import dataclass
from datetime import datetime
import flet as ft

class Creation_Validate:
    # metodo que crea un dialog que indica que se realizo una accion con exito
    @staticmethod
    def validate_action(page:ft.Page, title: str, text: str):
        dialog = Creation_Validate._create_dialog(page, title, text)
        dialog.open = True
        page.add(dialog)
    @staticmethod
    def validate_date(page: ft.Page, year, month, day, hour, minute, seconds) -> datetime:
        try:
            year = int(year)
            month = int(month)
            day = int(day)
            hour = int(hour)
            minute = int(minute)
            seconds = int(seconds)
            return datetime(year, month, day, hour, minute, seconds)
        except Exception:
            dialog = Creation_Validate._create_dialog(page, "Invalid Date", "The arg are not valid")
            dialog.open = True
            page.add(dialog)
    # =====================================================================================
    @staticmethod
    def _create_dialog(page: ft.Page, title: str, content: str) -> ft.AlertDialog:
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.ElevatedButton("OK", on_click=lambda e: Creation_Validate._close_dialog(page, dlg))
            ]
        )
        return dlg
    # ======================================================================================
    @staticmethod
    def _close_dialog(page: ft.Page, dialog: ft.AlertDialog):  
        dialog.open = False
        page.update()
    # ======================================================================================
    # Metodo para simular un "menu inteligente" cuando se van a rellenar las especialidades 
    @staticmethod
    def filter_options(e, page:ft.Page, options:set[str], menu:ft.ListView):
        text = e.control.value.lower()
        menu.controls.clear()

        for s in options:
            if text in s.lower():
                menu.controls.append(
                    ft.ListTile(
                        title=ft.Text(s),
                        bgcolor=ft.Colors.BLUE_800,
                        on_click=lambda ev, val=s:
                            Creation_Validate.select_option(page, val, e.control, menu)
                    )
                )
        menu.visible = True
        page.update()
    # ======================================================================================
    # metodo para dar valor de la especialidad seleccionada
    @staticmethod
    def select_option(page:ft.Page, val:str, specialist_in_charge:ft.TextField, menu:ft.ListView):
        specialist_in_charge.value = val
        specialist_in_charge.border_color = None
        specialist_in_charge.tooltip = None
        
        Creation_Validate.hide_menu(page, menu)
    # ======================================================================================
    # metodo para mostrar el menu inteligente
    @staticmethod
    def show_menu(e, page:ft.Page, specialities:set[str], speciality_menu:ft.ListView):
        Creation_Validate.filter_options(e, page, specialities, speciality_menu)
    # ======================================================================================
    # metodo para validar si la especialidad introducida es correcta
    @staticmethod
    def validate_speciality(page:ft.Page, specialty:str ,specialities:set[str], control) -> bool:
        
        if specialty not in specialities:
            control.border_color = ft.Colors.RED
            # mensaje que se muestra al pasar el mouse por encima del campo
            control.tooltip = "Speciality not valid"
            page.update()
            return False
        else:
            control.border_color = None
            control.tooltip = None
        page.update()
        return True
    # =======================================================================================
    # metodo para oculrar el menu inteligente
    @staticmethod
    def hide_menu(page:ft.Page, speciality_menu:ft.ListView):
        speciality_menu.visible = False
        page.update()
    # ==========================================================================================