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
    # Optionally, you can pass initial updates as well if needed:
    updates = Update.objects.all()
    return render(request, 'randomizer/index.html', {
        'csrf_token': request.COOKIES['csrftoken'],
        'username': request.user.username,
        'names': list(names),
        'updates': updates  # not used directly because we include _updates.html in the sidebar
    })

@login_required
def add_name(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                name = request.POST.get('name')
                if name:
                    NameEntry.objects.create(name=name, user=request.user)
                    names = NameEntry.objects.filter(user=request.user).values('id', 'name')
                    if request.headers.get('HX-Request'):
                        return render(request, 'randomizer/partials/_name_list.html', {'names': names})
                    return JsonResponse({'success': True, 'names': list(names)})
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
        ids = request.POST.get('ids', '')
        if ids:
            try:
                id_list = ids.split(',')
                NameEntry.objects.filter(id__in=id_list, user=request.user).delete()
                names = NameEntry.objects.filter(user=request.user).values('id', 'name')
                if request.headers.get('HX-Request'):
                    return render(request, 'randomizer/partials/_name_list.html', {'names': names})
                return JsonResponse({'success': True, 'names': list(names)})
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
            if request.headers.get('HX-Request'):
                return render(request, 'randomizer/partials/_name_list.html', {'names': []})
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


   
import random

@login_required
def randomize_cohort(request):
    if request.method == 'POST':
        ids_str = request.POST.get('ids', '')
        mode = request.POST.get('mode', 'mode1')
        group_size = request.POST.get('group_size', None)
        if not ids_str:
            return render(request, 'randomizer/partials/_result.html', {'result': [['No names selected']]})
        id_list = [int(x) for x in ids_str.split(',') if x]
        # Get the names (as strings) from the DB
        selected_names = list(NameEntry.objects.filter(id__in=id_list, user=request.user).values_list('name', flat=True))
        random.shuffle(selected_names)
        result = []
        if mode == 'mode1':  # Pair mode
            while len(selected_names) > 1:
                result.append([selected_names.pop(), selected_names.pop()])
            if selected_names:
                result.append([selected_names.pop()])
        elif mode == 'mode2':
            try:
                group_size = int(group_size)
                if group_size <= 0:
                    raise ValueError("Invalid group size")
            except (ValueError, TypeError):
                return render(request, 'randomizer/partials/_result.html', {'result': [['Invalid group size']]})
            while selected_names:
                result.append(selected_names[:group_size])
                selected_names = selected_names[group_size:]
        else:
            return render(request, 'randomizer/partials/_result.html', {'result': [['Invalid mode']]})
        return render(request, 'randomizer/partials/_result.html', {'result': result})
    return render(request, 'randomizer/partials/_result.html', {'result': [['Invalid request method']]})

from django.http import HttpResponseForbidden
from .models import Update

@login_required
def updates_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")
    if request.method == 'POST':
        new_text = request.POST.get('update_text', '')
        if new_text:
            Update.objects.create(text=new_text)
    updates = Update.objects.all()
    return render(request, 'randomizer/partials/_updates.html', {'updates': updates})