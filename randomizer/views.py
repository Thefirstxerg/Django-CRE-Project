from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import NameEntry
from django.contrib.auth.decorators import login_required
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

@login_required
def index(request):
    names = NameEntry.objects.filter(user=request.user).values('id', 'name')
    return render(request, 'randomizer/index.html', {
        'csrf_token': request.COOKIES['csrftoken'],
        'username': request.user.username,
        'names': list(names)
    })

@login_required
def add_name(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                name = request.POST.get('name')
                if name:
                    NameEntry.objects.create(name=name, user=request.user)
                    names = list(NameEntry.objects.filter(user=request.user).values('id', 'name'))
                    return JsonResponse({'success': True, 'names': names})
                return JsonResponse({'success': False, 'error': 'Name is required'}, status=400)
        except Exception as e:
            logger.error(f"Error adding name: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@login_required
def delete_name(request, name_id):
    try:
        NameEntry.objects.filter(id=name_id, user=request.user).delete()
        names = list(NameEntry.objects.filter(user=request.user).values())
        return JsonResponse({'success': True, 'names': names})
    except Exception as e:
        logger.error(f"Error deleting name: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def delete_selected_names(request):
    if request.method == "POST":
        ids = request.POST.get('ids', '').split(',')
        if ids:
            try:
                NameEntry.objects.filter(id__in=ids, user=request.user).delete()
                names = list(NameEntry.objects.filter(user=request.user).values())
                return JsonResponse({'success': True, 'names': names})
            except Exception as e:
                logger.error(f"Error deleting selected names: {str(e)}")
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
        else:
            return JsonResponse({'success': False, 'message': 'No IDs provided'}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

@login_required
def clear_names(request):
    if request.method == "POST":
        try:
            NameEntry.objects.filter(user=request.user).delete()
            return JsonResponse({'success': True})
        except Exception as e:
            logger.error(f"Error clearing names: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@login_required
def get_names(request):
    try:
        names = list(NameEntry.objects.filter(user=request.user).values('id', 'name'))
        return JsonResponse({'names': names})
    except Exception as e:
        logger.error(f"Error getting names: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)