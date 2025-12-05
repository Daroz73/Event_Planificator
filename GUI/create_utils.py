import flet as ft
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from creation_validate import Creation_Validate
from core.domain import Domain
from core.events import Event
from core.worker import Worker
from core.resource import Resource

class Create_Utils:
    @staticmethod
    def create_event(page: ft.Page, navegation_bar):
        page.clean()
        page.add(navegation_bar)

        # Campos principales
        event_name = ft.TextField(
            label="Event Name", 
        )

        specialist_in_charge = ft.TextField(label="Specialist in Charge")

        b_y = ft.TextField(label="Year: ", expand=1)
        b_m = ft.TextField(label="Month: ", expand=1)
        b_d = ft.TextField(label="Day: ", expand=1)
        b_h = ft.TextField(label="Hours: ", expand=1)
        b_min = ft.TextField(label="Minutes: ", expand=1)
        b_sec = ft.TextField(label="Seconds: ", expand=1)

        begin = ft.Row([
            b_y,
            b_m,
            b_d,
            b_h,
            b_min,
            b_sec
        ],
        expand=True
        )

        e_y = ft.TextField(label="Year: ", expand=1)
        e_m = ft.TextField(label="Month: ", expand=1)
        e_d = ft.TextField(label="Day: ", expand=1)
        e_h = ft.TextField(label="Hours: ", expand=1)
        e_min = ft.TextField(label="Minutes: ", expand=1)
        e_sec = ft.TextField(label="Seconds: ", expand=1)

        end = ft.Row([
            e_y,
            e_m,
            e_d,
            e_h,
            e_min,
            e_sec
        ],
        expand=True
        )

        specialist = ft.TextField(label="Specialists: ")
        count = ft.TextField(label="Count: ")
        btn_add_specialist = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=lambda e: Create_Utils._agg_row(page, column, "Specialist: "))

        resource = ft.TextField(label="Resource: ")
        r_count = ft.TextField(label="Count: ")
        btn_add_resource = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=lambda e: Create_Utils._agg_row(page, column, "Resource: "))

        is_emergency = ft.Checkbox(label="Is Emergency?")

        column = ft.Column([
            event_name,
            specialist_in_charge,
            ft.Text("Begin Date: "),
            begin,
            ft.Text("End Date: "),
            end,
            ft.Text("Ask the personal requested: "),
            ft.Row([
                specialist,
                count,
                btn_add_specialist
            ]),
            ft.Text("Resources requested: "),
            ft.Row([
                resource,
                r_count,
                btn_add_resource
            ]),
            is_emergency,
            ft.ElevatedButton("Create Event",
                              on_click=lambda e: Create_Utils._create_event(page, event_name.value, specialist_in_charge.value, b_y.value, b_m.value, b_d.value, b_h.value, b_min.value, b_sec.value, e_y.value, e_m.value, e_d.value, e_h.value, e_min.value, e_sec.value, is_emergency.value,[],[])
            )
        ])

        page.add(column)
# ===========================================================================================================
    @staticmethod
    def add_worker(page: ft.Page, navegation_bar):
        page.clean()
        page.add(navegation_bar)

        # Campos principales
        worker_name = ft.TextField(
            label="Worker Name", 
        )

        worker_co_requested = ft.TextField(label="Co-requested")

        worker_role = ft.TextField(label="Specialist")

        column = ft.Column([
            worker_name,
            worker_co_requested,
            worker_role,
            ft.ElevatedButton("Add Worker",
                              on_click=lambda e: Create_Utils._create_worker(page, worker_name.value, worker_co_requested.value, worker_role.value))
        ])

        page.add(column)
# ===========================================================================================================
    @staticmethod
    def add_resource(page: ft.Page, navegation_bar):
        page.clean()
        page.add(navegation_bar)

        # Campos principales
        resource_name = ft.TextField(
            label="Resource Name", 
        )

        resource_co_requested = ft.TextField(label="Co-requested")

        column = ft.Column([
            resource_name,
            resource_co_requested,
            ft.ElevatedButton("Add Resource",
                              on_click = lambda e: Create_Utils._create_resource(page, resource_name.value, resource_co_requested.value)
                              )
        ])
        page.add(column)
# == Metodos que desencadena el evento de crear event, worker o resource ==============================
    @staticmethod
    def _create_event(page: ft.Page, name, specialist_in_charge, b_y, b_m, b_d, b_h, b_min, b_sec, e_y, e_m, e_d, e_h, e_min, e_sec, is_emergency, personal_requested, resources_requested):
        dom = Domain()
        id = dom.ids_generator("e")
        begin_date = Creation_Validate.validate_date(page, b_y, b_m, b_d, b_h, b_min, b_sec)
        end_date = Creation_Validate.validate_date(page, e_y, e_m, e_d, e_h, e_min, e_sec)
        event = Event(id, name, specialist_in_charge, begin_date, end_date, is_emergency, personal_requested, resources_requested)
        print(event)
    # ==========
    @staticmethod
    def _create_worker(page:ft.Page, name:str, co_requested:str, speciality: str):
        dom = Domain()
        id = dom.ids_generator("w")
        worker = Worker(id, name, co_requested,[], speciality)
        dom.add(worker)
        Creation_Validate.validate_action(page, "Added Worker", "The worker had added succefully")
    # ============
    @staticmethod
    def _create_resource(page:ft.Page, name:str, co_requested:str):
        dom = Domain()
        id = dom.ids_generator("r")
        resource = Resource(id, name, co_requested, [])
        dom.add(resource)
        Creation_Validate.validate_action(page, "Added Resource", "The resources had added succefully")
    # ==============================================
    @staticmethod
    def _agg_row(page: ft.Page, column: ft.Column, label_value: str):
        first_item = ft.TextField(label=label_value)
        second_item = ft.TextField(label="Count: ")
        new_row = ft.Row([
            first_item,
            second_item,
            ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=lambda e: Create_Utils._agg_row(page, column, label_value)),
            ft.FloatingActionButton(icon=ft.Icons.REMOVE)
        ])
        column.controls.insert(-4, new_row)
        page.update()