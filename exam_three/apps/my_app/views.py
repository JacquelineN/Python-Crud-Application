from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
from datetime import datetime
import bcrypt


def index(request):
    return render(request, 'index.html')  # must pass dict if items need to appear on html page, such as options for user to select

def register(request):
    errors = []
    
    if len(request.POST['name']) < 3:
        errors.append("Name must be at least three characters")
        #best used for a certian key field with limitations on characters entered
    if len(request.POST['alias']) < 3:
        errors.append("Alias must be at least three characters")
        #best used for a certian key field with limitations on characters entered
    if len(request.POST['email']) < 3:
        errors.append("Email must be at least three characters")
        #best used for a certian key field with limitations on characters entered
    if len(request.POST['date_of_birth']) < 1:
        errors.append("Date of birth must be be entered")
        #best used for a certian key field with limitations on characters entered
    if len(request.POST['password']) < 8:
        enteredpw = request.POST['password']
        errors.append("Password must be at least eight characters")
        #best used for a certian key field with limitations on characters entered

    if request.POST['password'] != request.POST['password_confirmation']:
        errors.append("Password and Confirm Password do not match.")

    if errors:
        for err in errors:
            messages.error(request, err)
        return redirect('/')
    
    else:
        try:
            User.objects.get(email=request.POST['email'])
            messages.error(request,"User with that email already exists.")
            return redirect('/')
        except User.DoesNotExist:
            salt = bcrypt.gensalt()
            hashpw = bcrypt.hashpw(request.POST['password'].encode(), salt)
            correct_pw = hashpw.decode('UTF-8')
            user = User.objects.create(name=request.POST['name'],\
                                alias=request.POST['alias'], \
                                email=request.POST['email'], \
                                password=correct_pw,\
                                date_of_birth = request.POST['date_of_birth'])
            request.session['user_id'] = user.id  # here we are putting user.id in session and it will remain until logout or redirect and input is given on login

            return redirect('/')

def login(request):
    try:
        user = User.objects.get(email = request.POST['email'])
        # bcrypt.checkpw(given_password, stored_password)
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id # if password is accepted, then assign user.id to session
            print(user.id)
            return redirect('/dashboard')
        else:
            messages.error(request, "Email/Password combination FAILED")
            return redirect('/')
    except User.DoesNotExist:
        messages.error(request, "Email does not exist. Please try again")
        return redirect('/')

def dashboard(request):
    session_id = request.session['user_id']
    user = User.objects.get(id=session_id)
    quotes = Quotes.objects.exclude(favorites__id=session_id)
    favorites = Quotes.objects.filter(favorites__id=session_id)

    context = {
        'user' : user,
        'quotes' : quotes,
        'favorites' : favorites,
    }
    return render(request, 'dashboard.html', context)

def add(request):
    errors = []
    if len(request.POST['author']) < 4:
        errors.append("Author must be greater than three characters")
        #best used for a certian key field with limitations on characters entered
    if len(request.POST['quote']) < 11:
        errors.append("Quote message must be greater than ten characters")
        #best used for a certian key field with limitations on characters entered
    if errors:
        for err in errors:
            messages.error(request, err)
        return redirect('/dashboard')

    else:
        session_id = request.session['user_id']
        user = User.objects.get(id=session_id)
        new_quote = Quotes.objects.create(author=request.POST['author'],\
                                    quote=request.POST['quote'], \
                                    uploaded_by=user,)
        return redirect('/dashboard')


def add_to_favs(request, id):
    session_id = request.session['user_id']
    user = User.objects.get(id=session_id)
    this_quote = Quotes.objects.get(id=id)

    this_quote.favorites.add(user)

    return redirect('/dashboard')

def user(request, id):
    user = User.objects.get(id=id)
    user_posts = Quotes.objects.filter(uploaded_by__id=id)
    count = Quotes.objects.filter(uploaded_by__id=id).count()

    context = {
        'user' : user,
        'user_posts' : user_posts,
        'count' : count,

    }
    return render(request,'quotes.html', context)


def remove_from_favs(request, id):
    session_id = request.session['user_id']
    user = User.objects.get(id=session_id)
    this_quote = Quotes.objects.get(id=id)

    this_quote.favorites.remove(user)

    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')
