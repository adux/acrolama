from django.shortcuts import render

# Create your views here.i

def homeview(request):
    template_name='home.html'
    context={}
    return render(request, template_name, context)
def portview(request):
    tempate_name='single-portfolio2.html'
    context={}
    return render(request,template_name,context)
