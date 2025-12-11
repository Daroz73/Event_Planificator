import flet as ft
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(ROOT)

from core.events import Event
from core.worker import Worker
from core.resource import Resource
from core.domain import Domain
from dataclasses import dataclass

class Delete_Utils:
    # metodo para remover elementos
    @staticmethod 
    def remove_item_grafic(page:ft.Page, type:str, id:str, row:ft.Row):
        dom = Domain()
        dom.remove_item(type, id)
        page.controls.remove(row)
        page.update()
