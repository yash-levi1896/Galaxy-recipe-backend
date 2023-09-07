from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer , RecipeSerializer,RatingSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile , Recipe , Rating
import json , os , openai
from django.http import JsonResponse 
from .middlware import token_auth_required
from django.contrib.auth.models import User 
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.environ.get('OPENAI_API_KEY')


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register_user(request):
    """
    Register a new user.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        user_document = UserProfile(user=user)
        user_document.save()
        
        return Response({'msg':'user registered !'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Log in a user and retrieve a token.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'msg':'Login succesfull','token': token.key,'username':username}, status=status.HTTP_200_OK)
    
    return Response({'msg': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_user_token(request):
    """
    Retrieve the token for the currently authenticated user.
    """
    user = request.user
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)

@csrf_exempt
def create_recipe(request):
    
    if request.method == 'POST':

        # Parse the JSON data from the request body
        data = json.loads(request.body)
        
        # Create a serializer with many=True to handle a list of recipes
        serializer = RecipeSerializer(data=data, many=True)
        
        if serializer.is_valid():
            # Save the recipes to the MongoDB database
            
            serializer.save()
            return JsonResponse({'message': 'Recipes created successfully'}, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)
    
@csrf_exempt
@api_view(['GET'])
def get_recipe(request):
    # Get the diet_preference query parameter from the request
    diet_preference = request.query_params.get('diet_preference', None)

    # Get all Recipe objects from the database
    recipes = Recipe.objects.all()

    # Apply filtering based on diet_preference if it's provided
    if diet_preference is not None:
        recipes = recipes.filter(diet_preference=diet_preference)

    # Serialize the filtered queryset using your RecipeSerializer
    serializer = RecipeSerializer(recipes, many=True)

    # Return the serialized data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])

def get_recipe_detail(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        serializer = RecipeSerializer(recipe)  # Serialize the single recipe
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Recipe.DoesNotExist:
        return Response({'message': 'Recipe not found'}, status=status.HTTP_404_NOT_FOUND)

@ csrf_exempt
def get_ai_suggestion(request):
    if request.method=='POST':
        data = json.loads(request.body)
        
        if 'ingredients_list' in data:
            ingredients=data['ingredients_list']
        else:
            ingredients=""
        if 'not_ingredients_list' in data:
            ingredients_not_required=data['not_ingredients_list']
        else:
            ingredients_not_required=""
        if 'not_ingredients_list' in data:
            diet_prefrence=data['diet']
        else:
            diet_prefrence=""
        
        # placeholder_ingredients=','.join(f'ingredient {i}'for i in range(len(ingredients)))
        # placeholder_not_ingredients=','.join(f'notingredient {i}'for i in range(len(ingredients_not_required)))
        prompt=f"You are a proffessional cook give me the top three recipes which include ingredients {ingredients}. Do not use {ingredients_not_required} (you can suggest some other ingredient on the place of these, specifically mentioned what are the alternative ingredients and what are they alternative of ) and recipe should be {diet_prefrence}. Also give expected cooking time and number of serving can be done. Also give quantity along with ingredients. give one sentence description about dish. Do not give any introduction. or conclusions just give recipe."
        
        response=openai.Completion.create(
              model= "text-davinci-003",
              prompt= prompt,
              max_tokens=1000,
             temperature= 0,
        )
       
        suggestions=response.choices[0].text.strip()

        return JsonResponse({'msg':suggestions})
    

@csrf_exempt
@token_auth_required
def add_favorite(request,recipe_id):
    if request.method == 'POST':
        if request.user is None:
            return JsonResponse({'msg': "Please Login !"})
        else:
            # Use .first() to retrieve a single instance from the QuerySet
            user = UserProfile.objects.filter(user_id=request.user.id).first()

            if user:
                # print(user.user_id)
                if recipe_id in user.recipeCollections:
                    return JsonResponse({'msg':'Already added to favorite'})
                user.recipeCollections.append(recipe_id)
                user.save()

                return JsonResponse({'msg': 'Recipe added to favorite'})
            else:
                return JsonResponse({'msg': 'User not found'})
            
@csrf_exempt
@token_auth_required
def get_favorite(request):
    user = UserProfile.objects.filter(user_id=request.user.id).first()
    favourite=[]
    if user:
        for recipe_id in user.recipeCollections:
            try:
            # Retrieve the recipe by ID
               recipe = Recipe.objects.get(id=recipe_id)  # Replace with your query
        
            # Serialize the recipe using the serializer
               recipe_data = RecipeSerializer(recipe).data
        
            # Append the serialized recipe to the list
               favourite.append(recipe_data)
            except Recipe.DoesNotExist:
            # Handle the case where a recipe with a given ID does not exist
             continue

        return JsonResponse({'msg':favourite})
    

@csrf_exempt
@token_auth_required
def delete_favorite(request, recipeid):
    if request.method == 'DELETE':
        user = UserProfile.objects.filter(user_id=request.user.id).first()

        if user:
            # Create a new list without the specified recipeid
            updated_collections = [id for id in user.recipeCollections if id != recipeid]
            
            # Update the user's recipeCollections with the new list
            user.recipeCollections = updated_collections
            user.save()

            return JsonResponse({'msg': 'Recipe deleted'})
        else:
            return JsonResponse({'msg': 'User not found'})
    else:
        return JsonResponse({'msg': 'Invalid request method'})

@csrf_exempt
@token_auth_required

def add_shoping(request,recipeID):
    if request.method == 'POST':
        if request.user is None:
            return JsonResponse({'msg': "Please Login !"})
        else:
            # Use .first() to retrieve a single instance from the QuerySet
            user = UserProfile.objects.filter(user_id=request.user.id).first()

            if user:
                # print(user.user_id)
                if recipeID in user.shoping_list:
                    return JsonResponse({'msg':'Already added to Shoping List'})
                user.shoping_list.append(recipeID)
                user.save()

                return JsonResponse({'msg': 'Ingredients added to Shoping List'})
            else:
                return JsonResponse({'msg': 'User not found'})
            

@csrf_exempt
@token_auth_required
def get_shoping(request):
    user = UserProfile.objects.filter(user_id=request.user.id).first()
    shoping=[]
    if user:
        for recipe_id in user.shoping_list:
            try:
            # Retrieve the recipe by ID
               recipe = Recipe.objects.get(id=recipe_id)  # Replace with your query
        
            # Serialize the recipe using the serializer
               recipe_data = RecipeSerializer(recipe).data
        
            # Append the serialized recipe to the list
               shoping.append({"ingredients":recipe_data['ingredients']})

            except Recipe.DoesNotExist:
            # Handle the case where a recipe with a given ID does not exist
             continue

        return JsonResponse({'msg':shoping})
    
    return JsonResponse({'msg': 'User not found'}, status=404)

    
@csrf_exempt
@token_auth_required
def delete_ingredient(request,ingredientID):
    if request.method == 'DELETE':
        user = UserProfile.objects.filter(user_id=request.user.id).first()

        if user:
            # Create a new list without the specified recipeid
            updated_shoping = [id for id in user.shoping_list if id != ingredientID]
            
            # Update the user's recipeCollections with the new list
            user.shoping_list = updated_shoping
            user.save()

            return JsonResponse({'msg': 'Ingredients deleted'})
        else:
            return JsonResponse({'msg': 'User not found'})
    else:
        return JsonResponse({'msg': 'Invalid request method'})
    


@csrf_exempt
@token_auth_required
def add_Rating(request,recipeID):
    if request.method=='POST':
        data=json.loads(request.body)
        ans=Rating.objects.filter(user_id=request.user.id).filter(recipe_id=recipeID)

        if not ans.exists():
            data['user']=request.user.id
            data['recipe']=recipeID
        
            serializer = RatingSerializer(data=data)
        
            if serializer.is_valid():
              # Save the recipes to the MongoDB database
            
             serializer.save()
             return JsonResponse({'msg': 'your response recorded sucessfully'}, status=201)
            else:
              return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({'msg':'you already rated this dish'})
        
@csrf_exempt

def get_ratings(request, recipeID):
    rate = Rating.objects.filter(recipe_id=recipeID)
    serializer = RatingSerializer(rate, many=True)

    for rating_data in serializer.data:
        # Get the user ID from the rating data
        user_id = rating_data['user']

        # Fetch the User instance using the user ID
        user = User.objects.get(id=user_id)

        # Add the 'username' key to the rating data
        rating_data['username'] = user.username

    return JsonResponse({'msg': serializer.data})


        







        
        

    

        

         
         
