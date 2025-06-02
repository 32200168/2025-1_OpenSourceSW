from django.contrib import admin
from .models import Profile, UserTaste, UserHashtagScore

admin.site.register(Profile)
admin.site.register(UserTaste)
admin.site.register(UserHashtagScore)
