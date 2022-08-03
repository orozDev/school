from tkinter import E
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import *


class UserAdminConfig(UserAdmin):
    model = Teacher
    search_fields = ('id', 'name', 'phone_number', 'email', 'group')
    list_display = ('id', 'get_avatar', 'name', 'phone_number', 'email', 'gender', 'last_login')
    list_display_links = ('id', 'name',)
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': (
                'avatar',
                'get_avatar',
                'phone_number',
                'name', 
                'email',
                'gender',
                'group',
                'is_superuser',
                'password',
                'created_at',
                'updated_at',
            )},
         ),
    )
    add_fieldsets = (
        (None, {
            'fields': (
                'avatar',
                'phone_number',
                'name',
                'email',
                'gender',
                'group',
                'password1',
                'password2',
                'is_superuser',
            )}
         ),
    )
    readonly_fields = ('last_login', 'get_avatar', 'created_at', 'updated_at',)


    def get_avatar(self, obj):
        try:
            return mark_safe(f'<img src="{obj.avatar.url}" width="50rem">')
        except Exception:
            return '-'

    get_avatar.short_description = 'Аватарка'


admin.site.register(Teacher, UserAdminConfig)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'birthday', 'group', 'gender', 'address', 'get_photo')
    list_display_links = ('id', 'name',)
    list_filter = ('group', 'gender',)
    search_fields = ('name', 'email', 'address',)
    
    def get_photo(self, obj):
        try:
            return mark_safe(f'<img src="{obj.photo.url}" width="70rem" />')
        except Exception:
            return '-'

    fields = (
        'name',
        'email',
        'birthday',
        'group',
        'address',
        'gender',
        'photo',
        'get_photo',
        'is_active',
        'created_at',
        'updated_at',
    )

    readonly_fields = ('get_photo', 'created_at', 'updated_at', 'is_active',)
    get_photo.short_description = 'Фотография'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'teacher', 'school')
    list_display_links = ('id', 'title',)
    list_filter = ('teacher',)

    def school(self, obj):
        try:
            return obj.set_school.first().title
        except Exception:
            pass
        
    school.short_description = 'Школа'
    


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)

# Register your models here.
