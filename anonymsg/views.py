from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import AnonymousMessage
from .forms import AskForm

# Create your views here.
@login_required(login_url="/user/login/")
def anonymous_page(request):
    user_id = request.user.id  # Get user id from request
    user = User.objects.get(id=user_id)  # Get user object from user id
    print(user.profile)
    messages = AnonymousMessage.objects.filter(user=user)
    if not messages:  # Jika tidak ada objek
        return render(request, "anonymsg/no-message.html")
    context = {"profile": user.profile, "messages": messages}
    return render(request, "anonymsg/anonymous-page.html", context)


@login_required(login_url="/user/login/")
def edit_message(request):
    user_id = request.user.id  # Get user id from request
    user = User.objects.get(id=user_id)  # Get user object from user id
    data = (
        request.POST
    )  # data adalah dictionary yang key-valuenya adalah nama input dan isinya
    print(data)

    messages = AnonymousMessage.objects.filter(user=user)

    if not messages:  # Jika tidak ada objek
        return HttpResponseRedirect("/anonymsg")
    if request.method == "POST":  # Akan dijalankan bila methodnya POST
        user_message = AnonymousMessage.objects.get(
            anonymous_question=data["anonymous_question"]
        )  # Mendapatkan profile berdasarkan user
        if request.POST["finalize"] == "Save":
            user_message.anonymous_answer = data[
                "anonymous_answer"
            ]  # Mengset field name dengan data baru
            user_message.save()  # Menyimpan kembali objek profile
            return HttpResponseRedirect("/anonymsg")  # Meredirect
        elif request.POST["finalize"] == "Delete":
            user_message.delete()
            return HttpResponseRedirect("/anonymsg/edit-message")  # Meredirect

    context = {"messages": messages}
    return render(request, "anonymsg/edit-message.html", context)


def ask_page(request):
    user_id = request.user.id  # Get user id from request
    user = User.objects.get(id=user_id)  # Get user object from user id
    updated_request = request.POST.copy()
    updated_request.update({"user": user})
    data = updated_request  # data adalah dictionary yang key-valuenya adalah nama input dan isinya
    print(data)
    form = AskForm(data or None)

    if (
        request.method == "POST" and form.is_valid
    ):  # Akan dijalankan bila methodnya POST
        form.save()
        return HttpResponseRedirect("/anonymsg")  # Meredirect

    # return render(request, "anonymsg/ask-page.html", context)
    return render(request, "anonymsg/ask-page.html")
