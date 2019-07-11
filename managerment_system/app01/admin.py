from django.contrib import admin
from app01 import models

# Register your models here.

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['pk','name','url','menu_id']
    list_editable = ['name','url']

class RoleAdmin(admin.ModelAdmin):
    list_display = ['pk','name']

class ClassListAdmin(admin.ModelAdmin):
    list_display = ['course','semester','price']

class Campuses(admin.ModelAdmin):
    list_display = ['name','address']

admin.site.register(models.UserInfo)
admin.site.register(models.Customer)
admin.site.register(models.ConsultRecord)
admin.site.register(models.Role,RoleAdmin)
admin.site.register(models.Permission,PermissionAdmin)
admin.site.register(models.ClassList,ClassListAdmin)
admin.site.register(models.Campuses)
