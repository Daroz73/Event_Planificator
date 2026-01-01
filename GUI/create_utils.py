import flet as ft
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from creation_validate import Creation_Validate
from core.domain import Domain
from core.events import Event
from core.worker import Worker
from core.resource import Resource
from core.events_planificator import Events_Planificator

class Create_Utils:
    @staticmethod
    def create_event(page: ft.Page, dom:Domain, navegation_bar):
        page.clean()
        page.add(navegation_bar)

        # Campos principales
        event_name = ft.TextField(
            label="Event Name", 
        )
        
        specialist_option = dom.get_specialities()
        specialist_menu = ft.ListView(
            controls=[],
            visible=False,
            height=150,
            spacing=0
        )
        specialist_in_charge = ft.TextField(
            label="Specialist in Charge",
            data = {"clicking_menu":False},
            on_change=lambda e: Creation_Validate.filter_options(e, page, specialist_option, specialist_menu),
            on_focus=lambda e: Creation_Validate.show_menu(e, page, specialist_option, specialist_menu),
            # on_blur=lambda e: Creation_Validate.hide_specialities_menu(page, specialist_menu) 
            )

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
        
        specialist_menu_personal_requested = ft.ListView(
            controls=[],
            visible=False,
            height=150,
            spacing=0
        )
        menu_specialist_personal_container = ft.Container(
            content=specialist_menu_personal_requested,
            width=250,
            height=150
        )
        personal_col = ft.Column([])
        specialist = ft.TextField(
            label="Specialists: ",
            on_change=lambda e: Creation_Validate.filter_options(e, page, specialist_option, specialist_menu_personal_requested),
            on_click=lambda e: Creation_Validate.show_menu(e, page, specialist_option, specialist_menu_personal_requested)
            # on_blur=lambda e:
            )
        count = ft.TextField(label="Count: ")
        btn_add_specialist = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=lambda e: Create_Utils._agg_row(page, personal_col, "Specialist: ", specialist_option)
            )
        personal_row = ft.Row([
                specialist,
                menu_specialist_personal_container,
                count,
                btn_add_specialist
            ])
        personal_col.controls.append(personal_row)

        resource_col = ft.Column([])
        resources_options = dom.get_resources()
        resources_menu = ft.ListView(
            controls=[],
            visible=False,
            height=150,
            spacing=0
        )
        resources_menu_cotainer = ft.Container(
            content=resources_menu,
            width=250,
            height=150
        )
        resource = ft.TextField(
            label="Resource: ",
            on_change=lambda e: Creation_Validate.filter_options(e, page, resources_options, resources_menu),
            on_focus=lambda e: Creation_Validate.show_menu(e, page, resources_options, resources_menu)
        )
        r_count = ft.TextField(label="Count: ")
        btn_add_resource = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=lambda e: Create_Utils._agg_row(page, resource_col, "Resource: ", resources_options)
            )
        resource_row = ft.Row([
                resource,
                resources_menu_cotainer,
                r_count,
                btn_add_resource
            ])
        resource_col.controls.append(resource_row)

        is_emergency = ft.Checkbox(label="Is Emergency?")

        column = ft.Column([
            event_name,
            specialist_in_charge,
            specialist_menu,
            ft.Text("Begin Date: "),
            begin,
            ft.Text("End Date: "),
            end,
            ft.Text("Ask the personal requested: "),
            personal_col,
            ft.Text("Resources requested: "),
            resource_col,
            is_emergency,
            ft.ElevatedButton("Create Event",
                              on_click=lambda e, ctr=specialist_in_charge: Create_Utils._create_event(page, ctr, dom, event_name.value, specialist_in_charge.value, b_y.value, b_m.value, b_d.value, b_h.value, b_min.value, b_sec.value, e_y.value, e_m.value, e_d.value, e_h.value, e_min.value, e_sec.value, is_emergency.value,Create_Utils._get_values_from_column(personal_col),Create_Utils._get_values_from_column(resource_col))
            )
        ],
            scroll="auto",
            expand=True)

        page.add(column)
# ===========================================================================================================
    @staticmethod
    def add_worker(page: ft.Page, dom:Domain, navegation_bar):
        page.clean()
        page.add(navegation_bar)

        # Campos principales
        worker_name = ft.TextField(
            label="Worker Name", 
        )

        worker_co_requested_options = dom.get_resources()
        worker_co_requested_menu = ft.ListView(
            controls=[],
            visible=False,
            height=150,
            spacing=0
        )
        worker_co_requested = ft.TextField(
            label="Co-requested",
            on_change=lambda e: Creation_Validate.filter_options(e, page, worker_co_requested_options, worker_co_requested_menu),
            on_focus=lambda e: Creation_Validate.show_menu(e, page, worker_co_requested_options, worker_co_requested_menu)
        )
        
        worker_specialities = dom.get_specialities()
        worker_menu_itelligent = ft.ListView(
            controls=[],
            visible=False,
            height=150,
            spacing=0
        )
        worker_role = ft.TextField(
            label="Specialist",
            on_change=lambda e: Creation_Validate.filter_options(e, page, worker_specialities, worker_menu_itelligent),
            on_focus=lambda e: Creation_Validate.show_menu(e, page, worker_specialities, worker_menu_itelligent),
            # on_blur=lambda e: Creation_Validate.hide_specialities_menu(page, worker_menu_itelligent)
        )

        column = ft.Column([
            worker_name,
            worker_co_requested,
            worker_co_requested_menu,
            worker_role,
            worker_menu_itelligent,
            ft.ElevatedButton("Add Worker",
                              on_click=lambda e: Create_Utils._create_worker(page, worker_name.value, worker_co_requested.value, worker_role.value))
        ])

        page.add(column)
