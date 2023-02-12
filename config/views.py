from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def index(request):
    # messages.success(request, "Successfully logged in!!")
    return render(request, "index.html", {})
