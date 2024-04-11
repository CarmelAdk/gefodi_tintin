from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, CompanyStatus

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    search_fields = ('name',)
    list_filter = ('name', 'level',)




class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'role', 'get_role_info')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'role')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Attribution du rôle', {'fields': ('role',)}),
        ('Roles info', {'fields': ('get_role_info',)}),

    )
    readonly_fields = ('get_role_info',)

    def get_role_info(self, obj):
        name = obj.role.name if obj.role else None
        level = obj.role.level if obj.role else None
        id_role = obj.role.id if obj.role else None
        return f"Rôle: {name}, Level: {level}, ID Rôle: {id_role}"

    get_role_info.short_description = 'Role Information'

class CompanyStatusAdmin(admin.ModelAdmin):
    list_display = ('status_name', 'short_name','description')
    search_fields = ('short_name',)
    list_filter = ('status_name', 'short_name', 'description')


admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(CompanyStatus, CompanyStatusAdmin)