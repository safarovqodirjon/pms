from django.contrib import admin
from .models import Project, ManagerProject, Task
from authentication.models import CustomUser, RegistrationRequest


class ManagerProjectInline(admin.TabularInline):
    model = ManagerProject
    fields = ['project', 'user']
    extra = 1

    verbose_name = 'Manager'
    verbose_name_plural = 'Managers'

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = CustomUser.objects.filter(is_manager=True, is_employee=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_managers', 'manager_count')
    list_display_links = ('name',)
    search_fields = ('name',)

    def get_managers(self, obj):
        return ', '.join(
            [f"{mp.user.first_name} {mp.user.last_name}" for mp in obj.managerproject_set.all()])

    get_managers.short_description = 'Managers'

    def manager_count(self, obj):
        return obj.managerproject_set.count()

    manager_count.short_description = 'Manager Count'
    inlines = [ManagerProjectInline, ]


# @admin.register(ManagerProject)
# class ManagerProjectAdmin(admin.ModelAdmin):
#     verbose_name = 'Менеджер'
#     verbose_name_plural = 'Менеджеры'
#     list_display = ('id', 'user', 'project', 'first_name',
#                     'last_name', 'email', 'date_joined')
#     list_display_links = ('user', 'project')
#     search_fields = ('user__username', 'project__name',)
#     sortable_by = ('date_joined',)
#     list_filter = (
#         ('user', admin.RelatedOnlyFieldListFilter),
#     )
#
#     def first_name(self, obj):
#         return obj.user.first_name
#
#     first_name.short_description = 'Имя'
#
#     def last_name(self, obj):
#         return obj.user.last_name
#
#     last_name.short_description = 'Фамилия'
#
#     def email(self, obj):
#         return obj.user.email
#
#     email.short_description = 'Email'
#
#     def date_joined(self, obj):
#         return obj.user.date_joined
#
#     date_joined.short_description = 'date_joined'
#
#     def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
#         if db_field.name == "user":
#             kwargs["queryset"] = CustomUser.objects.filter(is_manager=True, is_employee=False)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'project')
    search_fields = ('name', 'project__name',)
    list_filter = (
        ('project', admin.RelatedOnlyFieldListFilter),
    )

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "project":
            kwargs["queryset"] = Project.objects.filter(managers=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request):
        if request.user.is_superuser and request.user.is_manager:
            return True
        elif request.user.is_manager:
            return True
        else:
            return False


# request admin

@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_manager', 'user', 'first_name', 'last_name',
                    'email', 'short_message', 'created_at',
                    'approved',)
    list_display_links = ('id', 'user', 'short_message', 'is_manager')
    list_filter = ('approved', 'created_at')
    search_fields = ('user__username', 'user__email')
    actions = ['approve_requests', 'decline_requests']
    list_editable = ('approved',)

    def first_name(self, obj):
        return obj.user.first_name

    first_name.short_description = 'Имя'

    def last_name(self, obj):
        return obj.user.last_name

    last_name.short_description = 'Фамилия'

    def email(self, obj):
        return obj.user.email

    email.short_description = 'Email'

    def is_manager(self, obj):
        if obj.user.is_manager:
            return 'менеджер'
        else:
            return 'сотрудник'

    is_manager.short_description = 'is_manager'
    is_manager.allow_tags = True

    def short_message(self, obj):
        return obj.message[:50] + "..." if obj.message else ""

    short_message.short_description = 'Message'

    def approve_requests(self, request, queryset):
        queryset.update(approved=True)

    approve_requests.short_description = 'Approve selected requests'

    def decline_requests(self, request, queryset):
        queryset.update(declined=True)

    decline_requests.short_description = 'Decline selected requests'

    def has_add_permission(self, request):
        return False if request.user.is_authenticated else True

    def save_model(self, request, obj, form, change):
        obj.save()
