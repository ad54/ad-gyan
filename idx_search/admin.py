from django.contrib import admin

from .models import IndexItem
# Register your models here.

class IndexItemAdmin(admin.ModelAdmin):
    list_display = ('book_num', 'page_num', 'index_string')
    list_filter = ['book_num','page_num', 'index_string']
    search_fields = ['book_num','index_string']


admin.site.register(IndexItem, IndexItemAdmin)
