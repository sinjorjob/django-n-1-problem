from django.contrib import admin

from .models import Category, Kakeibo

class KakeiboAdmin(admin.ModelAdmin):
    list_display=('pk','date','category','amount','memo')

class CategoryAdmin(admin.ModelAdmin):
    list_display=('pk','category_name')



admin.site.register(Category, CategoryAdmin)
admin.site.register(Kakeibo, KakeiboAdmin)
