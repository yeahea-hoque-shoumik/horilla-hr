import logging
from datetime import datetime, timedelta
from typing import Any

from django.db.models import Q
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_noop
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from base.filters import (
    RotatingShiftAssignFilters,
    RotatingWorkFromAssignFilter,
    ShiftRequestFilter,
    WorkFromRequestFilter,
)
from base.models import (
    Announcement,
    AnnouncementExpire,
    AnnouncementView,
    Company,
    Department,
    EmployeeShift,
    EmployeeShiftSchedule,
    JobPosition,
    JobRole,
    RotatingShift,
    RotatingShiftAssign,
    RotatingWorkFrom,
    RotatingWorkFromAssign,
    ShiftRequest,
    ShiftRequestComment,
    WorkFrom,
    WorkFromRequest,
    WorkFromRequestComment,
)
from base.views import (
    is_reportingmanger,
    rotating_work_from_assign_export,
    shift_request_export,
    work_from_request_export,
)
from employee.models import Actiontype, Employee
from horilla_api.api_methods.base.announcements import (
    serialize_announcement,
    visible_announcements,
)
from horilla_api.api_methods.base.methods import reject_reason_from
from horilla_api.api_methods.base.pagination import HorillaPageNumberPagination
from notifications.signals import notify

from ...api_decorators.base.decorators import (
    check_approval_status,
    manager_or_owner_permission_required,
    manager_permission_required,
    permission_required,
)
from ...api_methods.base.capabilities import build_capabilities
from ...api_methods.base.methods import groupby_queryset, permission_based_queryset
from ...api_serializers.base.serializers import (
    CompanySerializer,
    DepartmentSerializer,
    EmployeeShiftScheduleSerializer,
    EmployeeShiftSerializer,
    JobPositionSerializer,
    JobRoleSerializer,
    RotatingShiftAssignSerializer,
    RotatingShiftSerializer,
    RotatingWorkFromAssignSerializer,
    RotatingWorkFromSerializer,
    ShiftRequestSerializer,
    WorkFromRequestSerializer,
    WorkFromSerializer,
)


def object_check(cls, pk):
    try:
        obj = cls.objects.get(id=pk)
        return obj
    except cls.DoesNotExist:
        return None


def object_delete(cls, pk):
    try:
        cls.objects.get(id=pk).delete()
        return "", 200
    except Exception as e:
        return {"error": str(e)}, 400


def individual_permssion_check(request):
    employee_id = request.GET.get("employee_id")
    employee = Employee.objects.filter(id=employee_id).first()
    if request.user.employee_get == employee:
        return True
    elif employee.employee_work_info.reporting_manager_id == request.user.employee_get:
        return True
    elif request.user.has_perm("base.view_rotatingworkfromassign"):
        return True
    return False


def _is_reportingmanger(request, instance):
    """
    If the instance have employee id field then you can use this method to know the request
    user employee is the reporting manager of the instance
    """
    manager = request.user.employee_get
    try:
        employee_work_info_manager = instance.employee_work_info.reporting_manager_id
    except Exception:
        # Same bug as base.views.is_reportingmanger: an HttpResponse is
        # truthy, so every caller of this in an `or` chain treated "no work
        # info" as "yes, you may".
        return False
    return manager == employee_work_info_manager


logger = logging.getLogger(__name__)


def _revert_work_info(employee, was_approved, **fields):
    """
    Put an employee's shift / work from back when a request is cancelled.

    Only a request that had been approved changed anything, so only that
    one is reverted. Rejecting a still-pending request used to overwrite the
    employee's current value with the request's "previous" one -- stale if
    anything changed since the request was made. An employee with no work
    information has nothing to revert; that used to raise instead.
    """
    if not was_approved:
        return
    work_info = getattr(employee, "employee_work_info", None)
    if work_info is None:
        return
    for field, value in fields.items():
        setattr(work_info, field, value)
    work_info.save()


