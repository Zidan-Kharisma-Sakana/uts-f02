from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from news.models import News
from .forms import NewsForm

# Create your views here.
def newshome(request):
    queryset = News.objects.filter(is_approved=True)

    return render(request, 'news.html', {queryset:'queryset'})

@login_required(login_url="/user/login/")
def newsrequest(request):
    
    submitted = False
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('?submitted=True')
    else:
        form = NewsForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'newsreq.html', {'form':form, 'submitted':submitted})
