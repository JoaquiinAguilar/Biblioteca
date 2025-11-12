from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from .models import Cubicle, Student, Career, RentalLog
from .forms import RentalForm, CubicleForm
from django.utils import timezone
from django.db.models import Count, Sum
from django.http import HttpResponse
import csv
from django.core.management import call_command
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

def is_staff_check(user):
    return user.is_authenticated and user.is_staff

@login_required
def dashboard(request):
    cubicles = Cubicle.objects.all().order_by('name')
    user_active_rental = None
    if not request.user.is_staff: # Only check for non-staff users
        user_active_rental = RentalLog.objects.filter(student__control_number=request.user.username, is_active=True).first()
    
    # Fetch active rental for each cubicle
    for cubicle in cubicles:
        cubicle.active_rental = RentalLog.objects.filter(cubicle=cubicle, is_active=True).first()

    return render(request, 'rentals/dashboard.html', {'cubicles': cubicles, 'user_active_rental': user_active_rental})

@login_required
def rent_cubicle(request, cubicle_id):
    cubicle = get_object_or_404(Cubicle, id=cubicle_id)
    
    initial_data = {}
    if request.method == 'GET':
        search_control_number = request.GET.get('control_number')
        if search_control_number:
            try:
                student = Student.objects.get(control_number=search_control_number)
                initial_data = {
                    'control_number': student.control_number,
                    'full_name': student.full_name,
                    'career': student.career # Pass the Career object directly
                }
            except Student.DoesNotExist:
                pass # Student not found, form will be empty

    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            control_number = form.cleaned_data['control_number']
            full_name = form.cleaned_data['full_name']
            career = form.cleaned_data['career'] # This is now a Career object
            requested_duration = form.cleaned_data['requested_duration']

            # No need to get_or_create career, it's already an object
            student, created = Student.objects.get_or_create(
                control_number=control_number,
                defaults={'full_name': full_name, 'career': career}
            )

            # Always update full_name and career, even if student existed
            student.full_name = full_name
            student.career = career
            student.save() # Save all changes

            cubicle.status = 'ocupado'
            cubicle.save()

            rental_log = RentalLog.objects.create(
                student=student,
                cubicle=cubicle,
                rented_by=request.user,
                requested_duration=requested_duration
            )

            return redirect('dashboard')
    else:
        form = RentalForm(initial=initial_data)

    return render(request, 'rentals/rent_cubicle.html', {'form': form, 'cubicle': cubicle})

@login_required
def reports(request):
    cubicle_usage = RentalLog.objects.values('cubicle__name').annotate(
        rental_count=Count('id'),
        total_duration=Sum('requested_duration')
    ).order_by('-rental_count')

    career_usage = RentalLog.objects.values('student__career__name').annotate(
        rental_count=Count('id'),
        total_duration=Sum('requested_duration')
    ).order_by('-rental_count')

    if 'export' in request.GET:
        report_type = request.GET.get('report')
        response = HttpResponse(content_type='text/csv')
        writer = csv.writer(response)

        if report_type == 'cubicle':
            response['Content-Disposition'] = 'attachment; filename="cubicle_usage.csv"'
            writer.writerow(['Cubículo', 'Total de Rentas', 'Duración Total (min)'])
            for row in cubicle_usage:
                writer.writerow([row['cubicle__name'], row['rental_count'], row['total_duration']])
        elif report_type == 'career':
            response['Content-Disposition'] = 'attachment; filename="career_usage.csv"'
            writer.writerow(['Carrera', 'Total de Rentas', 'Duración Total (min)'])
            for row in career_usage:
                writer.writerow([row['student__career__name'], row['rental_count'], row['total_duration']])
        
        return response

    return render(request, 'rentals/reports.html', {
        'cubicle_usage': cubicle_usage,
        'career_usage': career_usage
    })

