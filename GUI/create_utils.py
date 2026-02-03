import flet as ft
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from creation_validate import Creation_Validate
from visual_utils import Visual_Utils
from core.domain import Domain
from core.events import Event
from core.worker import Worker
from core.resource import Resource
from datetime import timedelta

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

        months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre"
                  ,"Noviembre", "Diciembre"]
        hours = [f"{i:02d}" for i in range(24)]
        minutes = [f"{i:02d}" for i in range(60)]

        b_y = ft.TextField(label="Year: ", width=90)
        b_m = ft.Dropdown(label="Month: ", options=[ft.dropdown.Option(m) for m in months], width=150)
        b_d = ft.TextField(label="Day: ", width=70)
        b_h = ft.Dropdown(label="Hours: ", options=[ft.dropdown.Option(h) for h in hours], width=150)
        b_min = ft.Dropdown(label="Minutes: ", options=[ft.dropdown.Option(m) for m in minutes], width=150)

        begin = ft.Row([
            b_y,b_m,b_d,
            ft.Text("-"),
            b_h,b_min
        ],
        expand=True
        )

        e_y = ft.TextField(label="Year: ", width=90)
        e_m = ft.Dropdown(label="Month: ", options=[ft.dropdown.Option(m) for m in months])
        e_d = ft.TextField(label="Day: ", width=70)
        e_h = ft.Dropdown(label="Hours: ", options=[ft.dropdown.Option(h) for h in hours], width=150)
        e_min = ft.Dropdown(label="Minutes: ", options=[ft.dropdown.Option(m) for m in minutes], width=150)

        end = ft.Row([
            e_y,e_m,e_d,
            ft.Text("-"),
            e_h,e_min
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
        count = ft.Dropdown(
            label="Count: ",
            options=[ft.dropdown.Option(i) for i in range(1,51)],
            width=150
            )
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
        r_count = ft.Dropdown(
            label="Count: ",
            options=[ft.dropdown.Option(i) for i in range(1, 51)],
            width=150
            )
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

        duration_hours = ft.Dropdown(
            label="Duration (hours)",
            width=150,
            options=[ft.dropdown.Option(str(i)) for i in range(13)]
        )
        duration_minutes = ft.Dropdown(
            label="Duration (minutes)",
            width=150,
            options=[ft.dropdown.Option(str(i)) for i in range(60)]
        )
        duration_row = ft.Row(
            [
                duration_hours,
                duration_minutes
            ],
            spacing=20
        )
        btn_find_slot = ft.ElevatedButton(
            "Find Slot",
            icon = ft.Icons.SEARCH,
            on_click=lambda e: Create_Utils._find_avialable_slot(page=page, dom=dom, personal_col=personal_col
                                                                , resource_col=resource_col, duration_h=duration_hours.value
                                                                , duration_min=duration_minutes.value, b_y=b_y, b_m=b_m
                                                                , b_d=b_d, b_h=b_h, b_min=b_min, e_y=e_y, e_m=e_m, e_d=e_d
                                                                , e_h=e_h, e_min=e_min
                                                                )
        )


        is_emergency = ft.Checkbox(label="Is Emergency?")
        create_event_btn = ft.ElevatedButton("Create Event",
                              on_click=lambda e, ctr=specialist_in_charge: Create_Utils._create_event(page, 
                                                                        ctr, dom,event_name.value, 
                                                                        specialist_in_charge.value, b_y.value, 
                                                                        b_m.value, b_d.value, b_h.value, b_min.value, 
                                                                        e_y.value, e_m.value, e_d.value, e_h.value, 
                                                                        e_min.value, is_emergency.value,
                                                                        Create_Utils._get_values_from_column(personal_col),
                                                                        Create_Utils._get_values_from_column(resource_col),
                                                                        save_event_btn
                                                                    )
            )
        save_event_btn = ft.ElevatedButton(
            "Save",
            visible=False,
            on_click=lambda e: (Visual_Utils.on_click_save(page, dom, dom.pending_events, save_event_btn), 
                                Creation_Validate.validate_action(page,"Saved","Events saved successfully")
                                )
        )
        column = ft.Column([
            event_name,
            specialist_in_charge,
            specialist_menu,
            ft.Text("Begin Date: "),
            begin,
            ft.Text("End Date: "),
            end,
            ft.Text("Event Duration (for find a slot, opcional)"),
            duration_row,
            btn_find_slot,
            ft.Text("Ask the personal requested: "),
            personal_col,
            ft.Text("Resources requested: "),
            resource_col,
            is_emergency,
            create_event_btn,
            save_event_btn
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
        add_worker_btn = ft.ElevatedButton("Add Worker",
                              on_click=lambda e: Create_Utils._create_worker(page, dom, worker_name.value,
                                                                            worker_co_requested.value, 
                                                                            worker_role.value, worker_co_requested,
                                                                            worker_role,
                                                                            save_workers_bts
                                                                            )
                            )
        save_workers_bts = ft.ElevatedButton(
            "Save",
            visible=False,
            on_click=lambda e: (Visual_Utils.on_click_save(page, dom, dom.pending_workers, save_workers_bts), 
                    Creation_Validate.validate_action(page,"Saved","Workers saved successfully")
                    )
        )
        column = ft.Column([
            worker_name,
            worker_co_requested,
            worker_co_requested_menu,
            worker_role,
            worker_menu_itelligent,
            add_worker_btn,
            save_workers_bts
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
        add_resource_btn = ft.ElevatedButton("Add Resource",
                              on_click = lambda e: Create_Utils._create_resource(page, dom, resource_name.value, 
                                                                                resource_co_requested.value, 
                                                                                resource_name, resource_co_requested,
                                                                                save_resources_btn
                                                                                )
                            )
        save_resources_btn = ft.ElevatedButton(
            "Save",
            visible=False,
            on_click=lambda e: (Visual_Utils.on_click_save(page, dom, dom.pending_resources, save_resources_btn), 
                                Creation_Validate.validate_action(page,"Saved","Resource saved successfully")
                            )
        )
        column = ft.Column([
            resource_name,
            resopurces_names_menu,
            resource_co_requested,
            co_requested_menu,
            add_resource_btn,
            save_resources_btn
        ])
        page.add(column)
# == Metodos que desencadena el evento de crear event, worker o resource ==============================
    @staticmethod
    def _create_event(page: ft.Page, ctr, dom:Domain, 
                      name, specialist_in_charge, b_y, b_m, b_d, b_h, b_min, e_y, e_m, e_d, e_h, e_min, 
                      is_emergency, personal_requested:dict, resources_requested:dict, btn_save:ft.ElevatedButton):
        if not Creation_Validate.validate_(page, specialist_in_charge, dom.get_specialities(), ctr):
            return
        begin_date = Creation_Validate.validate_date(page, b_y, b_m, b_d, b_h, b_min, 0)
        end_date = Creation_Validate.validate_date(page, e_y, e_m, e_d, e_h, e_min, 0)
        if begin_date is None or end_date is None:
            return
        if begin_date >= end_date:
            Creation_Validate.validate_action(page, "Invalid Date Range", "The begin date must be before the end date")
            return
        data_workers = dom.get_count("w")
        for p, c in personal_requested.items():
            if p not in data_workers.keys() or c > data_workers[p]:
                Creation_Validate.validate_action(page, "Invalid personal", f"The personal '{p}' is not available in the required count")
                return
        data_resources = dom.get_count("r")
        for r, c in resources_requested.items():
            if r not in data_resources.keys() or c > data_resources[r]:
                Creation_Validate.validate_action(page, "Invalid resource", f"The resource '{r}' is not available in the required count")
                return
        id = dom.ids_generator("e")
        event = Event(id, name, personal_requested, resources_requested, specialist_in_charge, begin_date, end_date, is_emergency, [], [])
        # dom.rebuild_relations()
        dom.pending_events.append(event)
        Creation_Validate.validate_action(page, "Success", f"The event {name} has been added to the wait list.\n For saved it click the Save Button.")
        Visual_Utils.visible_btn(page, dom.pending_events, btn_save)
        page.update()
    # =======================================================================================================
    @staticmethod
    def _create_worker(page:ft.Page, dom: Domain, name:str, co_requested:str, speciality: str, 
                       co_requested_ctr:ft.TextField, speciality_ctr:ft.TextField, save_btn:ft.ElevatedButton):
        if not Creation_Validate.validate_(page, co_requested, dom.get_resources(), co_requested_ctr):
            return
        if not Creation_Validate.validate_(page, speciality, dom.get_specialities(), speciality_ctr):
            return
        if not "all" in dom.get_specialities_by_resource()[co_requested] and speciality not in dom.get_specialities_by_resource()[co_requested]:
            Creation_Validate.validate_action(page, "Invalid speciality", 
                                              f"The speciality '{speciality}' cannot use the resource '{co_requested}'")
            return
        id = dom.ids_generator("w")
        worker = Worker(id, name, co_requested,[], speciality)
        dom.add(worker)
        Visual_Utils.visible_btn(page, dom.pending_workers, save_btn)
        Creation_Validate.validate_action(page, "Added Worker", "The worker had added succefully")
    # =======================================================================================================
    @staticmethod
    def _create_resource(page:ft.Page, dom:Domain, name:str, co_requested:str, ctr_name:ft.TextField,
                        crt_co_requested:ft.TextField, save_btn:ft.ElevatedButton):
        if not Creation_Validate.validate_(page, name, dom.get_resources(), ctr_name):
            return
        if not Creation_Validate.validate_(page, co_requested, dom.get_specialities(), crt_co_requested):
            return
        if name not in dom.get_specialities_by_resource()[name]:
            Creation_Validate.validate_action(page, "Invalid speciality", 
                                              f"The speciality '{co_requested}' cannot use the resource '{name}'")
            return
        id = dom.ids_generator("r")
        resource = Resource(id, name, co_requested, [])
        dom.add(resource)
        Visual_Utils.visible_btn(page, dom.pending_resources, save_btn)
        Creation_Validate.validate_action(page, "Added Resource", "The resources had added succefully")
    # =======================================================================================================
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
        second_item = ft.Dropdown(
            label="Count: ",
            options=[ft.dropdown.Option(i) for i in range(1,51)],
            width=150
            )
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
    # ===============================================================================================
    @staticmethod
    def _remove_row(page: ft.Page, column: ft.Column, row: ft.Row):
        column.controls.remove(row)
        page.update()
    # ===============================================================================================
    @staticmethod
    def _get_values_from_column(column: ft.Column) -> dict:
        extracted_dict = {}
        for row in column.controls:
            if isinstance(row, ft.Row):
                values = []
                for control in row.controls:
                    if isinstance(control, ft.TextField) or isinstance(control, ft.Dropdown):
                        if control.value is None:
                            continue
                        values.append(control.value)
                if len(values) == 2:
                    key = values[0]
                    try:
                        value = int(values[1])
                    except (ValueError, TypeError):
                        value = 0
                    extracted_dict[key] = value
        return extracted_dict
    # ========================================================================================================
    # funcion para buscar hueco
    @staticmethod
    def _find_avialable_slot(page:ft.Page, dom:Domain, personal_col:ft.Column, resource_col:ft.Column
                            , duration_h, duration_min, b_y, b_m, b_d, b_h, b_min
                            , e_y, e_m, e_d, e_h, e_min):
        if not duration_h or not duration_min:
            Creation_Validate.validate_action(page, "Missing data", "Debe iniciar la duracion")
            return

        duration = timedelta(hours=int(duration_h), minutes=int(duration_min))
        
        personal_requested = Create_Utils._get_values_from_column(personal_col)
        resource_requested = Create_Utils._get_values_from_column(resource_col)

        if not personal_requested and not resource_requested:
            Creation_Validate.validate_action(page, "No requeriments", "Debe iniciar Personal o recursos")
            return
        begin, end = dom.find_next_avialable_slot(personal_requested, resource_requested, duration)

        b_y.value = str(begin.year)
        b_m.value = Creation_Validate._num_to_month(begin.month)
        b_d.value = str(begin.day)
        b_h.value = f"{begin.hour:02d}"
        b_min.value = f"{begin.minute:02d}"

        e_y.value = str(end.year)
        e_m.value = Creation_Validate._num_to_month(end.month)
        e_d.value = str(end.day)
        e_h.value = f"{end.hour:02d}"
        e_min.value = f"{end.minute:02d}"

        page.update()