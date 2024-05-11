from django.urls import path
from . import views
# other imports
app_name = 'auth'
urlpatterns = [
    path('register/',views.RegisterView.as_view(),name="register"),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('', views.LoginAPIView.as_view(), name="login")
]
