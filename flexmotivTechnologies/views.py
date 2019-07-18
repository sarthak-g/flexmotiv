from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        authenticated = 'Yes'
        return render(request,"index.html",{'authenticated':authenticated})
    else:
        return redirect("/login/")
    return render(request,"index.html")
@login_required
def access(request):
    return render(request, "access.html")
