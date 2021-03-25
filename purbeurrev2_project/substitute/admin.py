from django.contrib import admin

from .models import Product, Profile


class FavoriteProfilesInLine(admin.TabularInline):
    readonly_fields = ['product']
    model = Profile.favorite.through
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ['brands']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [FavoriteProfilesInLine, ]
