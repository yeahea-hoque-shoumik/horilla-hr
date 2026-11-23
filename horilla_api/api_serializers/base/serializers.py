import datetime

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import get_error_detail

from base.models import (
    Company,
    Department,
    EmployeeShift,
    EmployeeShiftDay,
    EmployeeShiftSchedule,
    JobPosition,
    JobRole,
    RotatingShift,
    RotatingShiftAssign,
    RotatingWorkFrom,
    RotatingWorkFromAssign,
    ShiftRequest,
    WorkFrom,
    WorkFromRequest,
)
from horilla import horilla_middlewares


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

    def validate_default_work_from(self, value):
        scope = Q(company_id__isnull=True)
        if self.instance:
            scope |= Q(company_id=self.instance)
        if not WorkFrom.objects.entire().filter(scope, pk=value.pk, is_active=True).exists():
            raise serializers.ValidationError(
                _("This work from is not available for the company.")
            )
        return value


class JobPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosition
        fields = "__all__"


class JobRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRole
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

    def create(self, validated_data):
        comapny_id = validated_data.pop("company_id", [])
        obj = Department(**validated_data)
        obj.save()
        obj.company_id.set(comapny_id)
        return obj


class WorkFromSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkFrom
        fields = "__all__"

    def validate(self, attrs):
        # Create an instance of the model with the provided data
        instance = WorkFrom(**attrs)

        # Call the model's clean method for validation
        try:
            instance.clean()
        except DjangoValidationError as e:
            # Raise DRF's ValidationError with the same message
            raise serializers.ValidationError(get_error_detail(e))

        return attrs

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.clean()  # Call clean method before saving the instance
        instance.save()
        return instance


class RotatingWorkFromSerializer(serializers.ModelSerializer):
    class Meta:
        model = RotatingWorkFrom
        fields = "__all__"

    def validate(self, attrs):
        # Create an instance of the model with the provided data
        instance = RotatingWorkFrom(**attrs)

        # Call the model's clean method for validation
        try:
            instance.clean()
        except DjangoValidationError as e:
            # Raise DRF's ValidationError with the same message
            raise serializers.ValidationError(get_error_detail(e))

        return attrs

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.clean()  # Call clean method before saving the instance
        instance.save()
        return instance


class RotatingWorkFromAssignSerializer(serializers.ModelSerializer):
    rotating_work_from_name = serializers.SerializerMethodField(read_only=True)
    current_work_from_name = serializers.SerializerMethodField(read_only=True)
    next_work_from_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RotatingWorkFromAssign
        fields = "__all__"

    def get_current_work_from_name(self, instance):
        current_work_from = instance.current_work_from
        if current_work_from:
            return current_work_from.work_from
        else:
            return None  # Return null if previous_work_from_id doesn't exist

    def get_next_work_from_name(self, instance):
        next_work_from = instance.next_work_from
        if next_work_from:
            return next_work_from.work_from
        else:
            return None  # Return null if previous_work_from_id doesn't exist

    def get_rotating_work_from_name(self, instance):
        rotating_work_from_id = instance.rotating_work_from_id
        if rotating_work_from_id:
            return rotating_work_from_id.name
        else:
            return None  # Return null if previous_work_from_id doesn't exist

    def validate(self, attrs):
        if self.instance:
            return attrs
        # Create an instance of the model with the provided data
        instance = RotatingWorkFromAssign(**attrs)
        # Call the model's clean method for validation
        try:
            instance.clean()
        except DjangoValidationError as e:
            # Raise DRF's ValidationError with the same message
            raise serializers.ValidationError(get_error_detail(e))
        return attrs

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class EmployeeShiftDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeShiftDay
        fields = "__all__"


class EmployeeShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeShift
        fields = "__all__"

    def validate(self, attrs):
        # Create an instance of the model with the provided data
        instance = EmployeeShift(**attrs)

        # Call the model's clean method for validation
        try:
            instance.clean()
        except DjangoValidationError as e:
            # Raise DRF's ValidationError with the same message
            raise serializers.ValidationError(get_error_detail(e))

        return attrs

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.clean()  # Call clean method before saving the instance
        instance.save()
        return instance


class EmployeeShiftScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeShiftSchedule
        fields = "__all__"


class RotatingShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = RotatingShift
        fields = "__all__"

    def validate(self, attrs):
        # Create an instance of the model with the provided data
        instance = RotatingShift(**attrs)

        # Call the model's clean method for validation
        try:
            instance.clean()
        except DjangoValidationError as e:
            # Raise DRF's ValidationError with the same message
            raise serializers.ValidationError(get_error_detail(e))

        return attrs

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.clean()  # Call clean method before saving the instance
        instance.save()
        return instance


