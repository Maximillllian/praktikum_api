from django.contrib import admin
from .models import Sprint, Module, Theme, Lesson


class ModuleInline(admin.TabularInline):
    model = Module
    fields = ['title', 'image']

class ThemeInline(admin.TabularInline):
    model = Theme
    fields = ['title']
    # readonly_fields = ['title']


class LessonInline(admin.TabularInline):
    model = Lesson
    fields = ['order', 'title', 'webinar_link']
    # readonly_fields = ['order', 'title']


class SprintAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]


class ModuleAdmin(admin.ModelAdmin):
    inlines = [ThemeInline]


class ThemeAdmin(admin.ModelAdmin):
    inlines = [LessonInline]


class LessonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Sprint, SprintAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Lesson, LessonAdmin)