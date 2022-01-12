from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

auth_urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('rest_registration.api.urls'))
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(auth_urlpatterns)),
    path('courses/', views.CoursesListView.as_view(), name='courses_list'),
    path('theme/<slug:course_slug>', views.CourseView.as_view(), name='course'),
    path('theme/<slug:theme_slug>', views.ThemeView.as_view(), name='theme'),
    path('lesson/<slug:lesson_slug>', views.LessonView.as_view(), name='lesson'),
    path('lesson/<slug:lesson_slug>/theme', views.LessonThemeView.as_view(), name='theme'),
    path('create/course', views.CreateCourseView.as_view(), name='create_course'),
    path('create/theme', views.CreateThemeView.as_view(), name='create_theme'),
    path('create/lesson', views.CreateLessonView.as_view(), name='create_lesson'),
    path('course/<slug:course_slug>/themes/', views.ThemesListView.as_view(), name='themes_list'),
    path('course/<slug:course_slug>/theme/<slug:theme_slug>/', views.ThemeView.as_view(), name='theme'),
    path('course/<slug:course_slug>/theme/<slug:theme_slug>/lessons', views.LessonsListView.as_view(), name='lessons_list'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

