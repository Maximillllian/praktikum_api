from django.contrib import admin
from .models import Course, Theme, Lesson


class ThemeInline(admin.TabularInline):
    model = Theme
    fields = ['title']
    readonly_fields = ['title']


class LessonInline(admin.TabularInline):
    model = Lesson
    fields = ['order', 'title']
    readonly_fields = ['order', 'title']


class CourseAdmin(admin.ModelAdmin):
    inlines = [ThemeInline]


class ThemeAdmin(admin.ModelAdmin):
    inlines = [LessonInline]


class LessonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Lesson, LessonAdmin)