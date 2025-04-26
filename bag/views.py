from django.shortcuts import render

# Create your views here.

def bag_view(request):
    
    return render(request,'bag/bag.html')