# ===========================================================================================================
    @staticmethod
    def add_resource(page: ft.Page, dom:Domain, navegation_bar):
        page.clean()
        page.add(navegation_bar)

        # Campos principales
        resources_names_options = dom.get_resources()
        resopurces_names_menu = ft.ListView(
            controls=[],
            visible=False,
            height=150,
            spacing=0
        )
        resource_name = ft.TextField(
            label="Resource Name",
            on_change=lambda e: Creation_Validate.filter_options(e, page, resources_names_options, resopurces_names_menu),
            on_focus=lambda e: Creation_Validate.show_menu(e, page, resources_names_options, resopurces_names_menu) 
        )

        co_requested_option = dom.get_specialities()
        co_requested_menu = ft.ListView(
            controls=[],
            visible=False,
            height=150,
            spacing=0
        )
        resource_co_requested = ft.TextField(
            label="Co-requested",
            on_change=lambda e: Creation_Validate.filter_options(e, page, co_requested_option, co_requested_menu),
            on_focus=lambda e: Creation_Validate.show_menu(e, page, co_requested_option, co_requested_menu)    
        )

        column = ft.Column([
            resource_name,
            resopurces_names_menu,
            resource_co_requested,
            co_requested_menu,
            ft.ElevatedButton("Add Resource",
                              on_click = lambda e: Create_Utils._create_resource(page, resource_name.value, resource_co_requested.value)
                              )
        ])
        page.add(column)
# == Metodos que desencadena el evento de crear event, worker o resource ==============================
    @staticmethod
    def _create_event(page: ft.Page, ctr, dom:Domain, name, specialist_in_charge, b_y, b_m, b_d, b_h, b_min, b_sec, e_y, e_m, e_d, e_h, e_min, e_sec, is_emergency, personal_requested, resources_requested):
        if not Creation_Validate.validate_speciality(page, specialist_in_charge, dom.get_specialities(), ctr):
            return
        begin_date = Creation_Validate.validate_date(page, b_y, b_m, b_d, b_h, b_min, b_sec)
        end_date = Creation_Validate.validate_date(page, e_y, e_m, e_d, e_h, e_min, e_sec)
        id = dom.ids_generator("e")
        event = Event(id, name, personal_requested, resources_requested, specialist_in_charge, begin_date, end_date, is_emergency, [], [])
        dom.rebuild_relations()
        dom.add(event)
    # =====================================================================================
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
    def _agg_row(page: ft.Page, column: ft.Column, label_value: str, speciality_option:set[str]):
        menu = ft.ListView(
            controls=[],
            visible=False,
            height=150,
            spacing=0
        )
        menu_container = ft.Container(
            content=menu,
            width=250,
            height=150
        )
        new_row = ft.Row([])
    
        first_item = ft.TextField(
            label=label_value,
            data={"menu":menu},
            on_change=lambda e: Creation_Validate.filter_options(e, page, speciality_option, e.control.data["menu"]),
            on_focus=lambda e: Creation_Validate.show_menu(e, page, speciality_option, e.control.data["menu"])
        )
        second_item = ft.TextField(label="Count: ")
        new_row.controls = [
            first_item,
            menu_container,
            second_item,
            ft.FloatingActionButton(
                icon=ft.Icons.ADD, 
                on_click=lambda e: Create_Utils._agg_row(page, column, label_value, speciality_option)
                ),
            ft.FloatingActionButton(
                icon=ft.Icons.REMOVE,
                on_click=lambda e: Create_Utils._remove_row(page, column, new_row)
                )
        ]
        column.controls.insert(1,new_row)
        page.update()
    # =============================================
    @staticmethod
    def _remove_row(page: ft.Page, column: ft.Column, row: ft.Row):
        column.controls.remove(row)
        page.update()
    # =============================================
    @staticmethod
    def _get_values_from_column(column: ft.Column) -> dict:
        extracted_dict = {}
        for row in column.controls:
            if isinstance(row, ft.Row):
                values = []
                for control in row.controls:
                    if isinstance(control, ft.TextField):
                        values.append(control.value)
                if len(values) == 2:
                    key = values[0]
                    try:
                        value = int(values[1])
                    except ValueError:
                        value = 0
                    extracted_dict[key] = value
        return extracted_dict