from django.shortcuts import render

def home(request):
    return render(request, 'randomizer/index.html')  # Replace with your actual HTML file name