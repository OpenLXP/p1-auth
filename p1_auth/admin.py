from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from p1_auth.models import AttributeCheck, RelatedAssignment

# Register your models here.


class AttributeCheckInline(admin.TabularInline):
    model = AttributeCheck
    fields = ('jwt_attribute', 'expected_value',)


class RelatedAssignmentInline(GenericTabularInline):
    ct_field = 'object_model'
    ct_fk_field = 'object_pk'


@admin.register(AttributeCheck)
class AttributeCheckAdmin(admin.ModelAdmin):
    list_display = ('expected_value', 'assignment')
    fieldsets = (
        ('General', {'fields': ('jwt_attribute', 'expected_value',)}),
        ('Connection', {'fields': ('assignment',)}),
    )


@admin.register(RelatedAssignment)
class RelatedAssignmentAdmin(admin.ModelAdmin):
    list_display = ('foreign_object',)
    fieldsets = (
        ('Assign To', {'fields': ('object_model', 'object_pk',)}),
        # ('Validators', {'fields': ('validators',)}),
    )
    inlines = [AttributeCheckInline]
