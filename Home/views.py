from django.shortcuts import render
from django.views import View
from django.utils.translation import activate
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'Home/home.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'Home/about.html')


def set_language(request):
    user_language = request.GET.get('language', 'en')
    activate(user_language)
    request.session['django_language'] = user_language
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('home')))