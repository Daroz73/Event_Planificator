import flet as ft
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(ROOT)

from core.domain import Domain

class Delete_Utils:
    # metodo para remover elementos
    @staticmethod 
    def remove_item_grafic(page:ft.Page, dom:Domain, kind:str, id:str, row:ft.Row):
        dom.mark_for_delete(kind, id)
        page.controls.remove(row)
        page.update()
