from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import NameEntry

def index(request):
    return render(request, 'randomizer/index.html', {'csrf_token': request.COOKIES['csrftoken']})

def add_name(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            NameEntry.objects.create(name=name)
    return JsonResponse({'success': True, 'names': list(NameEntry.objects.values())})

def delete_name(request, name_id):
    NameEntry.objects.filter(id=name_id).delete()
    return JsonResponse({'success': True, 'names': list(NameEntry.objects.values())})

def delete_selected_names(request):
    if request.method == "POST":
        ids = request.POST.get('ids', '').split(',')
        if ids:
            NameEntry.objects.filter(id__in=ids).delete()  # Delete the selected names
            names = list(NameEntry.objects.values())  # Get the remaining names
            return JsonResponse({'success': True, 'names': names})
        else:
            return JsonResponse({'success': False, 'message': 'No IDs provided'}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

def clear_names(request):
    if request.method == "POST":
        try:
            NameEntry.objects.all().delete()  # Delete all names
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def get_names(request):
    return JsonResponse({'names': list(NameEntry.objects.values())})