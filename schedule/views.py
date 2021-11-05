from django.shortcuts import render
from django.core import serializers
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Activity
from .forms import ActivityForm

# Create your views here.
@login_required(login_url='/user/login/')
def schedule(request):
    form = ActivityForm()
    if request.is_ajax() and request.method == 'POST':
        # Get the form data
        form = ActivityForm(request.POST)
        duplicate = False

        # Ensure this form doesn't save duplicate objects
        for instance in Activity.objects.all():
            print(instance.activity + " " + form['activity'].value())
            print(str(instance.start_time)[:5] +" "+ str(form['start_time'].value()))
            print(str(instance.end_time)[:5] +" "+ str(form['end_time'].value()))
            print(str(instance.year) + " " + form['year'].value())
            print(str(instance.month) + " " + form['month'].value())
            print(str(instance.day) + " " + form['day'].value())
            print("---")
            if (instance.activity == form['activity'].value() and str(instance.year) == form['year'].value() and str(instance.month) == form['month'].value() and str(instance.day) == form['day'].value() and str(instance.start_time)[:5] == str(form['start_time'].value()) and str(instance.end_time)[:5] == str(form['end_time'].value())):
                duplicate = True

        # If valid, save the object to database and fetch the object in activity
        if (not duplicate and form.is_valid()):
            activity = form.save()
            # serialize in new activity object in json
            ser_activity = serializers.serialize('json', [activity, ])
            # send to client side
            return JsonResponse({
                'activity': ser_activity
            }, status = 200)
        else:
            # some form errors occured
            return JsonResponse({
                'error': form.errors
            }, status = 400)

    activities = Activity.objects.all()  # Load Activity objects
    dataJSON = serializers.serialize('json', activities)
    response = {'form': form, 'data': dataJSON}
    return render(request, 'schedule.html', response)

@login_required(login_url='/user/login/')
def delete_activity(request):
    if request.is_ajax() and request.method == 'POST':
        id = request.POST.get('sid')
        pi = Activity.objects.get(pk=id)
        pi.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})