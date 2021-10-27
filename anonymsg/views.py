from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View
from django.urls import reverse
from .models import AnonymousMessage
from .forms import AskForm
from user.models import Profile

# Create your views here.
@login_required(login_url="/user/login/")
def home(request):
    if request.user.is_superuser:
        return HttpResponseRedirect("/admin/")
    return HttpResponseRedirect(reverse("anonymous-page"))


@login_required(login_url="/user/login/")
def edit_message(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    data = request.POST
    messages = AnonymousMessage.objects.filter(user=user)
    if not messages:
        return HttpResponseRedirect(reverse("anonymsg"))
    if request.method == "POST":
        user_message = AnonymousMessage.objects.get(
            user=user, anonymous_question=data["anonymous_question"]
        )
        if request.POST["finalize"] == "Save":
            user_message.anonymous_answer = data["anonymous_answer"]
            user_message.save()
            return HttpResponseRedirect(reverse("anonymsg"))
        elif request.POST["finalize"] == "Delete":
            user_message.delete()
            return HttpResponseRedirect(reverse("edit-message"))
    context = {"messages": messages}
    return render(request, "anonymsg/edit-message.html", context)


class MyAnonymousView(LoginRequiredMixin, View):
    def get(self, request):
        user_id = request.user.id  # Get user id from request
        user = User.objects.get(id=user_id)
        messages = AnonymousMessage.objects.filter(user=user)
        context = {"message_user_profile": user.profile, "messages": messages}
        if not messages:  # Jika tidak ada message
            return render(request, "anonymsg/no-message.html", context)
        return render(request, "anonymsg/anonymous-page.html", context)


class OtherAnonymousView(LoginRequiredMixin, View):
    def get(self, request, name):
        user_id = request.user.id  # Get user id from request
        user = User.objects.get(id=user_id)
        if name == user.profile.name:
            return HttpResponseRedirect(reverse("anonymous-page"))
        message_user = Profile.objects.get(name=name).user
        messages = AnonymousMessage.objects.filter(user=message_user)
        context = {
            "other_view": True,
            "messages": messages,
            "message_user_profile": message_user.profile,
        }
        if not messages:  # Jika tidak ada message
            return render(request, "anonymsg/no-message.html", context)
        return render(request, "anonymsg/anonymous-page.html", context)


class AskView(View):
    def get(self, request, name):
        message_user = Profile.objects.get(name=name).user
        context = {
            "message_user_profile": message_user.profile,
        }
        return render(request, "anonymsg/ask-page.html", context)

    def post(self, request, name):
        user_id = request.user.id  # Get user id from request
        user = User.objects.get(id=user_id)
        if name == user.profile.name:
            return HttpResponseRedirect(reverse("anonymous-page"))
        message_user = Profile.objects.get(name=name).user
        updated_request = request.POST.copy()
        updated_request.update({"user": message_user})
        data = updated_request
        form = AskForm(data or None)
        if request.method == "POST" and form.is_valid:
            form.save()
            return HttpResponseRedirect(
                reverse("anonymous-page-other", args=(message_user.profile.name,))
            )
        return render(request, "anonymsg/ask-page.html")
