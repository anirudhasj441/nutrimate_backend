from authentication import views
from django.urls import path


urlpatterns = [
    path('login', views.LoginUser.as_view()),
    path('signup', views.SignUpUser.as_view()),
    path('get_user', views.GetUser.as_view())
]