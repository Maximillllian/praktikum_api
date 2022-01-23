from django.core import validators
from slugify import slugify
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User


class Sprint(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Sprint, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class Module(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)
    order = models.IntegerField(default=0)
    image = models.FileField(upload_to='pictures/', validators=[FileExtensionValidator(['svg', 'png', 'jpg', 'jpeg'])], blank=True, null=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, related_name='modules', blank=True, null=True)

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.title == 'Вебинары':
            self.image = 'pictures/webinar.svg'
            self.slug += self.sprint.slug
        super(Module, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class Theme(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='themes')

    class Meta:
        ordering = ['title']
    
    def themes_of_module(self):
        themes_of_module = self.module.themes.all()
        return themes_of_module
    
    def current_theme_index(self):
        for num, theme in enumerate(self.themes_of_module()):
            if theme.id == self.id:
                return num

    def is_last(self):
        last_theme = self.themes_of_module().reverse()[0]
        return last_theme.id == self.id
    
    def is_first(self):
        first_theme = self.themes_of_module()[0]
        return first_theme.id == self.id
    
    def next_theme_first_lesson_slug(self):
        if self.is_last():
            return False
        next_theme = self.themes_of_module()[self.current_theme_index() + 1]
        return Lesson.objects.filter(theme=next_theme)[0].slug

    def prev_theme_slug(self):
        if self.is_first():
            return False
        return self.themes_of_module()[self.current_theme_index() - 1].slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Theme, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)
    order = models.IntegerField()
    text_file = models.FileField(upload_to='lessons_files/', blank=True, null=True, validators=[FileExtensionValidator(['txt', 'html'])])
    text = models.TextField(blank=True, null=True)
    webinar_link = models.URLField(blank=True, null=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='lessons')
    completed_users = models.ManyToManyField(User, blank=True, related_name="completed_lessons")

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.text_file:
            content = self.text_file.read().decode('utf-8', errors='ignore')
            self.text = content
        super(Lesson, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
