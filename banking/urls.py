from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # User APIs
    path("api/", include("users.urls")),                                            #api/register - register new user -> Go to users app -> 

    # JWT APIs
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),      #used to authenticate a user and generate two JWT tokens: access token and refresh token"
    path("api/refresh/", TokenRefreshView.as_view(), name="token_refresh"),           #refresh the access token

    path("api/accounts/", include("accounts.urls")),
    path("api/transactions/",include("transactions.urls")),
]