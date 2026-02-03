import flet as ft
from dataclasses import dataclass
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(ROOT)
from flet import Row, Column
from core.domain import Domain
from delete_utils import Delete_Utils
from core.worker import Worker
from core.resource import Resource
from creation_validate import Creation_Validate

class Visual_Utils:

    @staticmethod
    def show(page: ft.Page, kind: str, navegation_bar, domain: Domain):
        if kind.lower() == "event":
            Visual_Utils._show_events(page, navegation_bar, domain)
        else:
            Visual_Utils._show_resources(page, kind, navegation_bar, domain)

    # =====================================================================
    @staticmethod
    def _show_events(page: ft.Page, navegation_bar, dom:Domain):
        page.clean()
        page.add(navegation_bar)

        dom.rebuild_relations()
        events = dom.list_("events")

        if len(events) == 0:
            page.add(ft.Text("No hay eventos registrados", color=ft.Colors.RED))
            return

        save_btn = ft.ElevatedButton(
            text = "Save",
            visible=False,
            icon=ft.Icon(ft.Icons.SAVE),
            on_click=lambda e: (
                Visual_Utils.save_deletions(page,dom),
                Visual_Utils.visible_btn(page, dom.event_to_delete, save_btn)
            )
        )

        for e in events:
            event_id = ft.Text(f"Event ID: {e.id}")
            event_name = ft.Text(f"Event Name: {e.name}")
            event_begin = ft.Text(f"Begin: {e.begin}")
            event_end = ft.Text(f"End: {e.end}")
            view_details_option = ft.MenuItemButton(
                content=ft.Text("View Details"),
                on_click=lambda e, e_id=e.id: Visual_Utils.show_event_details(page,e_id)
                )
            delete_option = ft.MenuItemButton(
                content=ft.Text("Delete Event"),
                on_click=lambda e, e_id=e.id: (
                    Delete_Utils.remove_item_grafic(page, dom, "e", e_id, event_row),
                    Visual_Utils.visible_btn(page, dom.event_to_delete, save_btn)
                )
            )
            event_row = Row([
                event_id,
                event_name,
                event_begin,
                event_end,
                ft.SubmenuButton(
                    leading=ft.Icon(ft.Icons.MORE_VERT),
                    controls=[
                        view_details_option,
                        delete_option
                    ]
                )
            ])
            page.add(event_row)
        page.add(save_btn)

    # =====================================================================
    @staticmethod
    def _show_resources(page: ft.Page, kind: str, navegation_bar, dom:Domain):
        page.clean()
        page.add(navegation_bar)

        dom.rebuild_relations()

        if kind.lower() == "worker":
            items = dom.list_("worker")
        else:
            items = dom.list_("resource")

        if len(items) == 0:
            page.add(ft.Text("No hay elementos para mostrar", color=ft.Colors.RED))
            return

        save_btn = ft.ElevatedButton(
            text = "Save",
            visible=False,
            icon=ft.Icon(ft.Icons.SAVE),
            on_click=lambda e: (
                Visual_Utils.save_deletions(page, dom),
                Visual_Utils.visible_btn(page, dom.worker_to_delete if kind.lower() == "worker" else dom.resource_to_delete, save_btn)
            )
        )

        for l in items:
            if kind.lower() == "worker":
                row = Row([])
                worker_id = ft.Text(f"id: {l.id}")
                worker_name = ft.Text(f"name: {l.name}")
                worker_co_requested = ft.Text(f"co_requested: {l.co_requested}")
                worker_specialty = ft.Text(f"specialty: {l.specialty}")
                worker_view_use_plan = ft.MenuItemButton(
                    content=ft.Text("View Use Plan"),
                    on_click=lambda e, wid=l.id: Visual_Utils.show_use_plan(page, wid, kind)
                )
                worker_delete_option = ft.MenuItemButton(
                    content=ft.Text("Delete Worker"),
                    on_click=lambda e, wid=l.id, row_copy=row: (
                        Delete_Utils.remove_item_grafic(page, dom, "w", wid, row_copy),
                        Visual_Utils.visible_btn(page, dom.worker_to_delete, save_btn)
                    )
                )
                row.controls = [
                    worker_id,
                    worker_name,
                    worker_co_requested,
                    worker_specialty,
                    ft.SubmenuButton(
                        leading=ft.Icon(ft.Icons.MORE_VERT),
                        controls=[
                            worker_view_use_plan,
                            worker_delete_option
                        ])
                ]
                page.add(row)
            else:
                row = Row([])
                resource_id = ft.Text(f"id: {l.id}")
                resource_name = ft.Text(f"name: {l.name}")
                resource_co_requested = ft.Text(f"co_requested: {l.co_requested}")
                resource_view_use_plan = ft.MenuItemButton(
                    content=ft.Text("View Use Plan"),
                    on_click=lambda e, rid=l.id: Visual_Utils.show_use_plan(page, rid, kind)
                )
                resource_delete_option = ft.MenuItemButton(
                    content=ft.Text("Delete Resource"),
                    on_click=lambda e, rid=l.id, row_copy=row: (
                        Delete_Utils.remove_item_grafic(page, dom, "r", rid, row_copy),
                        Visual_Utils.visible_btn(page, dom.resource_to_delete, save_btn)
                    )
                )
                row.controls = [
                    resource_id,
                    resource_name,
                    resource_co_requested,
                    ft.SubmenuButton(
                        leading=ft.Icon(ft.Icons.MORE_VERT),
                        controls=[
                            resource_view_use_plan,
                            resource_delete_option
                        ])
                ]
                page.add(row)
        page.add(save_btn)
        
