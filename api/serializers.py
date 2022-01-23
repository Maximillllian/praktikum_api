from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Sprint, Module, Theme, Lesson

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class ShortLessonSerializer(serializers.ModelSerializer):
    is_complete = serializers.SerializerMethodField()

    def get_is_complete(self, obj, *args, **kwargs):
        username = self.context['request'].user.username
        if username:
            completed_users = obj.completed_users.all()
            is_complete = any(list(map(lambda user: user.username == username, completed_users)))
            return is_complete
        return False

    class Meta:
        model = Lesson
        exclude = ['text_file', 'text', 'completed_users']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        exclude = ['text_file', 'theme']


class LessonUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['slug', 'completed_users']


class ThemeSerializer(serializers.ModelSerializer):
    lessons = ShortLessonSerializer(many=True)

    class Meta:
        model = Theme
        fields = ['title', 'slug', 'is_last', 'next_theme_first_lesson_slug', 'lessons']


class ModuleSerializer(serializers.ModelSerializer):
    themes = ThemeSerializer(many=True)

    class Meta:
        model = Module
        fields = ['title', 'themes']


class ShortModuleSerializer(serializers.ModelSerializer):
    themes_count = serializers.SerializerMethodField()

    def get_themes_count(self, obj, *args, **kwargs):
        return len(obj.themes.all())

    class Meta:
        model = Module
        fields = ['title', 'slug', 'image', 'order', 'themes_count']


class SprintSerializer(serializers.ModelSerializer):
    modules = ShortModuleSerializer(many=True)
    class Meta:
        model = Sprint
        fields = ['title', 'slug', 'modules']


class CreateSprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ['title']


class CreateModuleSerializer(serializers.ModelSerializer):
    sprint = serializers.SlugRelatedField(
        slug_field='slug', queryset=Sprint.objects.all()
    )

    class Meta:
        model = Module
        fields = ['title', 'sprint']


class CreateThemeSerializer(serializers.ModelSerializer):
    module = serializers.SlugRelatedField(
        slug_field='slug', queryset=Module.objects.all()
    )
    
    class Meta:
        model = Theme
        fields = ['title', 'module']


class CreateLessonSerializer(serializers.ModelSerializer):
    theme = serializers.SlugRelatedField(
        slug_field='slug', queryset=Theme.objects.all()
    )

    class Meta:
        model = Lesson
        fields = ['title', 'order', 'text', 'theme']