class RotatingShiftAssignSerializer(serializers.ModelSerializer):
    current_shift_name = serializers.SerializerMethodField(read_only=True)
    next_shift_name = serializers.SerializerMethodField(read_only=True)
    rotating_shift_name = serializers.SerializerMethodField(read_only=True)
    rotate = serializers.CharField(read_only=True)

    class Meta:
        model = RotatingShiftAssign
        fields = "__all__"

    def validate(self, attrs):
        # Create an instance of the model with the provided data
        instance = RotatingShiftAssign(**attrs)

        # Call the model's clean method for validation
        try:
            instance.clean()
        except DjangoValidationError as e:
            # Raise DRF's ValidationError with the same message
            raise serializers.ValidationError(get_error_detail(e))

        return attrs

    def create(self, validated_data):
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.based_on == "after":
            representation["rotate"] = f"Rotate after {instance.rotate_after_day} days"
        elif instance.based_on == "weekly":
            representation["rotate"] = f"Weekly every {instance.rotate_every_weekend}"
        elif instance.based_on == "monthly":
            if instance.rotate_every == "1":
                representation["rotate"] = (
                    f"Rotate every {instance.rotate_every}st day of month"
                )
            elif instance.rotate_every == "2":
                representation["rotate"] = (
                    f"Rotate every {instance.rotate_every}nd day of month"
                )
            elif instance.rotate_every == "3":
                representation["rotate"] = (
                    f"Rotate every {instance.rotate_every}rd day of month"
                )
            elif instance.rotate_every == "last":
                representation["rotate"] = "Rotate every last day of month"
            else:
                representation["rotate"] = (
                    f"Rotate every {instance.rotate_every}th day of month"
                )

        return representation

    def get_rotating_shift_name(self, instance):
        rotating_shift_id = instance.rotating_shift_id
        if rotating_shift_id:
            return rotating_shift_id.name
        else:
            return None  # Return null if previous_work_from_id doesn't exist

    def get_next_shift_name(self, instance):
        next_shift = instance.next_shift
        if next_shift:
            return next_shift.employee_shift
        else:
            return None  # Return null if previous_work_from_id doesn't exist

    def get_current_shift_name(self, instance):
        current_shift = instance.current_shift
        if current_shift:
            return current_shift.employee_shift
        else:
            return None  # Return null if previous_work_from_id doesn't exist

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.clean()  # Call clean method before saving the instance
        instance.save()
        return instance


class WorkFromRequestSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(
        source="employee_id.employee_first_name", read_only=True
    )
    employee_last_name = serializers.CharField(
        source="employee_id.employee_last_name", read_only=True
    )
    work_from_name = serializers.CharField(
        source="work_from_id.work_from", read_only=True
    )
    previous_work_from_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WorkFromRequest
        fields = "__all__"
        read_only_fields = ("approved", "canceled", "work_from_changed")

    def validate(self, attrs):
        request = getattr(horilla_middlewares._thread_locals, "request", None)
        # Check if the user is not a superuser
        requested_date = attrs.get("requested_date", None)

        if request and not request.user.is_superuser:

            if requested_date and requested_date < datetime.datetime.today().date():
                raise serializers.ValidationError(
                    {
                        "requested_date": _(
                            "Date must be greater than or equal to today."
                        )
                    }
                )

        # Validate requested_till is not earlier than requested_date
        requested_till = attrs.get("requested_till", None)
        if requested_till and requested_till < requested_date:
            raise serializers.ValidationError(
                {
                    "requested_till": _(
                        "End date must be greater than or equal to start date."
                    )
                }
            )

        # Check if any work from request already exists
        if self.instance and self.instance.is_any_work_from_request_exists():
            raise serializers.ValidationError(
                {
                    "error": _(
                        "A work from request already exists during this time period."
                    )
                }
            )

        # Validate if `is_permanent_work_from` is False, `requested_till` must be provided
        if not attrs.get("is_permanent_work_from", False):
            if not requested_till:
                raise serializers.ValidationError(
                    {"requested_till": _("Requested till field is required.")}
                )

        return attrs

    def create(self, validated_data):
        return super().create(validated_data)

    def get_previous_work_from_name(self, instance):
        previous_work_from = instance.previous_work_from_id
        if previous_work_from:
            return previous_work_from.work_from
        else:
            return None  # Return null if previous_work_from_id doesn't exist

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.clean()  # Call clean method before saving the instance
        instance.save()
        return instance


class ShiftRequestSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(
        source="employee_id.employee_first_name", read_only=True
    )
    employee_last_name = serializers.CharField(
        source="employee_id.employee_last_name", read_only=True
    )
    shift_name = serializers.SerializerMethodField(read_only=True)
    previous_shift_name = serializers.SerializerMethodField(read_only=True)

    def get_previous_shift_name(self, instance):
        previous_shift_id = instance.previous_shift_id
        if previous_shift_id:
            return previous_shift_id.employee_shift
        else:
            return None  # Re

    def get_shift_name(self, instance):
        shift_id = instance.shift_id
        if shift_id:
            return shift_id.employee_shift
        else:
            return None  # Re

    def validate(self, attrs):
        # Create an instance of the model with the provided data
        instance = ShiftRequest(**attrs)

        # Call the model's clean method for validation
        try:
            instance.clean()
        except DjangoValidationError as e:
            # Raise DRF's ValidationError with the same message
            raise serializers.ValidationError(get_error_detail(e))

        return attrs

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.clean()  # Call clean method before saving the instance
        instance.save()
        return instance

    class Meta:
        model = ShiftRequest
        fields = "__all__"
        read_only_fields = (
            "approved",
            "canceled",
            "shift_changed",
            "reallocate_approved",
            "reallocate_canceled",
        )
