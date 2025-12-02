from recipes import views
from django.urls import path


urlpatterns = [
   path('', views.RecipeListView.as_view()),
   path('<int:recipe_id>', views.RecipeListView.as_view()),
]