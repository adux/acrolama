from django.shortcuts import render

# Create your views here.i

def homeview(request):
    template_name='home.html'
    context={}
    return render(request, template_name, context)
