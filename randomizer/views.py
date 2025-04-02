from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
from .models import NameEntry, Update
from django.contrib.auth.decorators import login_required
from django.db import transaction
import logging
import random

logger = logging.getLogger(__name__)

# Display main page with user names and updates.
def index(request):
    """Display main page with names and updates."""
    name_entries = NameEntry.objects.filter(user=request.user).values('id', 'name')
    updates = Update.objects.all()
    context = {
        'csrf_token': request.COOKIES['csrftoken'],
        'username': request.user.username,
        'names': list(name_entries),
        'updates': updates,
    }
    return render(request, 'randomizer/index.html', context)

# Add a new name to the database.
@login_required
def add_name(request):
    """Add a new name to the database."""
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

# Delete a name from the database.
@login_required
def delete_name(request, name_id):
    """Delete one name from the database."""
    try:
        NameEntry.objects.filter(id=name_id, user=request.user).delete()
        names = list(NameEntry.objects.filter(user=request.user).values())
        return JsonResponse({'success': True, 'names': names})
    except Exception as e:
        logger.error(f"Error deleting name: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# Delete multiple names from the database.
@login_required
def delete_selected_names(request):
    """Delete multiple names based on provided IDs."""
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
        return JsonResponse({'success': False, 'message': 'No IDs provided'}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

# Clear all names for the current user.
@login_required
def clear_names(request):
    """Remove all names for the current user."""
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

# Retrieve the list of names for the current user.
@login_required
def get_names(request):
    """Retrieve current user's names."""
    try:
        names = list(NameEntry.objects.filter(user=request.user).values('id', 'name'))
        return JsonResponse({'names': names})
    except Exception as e:
        logger.error(f"Error getting names: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

# Duplicate definitions (if intentional)
# Display main page with names and updates (duplicate).
@login_required
def index(request):
    """Display main page with names and updates (duplicate)."""
    names = NameEntry.objects.filter(user=request.user).values('id', 'name')
    updates = Update.objects.all()
    return render(request, 'randomizer/index.html', {
        'csrf_token': request.COOKIES['csrftoken'],
        'username': request.user.username,
        'names': list(names),
        'updates': updates
    })

# Add a name to the database (duplicate).
@login_required
def add_name(request):
    """Add a name (duplicate)."""
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

# Delete a name (duplicate).
@login_required
def delete_name(request, name_id):
    """Delete one name (duplicate)."""
    try:
        NameEntry.objects.filter(id=name_id, user=request.user).delete()
        names = list(NameEntry.objects.filter(user=request.user).values())
        return JsonResponse({'success': True, 'names': names})
    except Exception as e:
        logger.error(f"Error deleting name: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# Delete multiple names (duplicate).
@login_required
def delete_selected_names(request):
    """Delete selected names (duplicate)."""
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
        return JsonResponse({'success': False, 'message': 'No IDs provided'}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

# Clear all names (duplicate).
@login_required
def clear_names(request):
    """Clear all names (duplicate)."""
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

# Retrieve names (duplicate).
@login_required
def get_names(request):
    """Retrieve names (duplicate)."""
    try:
        names = list(NameEntry.objects.filter(user=request.user).values('id', 'name'))
        return JsonResponse({'names': names})
    except Exception as e:
        logger.error(f"Error getting names: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

# Randomize selected names into cohorts.
@login_required
def randomize_cohort(request):
    """Randomize selected names into cohorts."""
    if request.method == 'POST':
        selected_ids_string = request.POST.get('ids', '')
        cohort_mode = request.POST.get('mode', 'mode1')
        group_size_str = request.POST.get('group_size', None)
        if not selected_ids_string:
            return render(request, 'randomizer/partials/_result.html', {'result': [['No names selected']]})
        selected_id_list = [int(name_id) for name_id in selected_ids_string.split(',') if name_id]
        selected_names = list(NameEntry.objects.filter(id__in=selected_id_list, user=request.user).values_list('name', flat=True))
        random.shuffle(selected_names)
        result = []
        if cohort_mode == 'mode1':
            while len(selected_names) > 1:
                result.append([selected_names.pop(), selected_names.pop()])
            if selected_names:
                result.append([selected_names.pop()])
        elif cohort_mode == 'mode2':
            try:
                group_size = int(group_size_str)
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

# Handle application updates (superuser only).
@login_required
def updates_view(request):
    """Manage updates (accessible only to superusers)."""
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")
    if request.method == 'POST':
        new_text = request.POST.get('update_text', '')
        if new_text:
            Update.objects.create(text=new_text)
    updates = Update.objects.all().order_by('created_at')
    return render(request, 'randomizer/partials/_updates.html', {'updates': updates})
