from django.contrib import admin

from .models import User

admin.site.empty_value_display = "Не задано"


@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ("username", "phone_number", "balance", "email")
    list_filter = ("username", "email")
    search_fields = ("username",)
