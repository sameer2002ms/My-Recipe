from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="/login/")
def recipe(request):
    if request.method == "POST":
        data = request.POST

        recipe_img = request.FILES.get('recipe_img')
        recipe_name = data.get('recipe_name')
        recipe_dis = data.get('recipe_dis')

        # print(recipe_img)
        # print(recipe_name)
        # print(recipe_dis)

# here we are saving the data
        recipes.objects.create(
            recipe_name=recipe_name,
            recipe_img=recipe_img,
            recipe_dis=recipe_dis
        )

        return redirect('/recipe/')

    queryset = recipes.objects.all()

# here i am adding the search functionality
    if request.GET.get('search'):
        # filter in recipe name
        queryset = queryset.filter(
            recipe_name__icontains=request.GET.get('search'))
    context = {'recipes': queryset, 'page': 'Recipe'}

    return render(request, 'recipe.html', context)


def Update_recipe(request, id):
    queryset = recipes.objects.get(id=id)

    if request.method == "POST":
        data = request.POST

        recipe_img = request.FILES.get('recipe_img')
        recipe_name = data.get('recipe_name')
        recipe_dis = data.get('recipe_dis')

        queryset.recipe_name = recipe_name
        queryset.recipe_dis = recipe_dis

        if recipe_img:
            queryset.recipe_img = recipe_img

        queryset.save()
        return redirect('/recipe/')

    context = {'recipe': queryset, 'page': 'Update Recipe'}

    return render(request, 'update_recipe.html', context)


def delete_recipe(request, id):
    queryset = recipes.objects.get(id=id)
    queryset.delete()
    return redirect('/recipe/')


# here i have implemenetd the login logic
def login_page(request):
    context = {'page': 'Login Page'}

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if not user.exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/login/')

        else:
            login(request, user)
            return redirect('/recipe/')

    return render(request, 'login.html', context)


# here i am registering the users
def register_page(request):
    context = {'page': 'Register Page'}

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

# here we are checking the unique user
        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, 'Username already exists')
            return redirect('/register/')

# here we are creating the object
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
# here we are saving the password in the form of encryption
        user.set_password(password)
        user.save()

        messages.info(request, 'Account created Successfully')

        return redirect('/register/')

    return render(request, 'register.html', context)


def logout_page(request):

    logout(request)
    return redirect('/login/')
