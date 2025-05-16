from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("main")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "users/login.html")

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': '이미 존재하는 사용자명입니다.'})

        User.objects.create_user(username=username, password=password)
        return redirect('/users/taste/')  # 회원가입 후 취향선택 페이지로 이동

    return render(request, 'users/signup.html')


def taste_view(request):
    if request.method == "POST":
        tags = request.POST.getlist("hashtags")
        print("선택된 태그:", tags)  # 로그 확인용
        return redirect("/users/firstPL/")
    return render(request, "users/taste.html")

def playlist_view(request):
    return render(request, "users/playlist.html") # 다음으로 어디로???