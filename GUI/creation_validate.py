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
    @staticmethod
    def _close_dialog(page: ft.Page, dialog: ft.AlertDialog):  
        dialog.open = False
        page.update()