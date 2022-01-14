from django.contrib.auth.models import User, Group
from django.db.models import query
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from .serializers import UserSerializer, SprintSerializer, CourseSerializer, ThemeSerializer, LessonSerializer, CreateSprintSerializer, CreateCourseSerializer, CreateThemeSerializer, CreateLessonSerializer
from .models import Sprint, Course, Theme, Lesson


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


class CoursesListView(generics.ListAPIView):
    permissions = [permissions.AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseView(generics.RetrieveAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = CourseSerializer

    def get_object(self, *args, **kwargs):
        course_slug = self.kwargs['course_slug']
        course = Course.objects.get(slug=course_slug)
        return course


class ThemesListView(generics.ListAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = ThemeSerializer

    def get_queryset(self, *args, **kwargs):
        course_slug = self.kwargs['course_slug']
        course = Course.objects.get(slug=course_slug)
        return course.themes.all()


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
        course_slug = self.kwargs['course_slug']
        theme_slug = self.kwargs['theme_slug']
        course = Course.objects.get(slug=course_slug)
        theme = course.themes.get(slug=theme_slug)
        return theme.lessons.all()


class LessonView(generics.RetrieveAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = LessonSerializer

    def get_object(self, *args, **kwargs):
        lesson_slug = self.kwargs['lesson_slug']
        lesson = Lesson.objects.get(slug=lesson_slug)
        return lesson


class LessonThemeView(generics.RetrieveAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = ThemeSerializer

    def get_object(self, *args, **kwargs):
        lesson_slug = self.kwargs['lesson_slug']
        lesson = Lesson.objects.get(slug=lesson_slug)
        return lesson.theme
# Create your views here.


class CreateSprintView(generics.CreateAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = CreateSprintSerializer


class CreateCourseView(generics.CreateAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = CreateCourseSerializer


class CreateThemeView(generics.CreateAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = CreateThemeSerializer


class CreateLessonView(generics.CreateAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = CreateLessonSerializer