"""
this page is handling the cbv methods for work from in settings
"""

from typing import Any

from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _

from base.filters import WorkFromFilter
from base.models import WorkFrom
from horilla.decorators import permission_required
from horilla_views.cbv_methods import login_required
from horilla_views.generic.cbv.views import (
    HorillaDetailedView,
    HorillaListView,
    HorillaNavView,
)


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("base.view_workfrom"), name="dispatch")
class WorkFromList(HorillaListView):
    """
    list view of work from options in settings
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.search_url = reverse("workfrom-list")
        self.actions = []
        if self.request.user.has_perm("base.change_workfrom"):
            self.actions.append(
                {
                    "action": _("Edit"),
                    "icon": "create-outline",
                    "attrs": """
                            class="oh-btn oh-btn--light-bkg oh-btn--sq-sm"
                            hx-get='{get_update_url}?instance_ids={ordered_ids}'
                                    hx-target="#genericModalBody"
                                    data-toggle="oh-modal-toggle"
                                    data-target="#genericModal"
                        """,
                }
            )
        if self.request.user.has_perm("base.delete_workfrom"):
            self.actions.append(
                {
                    "action": _("Delete"),
                    "icon": "trash-outline",
                    "attrs": """
                            class="oh-btn oh-btn--danger oh-btn--sq-sm"
                            hx-get="{get_delete_url}?model=base.workfrom&pk={pk}"
                            data-toggle="oh-modal-toggle"
                            data-target="#deleteConfirmation"
                            hx-target="#deleteConfirmationBody"
                        """,
                }
            )

    model = WorkFrom
    filter_class = WorkFromFilter
    show_toggle_form = False

    columns = [
        (_("Work From"), "work_from"),
        (_("Company"), "get_company_name"),
    ]

    row_attrs = """ id="workFromTr{get_delete_instance}" """

    header_attrs = {
        "work_from": """ style="width:300px !important" """,
        "action": """ style="width:180px !important" """,
    }


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("base.view_workfrom"), name="dispatch")
class WorkFromDetailView(HorillaDetailedView):
    """
    detail view for work from, also registered as the related-object-link
    target for WorkFrom via detail_view_url_name
    """

    model = WorkFrom
    detail_view_url_name = "workfrom-detail-view"
    detail_view_permission = "base.view_workfrom"
    title = _("Work From")

    header = {
        "title": "work_from",
        "subtitle": "",
        "avatar": "",
    }

    body = [
        (_("Work From"), "work_from"),
    ]


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("base.view_workfrom"), name="dispatch")
class WorkFromNav(HorillaNavView):
    """
    navbar of workfrom
    """

    template_name = "generic/inline_nav.html"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.search_url = reverse("workfrom-list")
        if self.request.user.has_perm("base.add_workfrom"):
            self.create_attrs = f"""
                                onclick = "event.stopPropagation();"
                                data-toggle="oh-modal-toggle"
                                data-target="#genericModal"
                                hx-target="#genericModalBody"
                                hx-get="{reverse('work-from-create-form')}"
                                """

    nav_title = _("Work From")
    search_swap_target = "#listContainer"
    filter_instance = WorkFromFilter()
