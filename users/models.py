from django.db import models

class CustomUser(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # 해싱 저장 예정
