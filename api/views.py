from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from .serializers import UserSerializer, CourseSerializer, ThemeSerializer, LessonSerializer, CreateCourseSerializer, CreateThemeSerializer, CreateLessonSerializer
from .models import Course, Theme, Lesson


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permissions = [permissions.AllowAny]


class CoursesListView(generics.ListAPIView):
    permissions = [permissions.AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


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
        course_slug = self.kwargs['course_slug']
        theme_slug = self.kwargs['theme_slug']
        course = Course.objects.get(slug=course_slug)
        theme = course.themes.get(slug=theme_slug)
        # theme['is_lates'] = True
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


class CreateCourseView(generics.CreateAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = CreateCourseSerializer


class CreateThemeView(generics.CreateAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = CreateThemeSerializer


class CreateLessonView(generics.CreateAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = CreateLessonSerializer