class JobPositionView(APIView):
    serializer_class = JobPositionSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(permission_required("base.view_jobposition"))
    def get(self, request, pk=None):
        if pk:
            job_position = object_check(JobPosition, pk)
            if job_position is None:
                return Response({"error": _("Job position not found ")}, status=404)
            serializer = self.serializer_class(job_position)
            return Response(serializer.data, status=200)

        job_positions = JobPosition.objects.all()
        paginater = HorillaPageNumberPagination()
        page = paginater.paginate_queryset(job_positions, request)
        serializer = self.serializer_class(page, many=True)
        return paginater.get_paginated_response(serializer.data)

    @method_decorator(permission_required("base.change_jobposition"))
    def put(self, request, pk):
        job_position = object_check(JobPosition, pk)
        if job_position is None:
            return Response({"error": _("Job position not found ")}, status=404)
        serializer = self.serializer_class(job_position, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @method_decorator(permission_required("base.add_jobposition"))
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @method_decorator(permission_required("base.delete_jobposition"))
    def delete(self, request, pk):
        job_position = object_check(JobPosition, pk)
        if job_position is None:
            return Response({"error": _("Job position not found ")}, status=404)
        response, status_code = object_delete(JobPosition, pk)
        return Response(response, status=status_code)


class DepartmentView(APIView):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(permission_required("base.view_department"), name="dispatch")
    def get(self, request, pk=None):
        if pk:
            department = object_check(Department, pk)
            if department is None:
                return Response({"error": _("Department not found ")}, status=404)
            serializer = self.serializer_class(department)
            return Response(serializer.data, status=200)

        departments = Department.objects.all()
        paginator = HorillaPageNumberPagination()
        page: list[Any] | None = paginator.paginate_queryset(departments, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @method_decorator(permission_required("base.change_department"), name="dispatch")
    def put(self, request, pk):
        department = object_check(Department, pk)
        if department is None:
            return Response({"error": _("Department not found ")}, status=404)
        serializer = self.serializer_class(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @method_decorator(permission_required("base.add_department"), name="dispatch")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @method_decorator(permission_required("base.delete_department"), name="dispatch")
    def delete(self, request, pk):
        department = object_check(Department, pk)
        if department is None:
            return Response({"error": _("Department not found ")}, status=404)
        response, status_code = object_delete(Department, pk)
        return Response(response, status=status_code)


class JobRoleView(APIView):
    serializer_class = JobRoleSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(permission_required("base.view_jobrole"), name="dispatch")
    def get(self, request, pk=None):
        if pk:
            job_role = object_check(JobRole, pk)
            if job_role is None:
                return Response({"error": _("Job role not found ")}, status=404)
            serializer = self.serializer_class(job_role)
            return Response(serializer.data, status=200)

        job_roles = JobRole.objects.all()
        paginator = HorillaPageNumberPagination()
        page = paginator.paginate_queryset(job_roles, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @method_decorator(permission_required("base.change_jobrole"), name="dispatch")
    def put(self, request, pk):
        job_role = object_check(JobRole, pk)
        if job_role is None:
            return Response({"error": _("Job role not found ")}, status=404)
        serializer = self.serializer_class(job_role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @method_decorator(permission_required("base.add_jobrole"), name="dispatch")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @method_decorator(permission_required("base.delete_jobrole"), name="dispatch")
    def delete(self, request, pk):
        job_role = object_check(JobRole, pk)
        if job_role is None:
            return Response({"error": _("Job role not found ")}, status=404)
        response, status_code = object_delete(JobRole, pk)
        return Response(response, status=status_code)


class CompanyView(APIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(permission_required("base.view_company"), name="dispatch")
    def get(self, request, pk=None):
        if pk:
            company = object_check(Company, pk)
            if company is None:
                return Response({"error": _("Company not found ")}, status=404)
            serializer = self.serializer_class(company)
            return Response(serializer.data, status=200)

        companies = Company.objects.all()
        paginator = HorillaPageNumberPagination()
        page = paginator.paginate_queryset(companies, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @method_decorator(permission_required("base.change_company"), name="dispatch")
    def put(self, request, pk):
        company = object_check(Company, pk)
        if company is None:
            return Response({"error": _("Company not found ")}, status=404)
        serializer = self.serializer_class(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @method_decorator(permission_required("base.add_company"), name="dispatch")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @method_decorator(permission_required("base.delete_company"), name="dispatch")
    def delete(self, request, pk):
        company = object_check(Company, pk)
        if company is None:
            return Response({"error": _("Company not found ")}, status=400)
        response, status_code = object_delete(Company, pk)
        return Response(response, status=status_code)


class WorkFromView(APIView):
    serializer_class = WorkFromSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            work_from = object_check(WorkFrom, pk)
            if work_from is None:
                return Response({"error": _("WorkFrom not found")}, status=404)
            serializer = self.serializer_class(work_from)
            return Response(serializer.data, status=200)

        work_froms = WorkFrom.objects.all()
        serializer = self.serializer_class(work_froms, many=True)
        return Response(serializer.data)

    @method_decorator(permission_required("base.add_workfrom"), name="dispatch")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @method_decorator(permission_required("base.change_workfrom"), name="dispatch")
    def put(self, request, pk):
        work_from = object_check(WorkFrom, pk)
        if work_from is None:
            return Response({"error": _("WorkFrom not found")}, status=404)
        serializer = self.serializer_class(work_from, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @method_decorator(permission_required("base.delete_workfrom"), name="dispatch")
    def delete(self, request, pk):
        work_from = object_check(WorkFrom, pk)
        if work_from is None:
            return Response({"error": _("WorkFrom not found")}, status=404)
        response, status_code = object_delete(WorkFrom, pk)
        return Response(response, status=status_code)


class WorkFromRequestView(APIView):
    serializer_class = WorkFromRequestSerializer
    filterset_class = WorkFromRequestFilter
    permission_classes = [IsAuthenticated]
    queryset = WorkFromRequest.objects.none()  # For drf-yasg schema generation

    def get_queryset(self, request=None):
        # Handle schema generation for DRF-YASG
        if getattr(self, "swagger_fake_view", False) or request is None:
            return WorkFromRequest.objects.none()
        queryset = WorkFromRequest.objects.all()
        user = request.user
        # checking user level permissions
        perm = "base.view_workfromrequest"
        queryset = permission_based_queryset(user, perm, queryset, user_obj=True)
        return queryset

    def get(self, request, pk=None):
        # individual object workflow
        if pk:
            work_from_request = object_check(WorkFromRequest, pk)
            if work_from_request is None:
                return Response({"error": _("WorkFromRequest not found")}, status=404)
            serializer = self.serializer_class(work_from_request)
            return Response(serializer.data, status=200)
        # permission based queryset
        work_from_requests = self.get_queryset(request)
        # filtering queryset
        work_from_request_filter_queryset = self.filterset_class(
            request.GET, queryset=work_from_requests
        ).qs
        # groupby workflow
        field_name = request.GET.get("groupby_field", None)
        if field_name:
            url = request.build_absolute_uri()
            return groupby_queryset(
                request, url, field_name, work_from_request_filter_queryset
            )
        # pagination workflow
        paginater = HorillaPageNumberPagination()
        page = paginater.paginate_queryset(work_from_request_filter_queryset, request)
        serializer = self.serializer_class(page, many=True)
        return paginater.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        if not request.user.has_perm("base.add_workfromrequest"):
            data["employee_id"] = request.user.employee_get.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            # The request is saved at this point. A notification failure --
            # most often an employee with no reporting manager or no work
            # information -- must not turn that into a 400, or the client
            # reports a failure for a request that exists and a retry
            # creates a duplicate.
            try:
                notify.send(
                    instance.employee_id,
                    recipient=instance.employee_id.employee_work_info.reporting_manager_id.employee_user_id,
                    verb=gettext_noop(
                        "You have new work from request to validate for %(employee)s"
                    ),
                    verb_params={"employee": str(instance.employee_id)},
                    icon="information",
                    redirect=f"/employee/work-from-request-view?id={instance.id}",
                    api_redirect=f"/api/base/workfrom-requests/{instance.id}",
                )
            except Exception:
                logger.warning(
                    "Work from request %s saved, but notifying the reporting "
                    "manager failed",
                    instance.id,
                    exc_info=True,
                )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @check_approval_status(WorkFromRequest, "base.change_workfromrequest")
    @manager_or_owner_permission_required(
        WorkFromRequest, "base.change_workfromrequest"
    )
    def put(self, request, pk):
        work_from_request = object_check(WorkFromRequest, pk)
        if work_from_request is None:
            return Response({"error": _("WorkFromRequest not found")}, status=404)
        serializer = self.serializer_class(work_from_request, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @check_approval_status(WorkFromRequest, "base.change_workfromrequest")
    @manager_or_owner_permission_required(
        WorkFromRequest, "base.delete_workfromrequest"
    )
    def delete(self, request, pk):
        work_from_request = object_check(WorkFromRequest, pk)
        if work_from_request is None:
            return Response({"error": _("WorkFromRequest not found")}, status=404)
        response, status_code = object_delete(WorkFromRequest, pk)
        return Response(response, status=status_code)


class WorkFromRequestCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        work_from_request = WorkFromRequest.find(pk)
        if (
            is_reportingmanger(request, work_from_request)
            or request.user.has_perm("base.cancel_workfromrequest")
            or work_from_request.employee_id == request.user.employee_get
            and work_from_request.approved == False
        ):
            was_approved = work_from_request.approved
            work_from_request.canceled = True
            work_from_request.approved = False
            _revert_work_info(
                work_from_request.employee_id,
                was_approved,
                work_from_id=work_from_request.previous_work_from_id,
            )
            work_from_request.save()
            reason = reject_reason_from(request)
            if reason:
                WorkFromRequestComment.objects.create(
                    request_id=work_from_request,
                    employee_id=request.user.employee_get,
                    comment=reason,
                )
            try:
                notify.send(
                    request.user.employee_get,
                    recipient=work_from_request.employee_id.employee_user_id,
                    verb=gettext_noop("Your work from request has been rejected."),
                    redirect=f"/employee/work-from-request-view?id={work_from_request.id}",
                    icon="close",
                    api_redirect="/api/base/workfrom-requests/<int:pk>/",
                )
            except Exception:
                logger.warning(
                    "Work from request %s rejected, but notifying the "
                    "employee failed",
                    work_from_request.id,
                    exc_info=True,
                )
            return Response({"status": "canceled"}, status=200)
        # Previously answered 200 here too, so a refused rejection looked
        # identical to a successful one.
        return Response({"error": _("You don't have permission")}, status=400)


class WorkRequestApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        work_from_request = WorkFromRequest.find(pk)
        if (
            is_reportingmanger(request, work_from_request)
            or request.user.has_perm("base.approve_workfromrequest")
            or request.user.has_perm("base.change_workfromrequest")
        ) and not work_from_request.approved:
            """
            Here the request will be approved, can send mail right here
            """
            # Previously fell through and returned None -- a 500 -- when an
            # overlapping approved request already existed.
            if work_from_request.is_any_work_from_request_exists():
                return Response(
                    {
                        "error": _(
                            "An approved work from request already exists "
                            "during this time period."
                        )
                    },
                    status=400,
                )
            work_from_request.approved = True
            work_from_request.canceled = False
            work_from_request.save()
            # Approved and saved: a notification failure is logged, not
            # reported as a failed approval.
            try:
                notify.send(
                    request.user.employee_get,
                    recipient=work_from_request.employee_id.employee_user_id,
                    verb=gettext_noop("Your work from request has been approved."),
                    redirect=f"/employee/work-from-request-view?id={work_from_request.id}",
                    icon="checkmark",
                    api_redirect="/api/base/workfrom-requests/<int:pk>/",
                )
            except Exception:
                logger.warning(
                    "Work from request %s approved, but notifying the "
                    "employee failed",
                    work_from_request.id,
                    exc_info=True,
                )
            return Response({"status": "approved"})
        else:
            return Response({"error": _("You don't have permission")}, status=400)


class WorkFromRequestExport(APIView):
    permission_classes = [IsAuthenticated]

    @manager_permission_required("base.view_workfromrequest")
    def get(self, request):
        return work_from_request_export(request)


class IndividualRotatingWorkFromsView(APIView):
    serializer_class = RotatingWorkFromAssignSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if individual_permssion_check(request) == False:
            return Response({"error": _("you have no permission to view")}, status=400)
        if pk:
            rotating_work_from_assign = object_check(RotatingWorkFromAssign, pk)
            if rotating_work_from_assign is None:
                return Response(
                    {"error": _("RotatingWorkFromAssign not found")}, status=404
                )
            serializer = self.serializer_class(rotating_work_from_assign)
            return Response(serializer.data, status=200)
        employee_id = request.GET.get("employee_id", None)
        rotating_work_from_assigns = RotatingWorkFromAssign.objects.filter(
            employee_id=employee_id
        )
        pagenation = HorillaPageNumberPagination()
        page = pagenation.paginate_queryset(rotating_work_from_assigns, request)
        serializer = self.serializer_class(page, many=True)
        return pagenation.get_paginated_response(serializer.data)


class RotatingWorkFromAssignView(APIView):
    serializer_class = RotatingWorkFromAssignSerializer
    filterset_class = RotatingWorkFromAssignFilter
    permission_classes = [IsAuthenticated]
    queryset = RotatingWorkFromAssign.objects.none()  # For drf-yasg schema generation

    @manager_or_owner_permission_required(
        RotatingWorkFromAssign, "base.view_rotatingworkfromassign"
    )
    def get(self, request, pk=None):

        if pk:

            rotating_work_from_assign = object_check(RotatingWorkFromAssign, pk)
            if rotating_work_from_assign is None:
                return Response(
                    {"error": _("RotatingWorkFromAssign not found")}, status=404
                )
            serializer = self.serializer_class(rotating_work_from_assign)
            return Response(serializer.data, status=200)
        rotating_work_from_assigns = RotatingWorkFromAssign.objects.all()
        rotating_work_from_assigns_filter_queryset = self.filterset_class(
            request.GET, queryset=rotating_work_from_assigns
        ).qs
        field_name = request.GET.get("groupby_field", None)
        if field_name:
            # groupby workflow
            url = request.build_absolute_uri()
            return groupby_queryset(
                request, url, field_name, rotating_work_from_assigns_filter_queryset
            )

        pagenation = HorillaPageNumberPagination()
        page = pagenation.paginate_queryset(
            rotating_work_from_assigns_filter_queryset, request
        )
        serializer = self.serializer_class(page, many=True)
        return pagenation.get_paginated_response(serializer.data)

    @manager_permission_required("base.add_rotatingworkfromassign")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            try:
                users = [employee.employee_user_id for employee in obj]
                notify.send(
                    request.user.employee_get,
                    recipient=users,
                    verb=gettext_noop("You are added to rotating work from"),
                    icon="infinite",
                    redirect="/employee/employee-profile/",
                    api_redirect="",
                )
            except:
                pass
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @manager_or_owner_permission_required(
        RotatingWorkFromAssign, "base.change_rotatingworkfromassign"
    )
    def put(self, request, pk):
        rotating_work_from_assign = object_check(RotatingWorkFromAssign, pk)
        if rotating_work_from_assign is None:
            return Response(
                {"error": _("RotatingWorkFromAssign not found")}, status=404
            )
        serializer = self.serializer_class(rotating_work_from_assign, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @manager_or_owner_permission_required(
        RotatingWorkFromAssign, "base.delete_rotatingworkfromassign"
    )
    def delete(self, request, pk):
        rotating_work_from_assign = object_check(RotatingWorkFromAssign, pk)
        if rotating_work_from_assign is None:
            return Response(
                {"error": _("RotatingWorkFromAssign not found")}, status=404
            )
        response, status_code = object_delete(RotatingWorkFromAssign, pk)
        return Response(response, status=status_code)


class IndividualWorkFromRequestView(APIView):
    serializer_class = WorkFromRequestSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if individual_permssion_check(request) == False:
            return Response({"error": _("you have no permission to view")}, status=400)

        # individual object workflow
        if pk:
            work_from_request = object_check(WorkFromRequest, pk)
            if work_from_request is None:
                return Response({"error": _("WorkFromRequest not found")}, status=404)
            serializer = self.serializer_class(work_from_request)
            return Response(serializer.data, status=200)
        employee_id = request.GET.get("employee_id", None)
        work_from_request = WorkFromRequest.objects.filter(employee_id=employee_id)
        paginater = HorillaPageNumberPagination()
        page = paginater.paginate_queryset(work_from_request, request)
        serializer = self.serializer_class(page, many=True)
        return paginater.get_paginated_response(serializer.data)


class EmployeeShiftView(APIView):
    serializer_class = EmployeeShiftSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            employee_shift = object_check(EmployeeShift, pk)
            if employee_shift is None:
                return Response({"error": _("EmployeeShift not found")}, status=404)
            serializer = self.serializer_class(employee_shift)
            return Response(serializer.data, status=200)

        employee_shifts = EmployeeShift.objects.all()
        serializer = self.serializer_class(employee_shifts, many=True)
        return Response(serializer.data, status=200)

    @method_decorator(permission_required("base.add_employeeshift"), name="dispatch")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @method_decorator(permission_required("base.change_employeeshift"), name="dispatch")
    def put(self, request, pk):
        employee_shift = object_check(EmployeeShift, pk)
        if employee_shift is None:
            return Response({"error": _("EmployeeShift not found")}, status=404)
        serializer = self.serializer_class(employee_shift, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @method_decorator(permission_required("base.delete_employeeshift"), name="dispatch")
    def delete(self, request, pk):
        employee_shift = object_check(EmployeeShift, pk)
        if employee_shift is None:
            return Response({"error": _("EmployeeShift not found")}, status=404)
        response, status_code = object_delete(EmployeeShift, pk)
        return Response(response, status=status_code)


class EmployeeShiftScheduleView(APIView):
    serializer_class = EmployeeShiftScheduleSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(
        permission_required("base.view_employeeshiftschedule"), name="dispatch"
    )
    def get(self, request, pk=None):
        if pk:
            employee_shift_schedule = object_check(EmployeeShiftSchedule, pk)
            if employee_shift_schedule is None:
                return Response(
                    {"error": _("EmployeeShiftSchedule not found")}, status=404
                )
            serializer = self.serializer_class(employee_shift_schedule)
            return Response(serializer.data, status=200)

        employee_shift_schedules = EmployeeShiftSchedule.objects.all()
        serializer = self.serializer_class(employee_shift_schedules, many=True)
        return Response(serializer.data, status=200)

    @method_decorator(
        permission_required("base.add_employeeshiftschedule"), name="dispatch"
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @method_decorator(
        permission_required("base.change_employeeshiftschedule"), name="dispatch"
    )
    def put(self, request, pk):
        employee_shift_schedule = object_check(EmployeeShiftSchedule, pk)
        if employee_shift_schedule is None:
            return Response({"error": _("EmployeeShiftSchedule not found")}, status=404)
        serializer = self.serializer_class(employee_shift_schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @method_decorator(
        permission_required("base.delete_employeeshiftschedule"), name="dispatch"
    )
    def delete(self, request, pk):
        employee_shift_schedule = object_check(EmployeeShiftSchedule, pk)
        if employee_shift_schedule is None:
            return Response({"error": _("EmployeeShiftSchedule not found")}, status=404)
        response, status_code = object_delete(EmployeeShiftSchedule, pk)
        return Response(response, status=status_code)


class RotatingShiftView(APIView):
    serializer_class = RotatingShiftSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(permission_required("base.view_rotatingshift"), name="dispatch")
    def get(self, request, pk=None):

        if pk:
            rotating_shift = object_check(RotatingShift, pk)
            if rotating_shift is None:
                return Response({"error": _("RotatingShift not found")}, status=404)
            serializer = self.serializer_class(rotating_shift)
            return Response(serializer.data, status=200)

        employee_id = request.GET.get(
            "employee_id"
        )  # Get the employee_id from query parameters
        if employee_id:  # Check if employee_ids are present in the request
            rotating_shifts = RotatingShift.objects.filter(
                employee_id__in=[employee_id]
            )

        rotating_shifts = RotatingShift.objects.all()
        serializer = self.serializer_class(rotating_shifts, many=True)
        return Response(serializer.data, status=200)

    @method_decorator(permission_required("base.add_rotatingshift"), name="dispatch")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @method_decorator(permission_required("base.change_rotatingshift"), name="dispatch")
    def put(self, request, pk):
        rotating_shift = object_check(RotatingShift, pk)
        if rotating_shift is None:
            return Response({"error": _("RotatingShift not found")}, status=404)
        serializer = self.serializer_class(rotating_shift, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @method_decorator(permission_required("base.delete_rotatingshift"), name="dispatch")
    def delete(self, request, pk):
        rotating_shift = object_check(RotatingShift, pk)
        if rotating_shift is None:
            return Response({"error": _("RotatingShift not found")}, status=404)
        response, status_code = object_delete(RotatingShift, pk)
        return Response(response, status=status_code)


class IndividualRotatingShiftView(APIView):
    serializer_class = RotatingShiftAssignSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if individual_permssion_check(request) == False:
            return Response({"error": _("you have no permission to view")}, status=400)

        if pk:
            rotating_shift_assign = object_check(RotatingShiftAssign, pk)
            if rotating_shift_assign is None:
                return Response(
                    {"error": _("RotatingShiftAssign not found")}, status=404
                )
            serializer = self.serializer_class(rotating_shift_assign)
            return Response(serializer.data, status=200)
        employee_id = request.GET.get("employee_id", None)
        rotating_shift_assigns = RotatingShiftAssign.objects.filter(
            employee_id=employee_id
        )

        paginator = HorillaPageNumberPagination()
        page = paginator.paginate_queryset(rotating_shift_assigns, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class RotatingShiftAssignView(APIView):
    serializer_class = RotatingShiftAssignSerializer
    filterset_class = RotatingShiftAssignFilters
    permission_classes = [IsAuthenticated]
    queryset = RotatingShiftAssign.objects.none()  # For drf-yasg schema generation

    @manager_or_owner_permission_required(
        RotatingShiftAssign, "base.view_rotatingshiftassign"
    )
    def get(self, request, pk=None):
        if pk:
            rotating_shift_assign = object_check(RotatingShiftAssign, pk)
            if rotating_shift_assign is None:
                return Response(
                    {"error": _("RotatingShiftAssign not found")}, status=404
                )
            serializer = self.serializer_class(rotating_shift_assign)
            return Response(serializer.data, status=200)

        rotating_shift_assigns = RotatingShiftAssign.objects.all()
        rotating_shift_assigns_filter_queryset = self.filterset_class(
            request.GET, queryset=rotating_shift_assigns
        ).qs
        field_name = request.GET.get("groupby_field", None)
        if field_name:
            # groupby workflow
            url = request.build_absolute_uri()
            return groupby_queryset(
                request, url, field_name, rotating_shift_assigns_filter_queryset
            )

        paginator = HorillaPageNumberPagination()
        page = paginator.paginate_queryset(
            rotating_shift_assigns_filter_queryset, request
        )
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @manager_permission_required("base.add_rotatingshiftassign")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @manager_or_owner_permission_required(
        RotatingShiftAssign, "base.change_rotatingshiftassign"
    )
    def put(self, request, pk):
        rotating_shift_assign = object_check(RotatingShiftAssign, pk)
        if rotating_shift_assign is None:
            return Response({"error": _("RotatingShiftAssign not found")}, status=404)
        serializer = self.serializer_class(rotating_shift_assign, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @manager_or_owner_permission_required(
        RotatingShiftAssign, "base.delete_rotatingshiftassign"
    )
    def delete(self, request, pk):
        rotating_shift_assign = object_check(RotatingShiftAssign, pk)
        if rotating_shift_assign is None:
            return Response({"error": _("RotatingShiftAssign not found")}, status=404)
        response, status_code = object_delete(RotatingShiftAssign, pk)
        return Response(response, status=status_code)


class IndividualShiftRequestView(APIView):
    serializer_class = ShiftRequestSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if individual_permssion_check(request) == False:
            return Response({"error": _("you have no permission to view")}, status=400)

        if pk:
            shift_request = object_check(ShiftRequest, pk)
            if shift_request is None:
                return Response({"error": _("EmployeeShift not found")}, status=404)
            serializer = self.serializer_class(shift_request)
            return Response(serializer.data, status=200)
        employee_id = request.GET.get("employee_id", None)
        shift_requests = ShiftRequest.objects.filter(employee_id=employee_id)
        paginater = HorillaPageNumberPagination()
        page = paginater.paginate_queryset(shift_requests, request)
        serializer = self.serializer_class(page, many=True)
        return paginater.get_paginated_response(serializer.data)


class ShiftRequestView(APIView):
    serializer_class = ShiftRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShiftRequestFilter
    permission_classes = [IsAuthenticated]
    queryset = ShiftRequest.objects.none()  # For drf-yasg schema generation

    def get_queryset(self, request=None):
        # Handle schema generation for DRF-YASG
        if getattr(self, "swagger_fake_view", False) or request is None:
            return ShiftRequest.objects.none()
        queryset = ShiftRequest.objects.all()
        user = request.user
        # checking user level permissions
        perm = "base.view_shiftrequest"
        queryset = permission_based_queryset(user, perm, queryset, user_obj=True)
        return queryset

    def get(self, request, pk=None):
        # individual section
        if pk:
            shift_request = object_check(ShiftRequest, pk)
            if shift_request is None:
                return Response({"error": _("ShiftRequest not found")}, status=404)
            serializer = self.serializer_class(shift_request)
            return Response(serializer.data, status=200)
        # filter section
        shift_requests = self.get_queryset(request)
        shift_requests_filter_queryset = self.filterset_class(
            request.GET, queryset=shift_requests
        ).qs
        # groupby section
        field_name = request.GET.get("groupby_field", None)
        if field_name:
            url = request.build_absolute_uri()
            return groupby_queryset(
                request, url, field_name, shift_requests_filter_queryset
            )
        # pagination section
        paginator = HorillaPageNumberPagination()
        page = paginator.paginate_queryset(shift_requests_filter_queryset, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        if not request.user.has_perm("base.add_shiftrequest"):
            data["employee_id"] = request.user.employee_get.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @check_approval_status(ShiftRequest, "base.change_shiftrequest")
    @manager_or_owner_permission_required(ShiftRequest, "base.change_shiftrequest")
    def put(self, request, pk):
        shift_request = object_check(ShiftRequest, pk)
        if shift_request is None:
            return Response({"error": _("ShiftRequest not found")}, status=404)
        serializer = self.serializer_class(shift_request, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @check_approval_status(ShiftRequest, "base.delete_shiftrequest")
    @manager_or_owner_permission_required(ShiftRequest, "base.delete_shiftrequest")
    def delete(self, request, pk):
        shift_request = object_check(ShiftRequest, pk)
        if shift_request is None:
            return Response({"error": _("ShiftRequest not found")}, status=404)
        response, status_code = object_delete(ShiftRequest, pk)
        return Response(response, status=status_code)


class RotatingWorkFromView(APIView):
    serializer_class = RotatingWorkFromSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(permission_required("base.view_rotatingworkfrom"))
    def get(self, request, pk=None):
        if pk:
            rotating_work_from = object_check(RotatingWorkFrom, pk)
            if rotating_work_from is None:
                return Response({"error": _("RotatingWorkFrom not found")}, status=404)
            serializer = self.serializer_class(rotating_work_from)
            return Response(serializer.data, status=200)

        rotating_work_froms = RotatingWorkFrom.objects.all()
        serializer = self.serializer_class(rotating_work_froms, many=True)
        return Response(serializer.data, status=200)

    @method_decorator(permission_required("base.add_rotatingworkfrom"), name="dispatch")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @method_decorator(
        permission_required("base.change_rotatingworkfrom"), name="dispatch"
    )
    def put(self, request, pk):
        rotating_work_from = object_check(RotatingWorkFrom, pk)
        if rotating_work_from is None:
            return Response({"error": _("RotatingWorkFrom not found")}, status=404)
        serializer = self.serializer_class(rotating_work_from, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @method_decorator(
        permission_required("base.delete_rotatingworkfrom"), name="dispatch"
    )
    def delete(self, request, pk):
        rotating_work_from = object_check(RotatingWorkFrom, pk)
        if rotating_work_from is None:
            return Response({"error": _("RotatingWorkFrom not found")}, status=404)
        response, status_code = object_delete(RotatingWorkFrom, pk)
        return Response(response, status=status_code)


class ShiftRequestApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        shift_request = ShiftRequest.objects.get(id=pk)
        if (
            is_reportingmanger(request, shift_request)
            or request.user.has_perm("base.approve_shiftrequest")
            or request.user.has_perm("base.change_shiftrequest")
        ) and not shift_request.approved:
            """
            here the request will be approved, can send mail right here
            """
            if not shift_request.is_any_request_exists():
                shift_request.approved = True
                shift_request.canceled = False
                shift_request.save()
                return Response({"status": "success"}, status=200)
            else:
                return Response(
                    {"error": _("Already request exits on same date")}, status=400
                )

        return Response({"error": _("No permission ")}, status=400)


class ShiftRequestBulkApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ids = request.data["ids"]
        length = len(ids)
        count = 0
        for id in ids:
            shift_request = ShiftRequest.objects.get(id=id)
            if (
                is_reportingmanger(request, shift_request)
                or request.user.has_perm("base.approve_shiftrequest")
                or request.user.has_perm("base.change_shiftrequest")
            ) and not shift_request.approved:
                """
                here the request will be approved, can send mail right here
                """
                shift_request.approved = True
                shift_request.canceled = False
                employee_work_info = shift_request.employee_id.employee_work_info
                employee_work_info.shift_id = shift_request.shift_id
                employee_work_info.save()
                shift_request.save()
                count += 1
        if length == count:
            return Response({"status": "success"}, status=200)
        return Response({"status": "failed"}, status=400)


class ShiftRequestCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        shift_request = ShiftRequest.objects.get(id=pk)
        if (
            is_reportingmanger(request, shift_request)
            or request.user.has_perm("base.cancel_shiftrequest")
            or shift_request.employee_id == request.user.employee_get
            and shift_request.approved == False
        ):
            was_approved = shift_request.approved
            shift_request.canceled = True
            shift_request.approved = False
            _revert_work_info(
                shift_request.employee_id,
                was_approved,
                shift_id=shift_request.previous_shift_id,
            )
            shift_request.save()
            reason = reject_reason_from(request)
            if reason:
                # Stored as a comment -- the request model has no reason
                # field, and comments are what the web shows on a request.
                ShiftRequestComment.objects.create(
                    request_id=shift_request,
                    employee_id=request.user.employee_get,
                    comment=reason,
                )
            return Response({"status": "success"}, status=200)
        return Response({"status": "failed"}, status=400)


class ShiftRequestBulkCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ids = request.data.get("ids", None)
        length = len(ids)
        count = 0
        for id in ids:
            shift_request = ShiftRequest.objects.get(id=id)
            if (
                is_reportingmanger(request, shift_request)
                or request.user.has_perm("base.cancel_shiftrequest")
                or shift_request.employee_id == request.user.employee_get
                and shift_request.approved == False
            ):
                was_approved = shift_request.approved
                shift_request.canceled = True
                shift_request.approved = False
                _revert_work_info(
                    shift_request.employee_id,
                    was_approved,
                    shift_id=shift_request.previous_shift_id,
                )
                shift_request.save()
                count += 1
        if length == count:
            return Response({"status": "success"}, status=200)
        return Response({"status": "failed"}, status=400)


class ShiftRequestDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(permission_required("base.delete_shiftrequest"))
    def delete(self, request, pk=None):

        if pk is None:
            try:
                ids = request.data["ids"]
                shift_requests = ShiftRequest.objects.filter(id__in=ids)
                shift_requests.delete()
            except Exception as e:
                return Response({"status": "failed", "error": str(e)}, status=400)
            return Response({"status": "success"}, status=200)
        try:
            shift_request = ShiftRequest.objects.get(id=pk)
            if not shift_request.approved:
                raise
            shift_request.delete()

        except ShiftRequest.DoesNotExist:
            return Response(
                {"status": "failed", "error": _("Shift request does not exists")},
                status=400,
            )
        return Response({"status": "deleted"}, status=200)


class ShiftRequestExportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return shift_request_export(request)


class ShiftRequestAllocationView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(permission_required("base.change_shiftrequest"))
    def post(self, request, id):
        shift_request = ShiftRequest.objects.get(id=id)
        if not shift_request.is_any_request_exists():
            shift_request.reallocate_approved = True
            shift_request.reallocate_canceled = False
            shift_request.save()
            return Response({"status": "success"}, status=200)
        return Response({"status": "failed"}, status=400)


class RotatingShiftAssignExport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return rotating_work_from_assign_export(request)


class RotatingShiftAssignBulkArchive(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(permission_required("base.change_rotatingshiftassign"))
    def put(self, request, status):
        ids = request.data.get("ids", None)
        try:
            rotating_shift_asssign = RotatingShiftAssign.objects.filter(id__in=ids)
            rotating_shift_asssign.update(is_active=status)
            return Response({"status": "success"}, status=200)
        except Exception as E:
            return Response({"error": str(E)}, status=400)


class RotatingShiftAssignBulkDelete(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(permission_required("base.delete_rotatingshiftassign"))
    def delete(self, request):
        ids = request.data.get("ids", None)
        try:
            rotating_shift_asssign = RotatingShiftAssign.objects.filter(id__in=ids)
            rotating_shift_asssign.delete()
            return Response({"status": "success"}, status=200)
        except Exception as E:
            return Response({"error": str(E)}, status=400)


class RotatingWorkFromPermissionCheck(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        manager = Employee.objects.filter(id=id).first().get_reporting_manager()
        if (
            request.user.has_perm("base.add_rotatingworkfromassign")
            or request.user.employee_get == manager
        ):
            return Response(status=200)
        return Response(status=400)


class RotatingShiftPermissionCheck(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        manager = Employee.objects.filter(id=id).first().get_reporting_manager()
        if (
            request.user.has_perm("base.add_rotatingshiftassign")
            or request.user.employee_get == manager
        ):
            return Response(status=200)
        return Response(status=400)


class WorkFromRequestApprovePermissionCheck(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        instance = Employee.objects.filter(id=request.GET.get("employee_id")).first()
        if (
            _is_reportingmanger(request, instance)
            or request.user.has_perm("base.approve_workfromrequest")
            or request.user.has_perm("base.change_workfromrequest")
        ):
            return Response(status=200)
        return Response(status=400)


class ShiftRequestApprovePermissionCheck(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        instance = Employee.objects.filter(id=request.GET.get("employee_id")).first()
        if (
            _is_reportingmanger(request, instance)
            or request.user.has_perm("base.approve_shiftrequest")
            or request.user.has_perm("base.change_shiftrequest")
        ):
            return Response(status=200)
        return Response(status=400)


class EmployeeTabPermissionCheck(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        instance = Employee.objects.filter(id=request.GET.get("employee_id")).first()
        if _is_reportingmanger(request, instance) or request.user.has_perms(
            [
                "base.view_workfromrequest",
                "attendance.view_shiftrequest",
                "employee.change_employee",
            ]
        ):
            return Response(status=200)
        return Response({"message": _("No permission")}, status=400)


class CheckUserLevel(APIView):

    def get(self, request):
        perm = request.GET.get("perm")
        if request.user.has_perm(perm):
            return Response(status=200)
        return Response({"error": _("No permission")}, status=400)


class CapabilitiesAPIView(APIView):
    """
    What the signed-in user's client may show.

    The same payload login returns. Exposed separately so a long-lived client
    can refresh it when permissions change, instead of forcing a re-login to
    notice that someone became a manager.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(build_capabilities(request.user), status=200)


class AnnouncementListAPIView(APIView):
    """
    API endpoint to list announcements for the authenticated user.

    - Updates expire dates if missing.
    - Filters based on user permissions and validity.
    - Marks announcements with whether the user has viewed them.
    - Supports pagination.
    """

    permission_classes = [IsAuthenticated]
    pagination_class = HorillaPageNumberPagination

    def get(self, request, *args, **kwargs):
        # Update missing expire_date in bulk, using each announcement's
        # company-specific "Default Expire Days" setting (falling back to
        # the "All Companies" default, then 30, when unconfigured).
        announcements_to_update = (
            Announcement.objects.filter(expire_date__isnull=True)
            .only("id", "created_at")
            .prefetch_related("company_id")
        )
        expire_days_by_company = {}
        for ann in announcements_to_update:
            companies = list(ann.company_id.all())
            company = companies[0] if companies else None
            cache_key = company.id if company else None
            if cache_key not in expire_days_by_company:
                setting = AnnouncementExpire.objects.filter(company_id=company).first()
                if not setting and company is not None:
                    setting = AnnouncementExpire.objects.filter(company_id=None).first()
                expire_days_by_company[cache_key] = (
                    setting.days if setting and setting.days is not None else 30
                )
            ann.expire_date = ann.created_at + timedelta(
                days=expire_days_by_company[cache_key]
            )
        if announcements_to_update:
            Announcement.objects.bulk_update(announcements_to_update, ["expire_date"])

        announcements = visible_announcements(request)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(announcements, request)
        return paginator.get_paginated_response(
            [serialize_announcement(ann, ann.has_viewed) for ann in page]
        )


class AnnouncementDetailAPIView(APIView):
    """
    One announcement with its attachments and author, if the caller is in
    its audience. Opening it marks it viewed, as opening it on the web does.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        announcement = (
            visible_announcements(request)
            .prefetch_related("attachments")
            .filter(pk=pk)
            .first()
        )
        if announcement is None:
            return Response({"error": "Announcement not found."}, status=404)
        view, _ = AnnouncementView.objects.get_or_create(
            user=request.user, announcement=announcement
        )
        if not view.viewed:
            view.viewed = True
            view.save()
        return Response(
            serialize_announcement(announcement, True, detail=True), status=200
        )
