from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'time_create')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'subject')
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'slug', 'type', 'subject', 'time_create')
    readonly_fields = ('author','type', 'time_create')
    save_on_top = True

class WorktypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

class StudentsAdmin(admin.ModelAdmin):
   list_display = ('id', 'aut_username','author', 'students')
   list_display_links = ( 'aut_username','author', 'students')
   fields = ('aut_username','author', 'students')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Worktype, WorktypeAdmin)
admin.site.register(Foreign_Students, StudentsAdmin)

admin.site.site_title = 'Сайттың админ панелі'
admin.site.site_header = 'Сайттың админ панелі'
