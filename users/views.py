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
            # 로그인 실패 시 오류 메시지 전달
            return render(request, "users/login.html", {
                'error': "등록된 사용자가 없거나 비밀번호가 틀렸습니다."
            })

    return render(request, "users/login.html")


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'users/signup.html', {'error': '이미 존재하는 사용자명입니다.'})

        User.objects.create_user(username=username, password=password)
        return redirect('/users/taste/')

    return render(request, 'users/signup.html')



def taste_view(request):
    if request.method == "POST":
        tags = request.POST.getlist("hashtags")
        print("선택된 태그:", tags)  # 로그 확인용
        return redirect("/users/playlist/")
    return render(request, "users/taste.html")


def playlist_view(request):
    if request.method == "POST":
        # 여기에 저장 처리 로직 추가
        # 예: 폼에서 데이터 읽고 DB에 저장

        return redirect("main")  # 저장 후 main 페이지로 이동

    return render(request, "users/playlist.html")