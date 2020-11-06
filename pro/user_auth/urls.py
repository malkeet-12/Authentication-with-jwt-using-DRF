from django.urls import path
from django.conf.urls import url
from .views import CreateUserAPIView ,LogoutAllView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .import views
 
urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('login/',views.authenticate_user.as_view()),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAllView.as_view(), name='auth_logout'),
    # path('update/',UserRetrieveUpdateAPIView.as_view())
]