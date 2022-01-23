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

get_urlpatterns = [
    path('sprints/', views.SprintListView.as_view(), name='sprints_list'),
    path('sprint/<slug:sprint_slug>', views.SprintView.as_view(), name="sprint"),
    path('modules/', views.ModulesListView.as_view(), name='modules_list'),
    path('module/<slug:module_slug>', views.ModuleView.as_view(), name='module'),
    path('theme/<slug:theme_slug>', views.ThemeView.as_view(), name='theme'),
    path('lesson/<slug:lesson_slug>', views.LessonView.as_view(), name='lesson'),
    path('lesson/<slug:lesson_slug>/theme', views.LessonThemeView.as_view(), name='theme'),

    path('module/<slug:module_slug>/themes/', views.ThemesListView.as_view(), name='themes_list'),
    path('module/<slug:module_slug>/theme/<slug:theme_slug>/', views.ThemeView.as_view(), name='theme'),
    path('module/<slug:module_slug>/theme/<slug:theme_slug>/lessons', views.LessonsListView.as_view(), name='lessons_list'),
]

create_urlpatterns = [
    path('create/sprint', views.CreateSprintView.as_view(), name='create_sprint'),
    path('create/module', views.CreateModuleView.as_view(), name='create_module'),
    path('create/theme', views.CreateThemeView.as_view(), name='create_theme'),
    path('create/lesson', views.CreateLessonView.as_view(), name='create_lesson'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(auth_urlpatterns)),
    path('', include(get_urlpatterns)),
    path('', include(create_urlpatterns)),

    path('complete/lesson/<slug:lesson_slug>/', views.CompleteLessonView.as_view(), name='complete_lesson'),
    
]

