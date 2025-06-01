from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),       # 메인 앱을 루트로 연결
    path('users/', include('users.urls')),  # 다른 앱(users)이 있다면 유지
    path('users/api/', include('users.urls')),  # ✅ 이 줄 추가!!
]
