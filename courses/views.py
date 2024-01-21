from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

def index(request):
    return render(request,template_name='index.html', context={'name':'Truuong Son'})


def welcome(request, year):
    return

def welcome2(request, year):
    return HttpResponse("Hello" + str(year))

class TestView(View):
    def get(self, request):
        return HttpResponse("Hello Get")

    def post(self, request):
        return HttpResponse("Hello Post")