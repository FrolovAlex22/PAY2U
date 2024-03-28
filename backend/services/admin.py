from django.contrib import admin

from .models import Service, Category, Terms, BankCard, Subscription, Comparison

admin.site.empty_value_display = "Не задано"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(Terms)
class TermsAdmin(admin.ModelAdmin):
    pass

@admin.register(BankCard)
class BankCardAdmin(admin.ModelAdmin):
    pass

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass

@admin.register(Comparison)
class ComparisonAdmin(admin.ModelAdmin):
    pass
