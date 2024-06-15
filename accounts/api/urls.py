from django.urls import path
from accounts.api.views import LoginAPIView , SignUpAPIView, UserListAPIView
from rest_framework_simplejwt.views import TokenRefreshView

app_name="accounts"


urlpatterns = [
    path('login/api/v1', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("signup/api/v1", SignUpAPIView.as_view(), name='sign-up'),
    path('api/v1/users', UserListAPIView.as_view(), name="user-list")
]