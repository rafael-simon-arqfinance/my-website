from django.shortcuts import render


def home(request):
    return render(request, 'core/home.html')


def page2(request):
    return render(request, 'core/page2.html')


def page3(request):
    return render(request, 'core/page3.html')
