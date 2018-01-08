from django.shortcuts import render

# Create your views here.

def fest_homeview(request):
    template_name='index.html'
    context={}
    return render(request, template_name,context)
