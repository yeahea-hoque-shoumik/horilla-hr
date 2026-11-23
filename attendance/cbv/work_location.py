"""
Work location settings: the list employees choose from when checking in.
"""

from typing import Any

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from attendance.filters import WorkLocationFilter
from attendance.forms import WorkLocationForm
from attendance.models import WorkLocation
from horilla.decorators import hx_request_required
from horilla.decorators import login_required as function_login_required
from horilla.decorators import permission_required as function_permission_required
from horilla_views.cbv_methods import login_required, permission_required
from horilla_views.generic.cbv.views import (
    HorillaFormView,
    HorillaListView,
    HorillaNavView,
)

RELOAD_LIST = (
    "<script>$('#genericModal').removeClass('oh-modal--show');"
    "$('#work-location-containerReload').click();</script>"
)


@function_login_required
@function_permission_required("attendance.view_worklocation")
def work_location_view(request):
    """Work location settings page."""
    return render(request, "attendance/work_location/work_location.html")


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required(perm="attendance.view_worklocation"), name="dispatch"
)
class WorkLocationListView(HorillaListView):
    """List of work locations, including archived ones."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.view_id = "work-location-container"
        self.search_url = reverse("work-location-list")

    model = WorkLocation
    filter_class = WorkLocationFilter
    bulk_select_option = False
    show_filter_tags = False
    columns = [
        (_("Name"), "name"),
        (_("Company"), "company_id"),
        (_("Geofence"), "fence_col"),
        (_("Status"), "status_col"),
    ]
    row_attrs = """ id = "workLocationTr{get_instance_id}" """
    action_method = "action_col"

    def get_queryset(self, queryset=None, filtered=False, *args, **kwargs):
        # Archived locations stay visible so HR can restore them. The manager's
        # all() hides inactive rows; get_queryset() keeps only the company scope.
        if queryset is None:
            queryset = WorkLocation.objects.get_queryset().order_by("name")
        return super().get_queryset(queryset, filtered, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required(perm="attendance.view_worklocation"), name="dispatch"
)
class WorkLocationNavView(HorillaNavView):
    """Page header with the create action."""

    template_name = "generic/inline_nav.html"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.search_url = reverse("work-location-list")
        if self.request.user.has_perm("attendance.add_worklocation"):
            self.create_attrs = f"""
                onclick="event.stopPropagation();"
                data-toggle="oh-modal-toggle"
                data-target="#genericModal"
                hx-target="#genericModalBody"
                hx-get="{reverse('work-location-create')}"
            """

    nav_title = _("Work Locations")
    filter_instance = WorkLocationFilter()
    search_swap_target = "#listContainer"


class WorkLocationFormBase(HorillaFormView):
    """Create and edit form."""

    model = WorkLocation
    form_class = WorkLocationForm
    new_display_title = _("Create work location")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.form.instance.pk:
            self.form_class.verbose_name = _("Update work location")
        return context

    def form_valid(self, form) -> HttpResponse:
        if form.is_valid():
            updating = bool(form.instance.pk)
            form.save()
            messages.success(
                self.request,
                (
                    _("Work location updated successfully.")
                    if updating
                    else _("Work location created successfully.")
                ),
            )
            return HttpResponse(RELOAD_LIST)
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required(perm="attendance.add_worklocation"), name="dispatch"
)
class WorkLocationCreateView(WorkLocationFormBase):
    """Create a work location."""


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required(perm="attendance.change_worklocation"), name="dispatch"
)
class WorkLocationUpdateView(WorkLocationFormBase):
    """Update a work location."""


@function_login_required
@hx_request_required
@function_permission_required("attendance.change_worklocation")
@require_POST
def work_location_archive(request, pk):
    """Archive or restore a location. Past attendance keeps its location."""
    location = get_object_or_404(WorkLocation.objects.get_queryset(), pk=pk)
    location.is_active = not location.is_active
    location.save(update_fields=["is_active"])
    messages.success(
        request,
        (
            _("Work location restored.")
            if location.is_active
            else _("Work location archived.")
        ),
    )
    return HttpResponse(RELOAD_LIST)
