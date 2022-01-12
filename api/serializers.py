from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Course, Theme, Lesson

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class ShortLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        exclude = ['text_file', 'text', 'user']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        exclude = ['text_file', 'theme']


class ThemeSerializer(serializers.ModelSerializer):
    lessons = ShortLessonSerializer(many=True)
    class Meta:
        model = Theme
        fields = ['title', 'slug', 'is_last', 'next_theme_first_lesson_slug', 'lessons']


class CourseSerializer(serializers.ModelSerializer):
    themes = ThemeSerializer(many=True)
    class Meta:
        model = Course
        fields = ['title', 'slug', 'image', 'order', 'themes']


class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title']


class CreateThemeSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(
        slug_field='slug',  queryset=Course.objects.all()
    )
    
    class Meta:
        model = Theme
        fields = ['title', 'course']


class CreateLessonSerializer(serializers.ModelSerializer):
    theme = serializers.SlugRelatedField(
        slug_field='slug', queryset=Theme.objects.all()
    )
    
    class Meta:
        model = Lesson
        fields = ['title', 'order', 'text', 'theme']