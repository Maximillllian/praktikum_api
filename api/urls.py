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
    path('auth/', include(auth_urlpatterns))
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]