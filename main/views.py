from django.shortcuts import render


def home(request):
    return render(request, 'main/home.html')

def anonymous_page(request):
    return render(request, 'main/anonymous_page.html')
