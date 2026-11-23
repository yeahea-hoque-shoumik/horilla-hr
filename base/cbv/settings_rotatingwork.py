"""
this page is handling the cbv methods for Rotating work from in settings
"""

from typing import Any

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _

from base.decorators import manager_can_enter
from base.filters import RotatingWorkFromFilter
from base.forms import RotatingWorkFromForm
from base.models import RotatingWorkFrom
from horilla.decorators import permission_required
from horilla_views.cbv_methods import login_required
from horilla_views.generic.cbv.views import (
    HorillaFormView,
    HorillaListView,
    HorillaNavView,
)


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("base.view_rotatingworkfrom"), name="dispatch")
class RotatingWorkFromList(HorillaListView):
    """
    list view of Rotating work from options in settings
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.search_url = reverse("rotating-list")
        self.actions = []
        if self.request.user.has_perm("base.change_rotatingworkfrom"):
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
                },
            )
        if self.request.user.has_perm("base.delete_rotatingworkfrom"):
            self.actions.append(
                {
                    "action": _("Delete"),
                    "icon": "trash-outline",
                    "attrs": """
                            class="oh-btn oh-btn--danger oh-btn--sq-sm"
                            hx-get="{get_delete_url}?model=base.rotatingworkfrom&pk={pk}"
                            data-toggle="oh-modal-toggle"
                            data-target="#deleteConfirmation"
                            hx-target="#deleteConfirmationBody"
                        """,
                }
            )

    model = RotatingWorkFrom
    filter_class = RotatingWorkFromFilter

    row_attrs = """
                id="rotatingWorkFromTr{get_delete_instance}"
                """

    columns = [
        (_("Title"), "name"),
        (_("Work From 1"), "work_from1"),
        (_("Work From 2"), "work_from2"),
        (_("Additional Work From Options"), "get_additional_worktytpes"),
    ]

    sortby_mapping = [
        (_("Title"), "name"),
        (_("Work From 1"), "work_from1__work_from"),
        (_("Work From 2"), "work_from2__work_from"),
        (_("Additional Work From Options"), "get_additional_worktytpes"),
    ]

    header_attrs = {
        "name": """ style="width:200px !important" """,
    }


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("base.view_rotatingworkfrom"), name="dispatch")
class RotatingWorkFromNav(HorillaNavView):
    """
    navbar of Rotating workfrom
    """

    template_name = "generic/inline_nav.html"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.search_url = reverse("rotating-list")
        if self.request.user.has_perm("base.add_rotatingworkfrom"):
            self.create_attrs = f"""
                                onclick = "event.stopPropagation();"
                                data-toggle="oh-modal-toggle"
                                data-target="#genericModal"
                                hx-target="#genericModalBody"
                                hx-get="{reverse('rotating-work-from-create-form')}"
                                """

    nav_title = _("Rotating Work From")
    search_swap_target = "#listContainer"
    filter_instance = RotatingWorkFromFilter()


@method_decorator(manager_can_enter("base.add_rotatingworkfrom"), name="dispatch")
@method_decorator(login_required, name="dispatch")
class DynamicRotatingWorkFromCreate(HorillaFormView):
    """
    form view for creating dynamic rotating work from
    """

    model = RotatingWorkFrom
    form_class = RotatingWorkFromForm
    template_name = "cbv/rotating_work_from/forms/inherit.html"
    new_display_title = _("Create Rotating Work From")
    is_dynamic_create_view = True

    def form_valid(self, form: RotatingWorkFromForm) -> HttpResponse:
        if form.is_valid():
            form.save()
            messages.success(self.request, _("Rotating Work From Created"))
            return self.HttpResponse("<script>$('#reloadMessagesbutton').click();")
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("base.add_rotatingworkfrom"), name="dispatch")
class RotatingWorkFromsCreateForm(DynamicRotatingWorkFromCreate):
    """
    form view for creating rotating work from options in settings
    """

    is_dynamic_create_view = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class()

        if self.form.instance.pk:
            form = self.form_class(instance=self.form.instance)
            self.form_class.verbose_name = _("Update Rotating Work From")
        context[form] = form
        return context

    def form_invalid(self, form: Any) -> HttpResponse:
        if self.form.instance.pk:
            self.form_class.verbose_name = _("Update Work From")
        if not form.is_valid():
            errors = form.errors.as_data()
            return render(
                self.request, self.template_name, {"form": form, "errors": errors}
            )
        return super().form_invalid(form)

    def form_valid(self, form: RotatingWorkFromForm) -> HttpResponse:
        if form.is_valid():
            if form.instance.pk:
                messages.success(self.request, _("Rotating Work From Updated"))
            else:
                messages.success(self.request, _("Rotating Work From Created"))
            form.save()
            return self.HttpResponse("")
        return super().form_valid(form)
