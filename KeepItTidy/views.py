from django.shortcuts import render

# Create your views here.

def index(request):
	return render(request, "keepittidy/index.html")


def login(request):
	return render(request, "keepittidy/login.html")


def register(request):
	return render(request, "keepittidy/register.html")