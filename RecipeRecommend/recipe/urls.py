from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register_user, name='register-user'),
    path('api/login/', views.login_user, name='login-user'),
    path('api/get-token/', views.get_user_token, name='get-user-token'),
    path('api/add-recipe/', views.create_recipe, name='create-recipe'),
    path('api/get-recipe/' , views.get_recipe , name='get-recipe'),
    path('api/recipe-detail/<int:recipe_id>/', views.get_recipe_detail, name='get-recipe-details'),
    path('api/recipe-recommend/', views.get_ai_suggestion, name='get-recipe-recomm'),
    path('api/add-favorite/<int:recipe_id>/', views.add_favorite, name='add-favorite'),
    path('api/get-favorite/', views.get_favorite, name='get-favorite'),
    path('api/del-favorite/<int:recipeid>/', views.delete_favorite, name='del-favorite'),
    path('api/add-shoping/<int:recipeID>/', views.add_shoping, name='add-shoping'),
    path('api/get-shoping/', views.get_shoping, name='get-shoping'),
    path('api/update-shoping/<int:item_id>/<str:nameIng>', views.update_ingredient_status, name='update-shoping'),
    path('api/del-shoping/<int:ingredientID>/', views.delete_ingredient, name='del-ingredient'),
    path('api/rating/<int:recipeID>/', views.add_Rating, name='rating'),
    path('api/get-rating/<int:recipeID>/', views.get_ratings, name='get-rating'),
]