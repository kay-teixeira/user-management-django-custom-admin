from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from people.views import UserCreate, CustomObtainAuthToken, UserRetrieve
from rest_framework.authtoken.views import obtain_auth_token
from people.views.dashboard import gerencial_dashboard

urlpatterns = [
    #path('', admin.site.urls),
    path('admin/', admin.site.urls),
    path('api/v1/', include('people.urls')),
    path('users/', UserCreate.as_view(), name='user_create'),
    path('users/<int:pk>/', UserRetrieve.as_view(), name='user_retrieve'),
    path("login/", CustomObtainAuthToken.as_view(), name="login"),
    
    #Rotas da Documentação
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    #Rota Dashboard
    path('dashboard/', gerencial_dashboard, name='dashboard'),
]