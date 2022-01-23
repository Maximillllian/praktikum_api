from django.contrib.auth.models import User, Group
from django.db.models import query
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import LessonUsersSerializer, UserSerializer, SprintSerializer, ModuleSerializer, ThemeSerializer, LessonSerializer, CreateSprintSerializer, CreateModuleSerializer, CreateThemeSerializer, CreateLessonSerializer
from .models import Sprint, Module, Theme, Lesson


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permissions = [permissions.AllowAny]


class SprintListView(generics.ListAPIView):
    permissions = [permissions.AllowAny]
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer


class SprintView(generics.RetrieveAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = SprintSerializer

    def get_object(self, *args, **kwargs):
        sprint_slug = self.kwargs['sprint_slug']
        sprint = Sprint.objects.get(slug=sprint_slug)
        return sprint


class ModulesListView(generics.ListAPIView):
    permissions = [permissions.AllowAny]
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class ModuleView(generics.RetrieveAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = ModuleSerializer

    def get_object(self, *args, **kwargs):
        module_slug = self.kwargs['module_slug']
        module = Module.objects.get(slug=module_slug)
        return module


class ThemesListView(generics.ListAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = ThemeSerializer

    def get_queryset(self, *args, **kwargs):
        module_slug = self.kwargs['module_slug']
        module = Module.objects.get(slug=module_slug)
        return module.themes.all()


class ThemeView(generics.RetrieveAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = ThemeSerializer

    def get_object(self, *args, **kwargs):
        theme_slug = self.kwargs['theme_slug']
        theme = Theme.objects.get(slug=theme_slug)
        return theme


class LessonsListView(generics.ListAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = LessonSerializer

    def get_queryset(self, *args, **kwargs):
        module_slug = self.kwargs['module_slug']
        theme_slug = self.kwargs['theme_slug']
        module = Module.objects.get(slug=module_slug)
        theme = module.themes.get(slug=theme_slug)
        return theme.lessons.all()


class LessonView(generics.RetrieveAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = LessonSerializer

    def get_object(self, *args, **kwargs):
        lesson_slug = self.kwargs['lesson_slug']
        lesson = Lesson.objects.get(slug=lesson_slug)
        return lesson


class CompleteLessonView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonUsersSerializer
    permissions = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        lesson_slug = self.kwargs['lesson_slug']
        lesson = Lesson.objects.get(slug=lesson_slug)
        return lesson

    def update(self, *args, **kwargs):
        lesson = self.get_object()
        user = self.request.user
        if user.username:
            lesson.completed_users.add(user)
            lesson.save()

            return Response({"message": "Success updated"})


class LessonThemeView(generics.RetrieveAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = ThemeSerializer

    def get_object(self, *args, **kwargs):
        lesson_slug = self.kwargs['lesson_slug']
        lesson = Lesson.objects.get(slug=lesson_slug)
        return lesson.theme



class CreateSprintView(generics.CreateAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = CreateSprintSerializer


class CreateModuleView(generics.CreateAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = CreateModuleSerializer


class CreateThemeView(generics.CreateAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = CreateThemeSerializer


class CreateLessonView(generics.CreateAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = CreateLessonSerializer