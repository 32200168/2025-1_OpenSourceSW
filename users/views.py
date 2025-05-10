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
            return redirect("home")  # 로그인 성공 시 이동할 페이지
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
    if request.method == 'POST':
        tags = request.POST.get('selected_tags', '')
        tag_list = tags.split(',') if tags else [] # 선택한 태그를 리스트로 저장
    return render(request, 'users/taste.html') # 다음에 이동할 페이지