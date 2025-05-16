from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import redirect

@login_required
def main_view(request):
    return render(request, 'main/main.html')

def profile_edit(request):
    return render(request, 'main/profile_edit.html')