@login_required
@user_passes_test(is_staff_check)
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        upload_type = request.POST.get('upload_type')
        
        try:
            if upload_type == 'students':
                call_command('import_students', file_path)
            elif upload_type == 'cubicles':
                call_command('import_cubicles', file_path)
        finally:
            fs.delete(filename)
            
        return redirect('dashboard')
        
    return render(request, 'rentals/upload_csv.html')

@user_passes_test(is_staff_check)
def cubicle_list_admin(request):
    cubicles = Cubicle.objects.all().order_by('name')
    for cubicle in cubicles:
        cubicle.active_rental = RentalLog.objects.filter(cubicle=cubicle, is_active=True).first()
    return render(request, 'rentals/cubicle_list_admin.html', {'cubicles': cubicles})

@user_passes_test(is_staff_check)
def cubicle_create(request):
    if request.method == 'POST':
        form = CubicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cubicle_list_admin')
    else:
        form = CubicleForm()
    return render(request, 'rentals/cubicle_form.html', {'form': form})

@user_passes_test(is_staff_check)
def cubicle_update(request, pk):
    cubicle = get_object_or_404(Cubicle, pk=pk)
    if request.method == 'POST':
        form = CubicleForm(request.POST, instance=cubicle)
        if form.is_valid():
            form.save()
            return redirect('cubicle_list_admin')
    else:
        form = CubicleForm(instance=cubicle)
    return render(request, 'rentals/cubicle_form.html', {'form': form, 'object': cubicle})

@user_passes_test(is_staff_check)
def cubicle_delete(request, pk):
    cubicle = get_object_or_404(Cubicle, pk=pk)
    if request.method == 'POST':
        cubicle.delete()
        return redirect('cubicle_list_admin')
    return render(request, 'rentals/cubicle_confirm_delete.html', {'object': cubicle})

@login_required
@user_passes_test(is_staff_check)
def force_release_cubicle(request, pk):
    cubicle = get_object_or_404(Cubicle, pk=pk)
    active_rental = RentalLog.objects.filter(cubicle=cubicle, is_active=True).first()

    if active_rental:
        cubicle.status = 'disponible'
        cubicle.save()

        active_rental.is_active = False
        active_rental.actual_end_time = timezone.now()
        active_rental.save()
    else:
        # If no active rental, just ensure cubicle is available
        cubicle.status = 'disponible'
        cubicle.save()

    return redirect('cubicle_list_admin')



@login_required
def release_my_cubicle(request, rental_id):
    rental_log = get_object_or_404(RentalLog, id=rental_id, is_active=True)

    # Allow any authenticated user to release any cubicle
    # No permission check needed - all users can release occupied cubicles

    if request.method == 'POST':
        cubicle = rental_log.cubicle
        cubicle.status = 'disponible'
        cubicle.save()

        rental_log.is_active = False
        rental_log.actual_end_time = timezone.now()
        rental_log.save()

        return redirect('dashboard')
    
    return render(request, 'rentals/release_confirm.html', {'rental_log': rental_log})

from django.http import JsonResponse
from django.db.models import Q

@login_required
def search_student_ajax(request):
    query = request.GET.get('query', '')
    students = Student.objects.filter(
        Q(control_number__icontains=query) | Q(full_name__icontains=query)
    ).values('control_number', 'full_name', 'career__name', 'career__id')[:5] # Limit to 5 results

    results = []
    for student in students:
        results.append({
            'control_number': student['control_number'],
            'full_name': student['full_name'],
            'career': student['career__name'] if student['career__name'] else 'N/A',
            'career_id': student['career__id'] if student['career__id'] else ''
        })
    return JsonResponse(results, safe=False)

@login_required
def cubicle_detail(request, pk):
    cubicle = get_object_or_404(Cubicle, pk=pk)
    active_rental = RentalLog.objects.filter(cubicle=cubicle, is_active=True).first()

    context = {
        'cubicle': cubicle,
        'active_rental': active_rental,
    }
    return render(request, 'rentals/cubicle_detail.html', context)