# ===========================================================================================================
    # funcion estatica para mostrar el plan de uso de un recurso que es una de las opciones que te da el menu desplegable de los 3 puntos
    @staticmethod
    def show_use_plan(page:ft.Page, id:str, kind:str):
        dom = Domain()
        dom.rebuild_relations()
        item = dom.get_item(kind, id)
        navegation_bar = page.controls[0]
        page.clean()
        page.add(navegation_bar)
        column_use_plan = ft.Column(scroll=ft.ScrollMode.AUTO)
        for e in item.use_plan:
            event_id = ft.Text(f"ID: {e.id}")
            event_name = ft.Text(f"Name: {e.name}")
            event_begin = ft.Text(f"Begin: {e.begin}")
            event_end = ft.Text(f"End: {e.end}")
            view_details_option = ft.MenuItemButton(
                content=ft.Text("View Details")
            )
            row = ft.Row([
                event_id,
                event_name,
                event_begin,
                event_end,
                ft.SubmenuButton(
                    leading=ft.Icon(ft.Icons.MORE_VERT),
                    controls=[
                        view_details_option
                    ])
            ])
            column_use_plan.controls.append(row)
        page.add(column_use_plan)
# ========================================================================================================
    # metodo para mostrar los detalles de un evento
    @staticmethod
    def show_event_details(page:ft.Page, id:str):
        navegation_bar = page.controls[0]
        page.clean()
        page.add(navegation_bar)
        dom = Domain()
        dom.rebuild_relations()
        event_col = ft.Column([])
        event = dom.get_item("e", id)
        event_id = ft.Text(f"Id: {event.id}")
        event_name = ft.Text(f"Name: {event.name}")
        event_specialist_in_charge = ft.Text(f"Specialist in Charge: {event.specialist_in_charge}")
        event_begin = ft.Text(f"Begin: {event.begin}")
        event_end = ft.Text(f"End: {event.end}")
        event_emergency = ft.Text(f"Emergency: {event.is_emergency}")
        event_workers_column = ft.Column([], scroll=ft.ScrollMode.AUTO)
        event_resources_column = ft.Column([], scroll=ft.ScrollMode.AUTO)
        for w in event.workers:
            w_item = Visual_Utils._get_visual_resource(w)
            event_workers_column.controls.append(w_item)
        for r in event.resources:
            r_item = Visual_Utils._get_visual_resource(r)
            event_resources_column.controls.append(r_item)
        event_row = ft.Row([
            event_id,
            event_name,
            event_specialist_in_charge,
            event_begin,
            event_end,
            event_emergency
        ])
        event_col.controls = [
            event_row,
            event_workers_column,
            event_resources_column
        ]
        page.add(event_col)
    # =========================================================
    def _get_visual_resource(item: Worker | Resource):
        item_row = ft.Row([])
        if isinstance(item, Worker):
            worker_id = ft.Text(f"Id: {item.id}")
            worker_name = ft.Text(f"Name: {item.name}")
            worker_co_requested = ft.Text(f"Co Requested: {item.co_requested}")
            worker_specialty = ft.Text(f"Specialty: {item.specialty}")
            item_row.controls = [
                worker_id,
                worker_name,
                worker_co_requested,
                worker_specialty
            ]
        elif isinstance(item, Resource):
            resource_id = ft.Text(f"Id: {item.id}")
            resource_name = ft.Text(f"Name: {item.name}")
            resource_co_requested = ft.Text(f"Co Requested: {item.co_requested}")
            item_row.controls = [
                resource_id,
                resource_name,
                resource_co_requested,
            ]
        return item_row
    # =========================================================
    # metodo para guardar los cambios de los elementos borrados
    def save_deletions(page:ft.Page, dom:Domain):
        if len(dom.event_to_delete) > 0:
            for e_id in set(dom.event_to_delete):
                dom.remove_item("e", e_id)
        if len(dom.worker_to_delete) > 0:
            for w_id in set(dom.worker_to_delete):
                dom.remove_item("w", w_id)
        if len(dom.resource_to_delete) > 0:
            for r_id in set(dom.resource_to_delete):
                dom.remove_item("r", r_id)
        dlg = Creation_Validate._create_dialog(page, "Save", "Deletions saved successfully")
        dlg.open = True
        page.add(dlg)
        page.update()
    # ====================================================================================================
    @staticmethod
    def on_click_save(page:ft.Page, dom:Domain, item_list:list, btn:ft.ElevatedButton):
        dom.save_pending()
        Visual_Utils.visible_btn(page, item_list, btn)
        page.update()
    # funcion para controlar la visibilidad de los botones================================================
    @staticmethod
    def visible_btn(page: ft.Page, item_list:list, btn:ft.ElevatedButton):
        if len(item_list) > 0:
            btn.visible = True
        else:
            btn.visible = False
        page.update()