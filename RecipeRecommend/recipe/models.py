from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shoping_list = models.JSONField(default=list)
    recipeCollections=models.JSONField(default=list)
    # Add other fields as needed

    # Define a method to get personalized recipe collections
    def get_recipe_collections(self):
        return self.recipeCollections.all()

    def __str__(self):
        return self.user.username
    
class Recipe(models.Model):
      image_url = models.URLField(max_length=200)  # Add the image URL field
      title = models.CharField(max_length=200)
      description = models.TextField()
      ingredients = models.JSONField(default=list,blank=True)  
      instructions = models.TextField(blank=True)
      cooking_time = models.PositiveIntegerField()  # In minutes
      servings = models.PositiveIntegerField()
      diet_preference=models.CharField(max_length=50 , default='vegan')

      def __str__(self):
        return self.title
      
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Rating for {self.recipe} by {self.user}"