from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (
    dashboard, rent_cubicle, reports, upload_csv,
    cubicle_list_admin, cubicle_create, cubicle_update, cubicle_delete, force_release_cubicle,
    release_my_cubicle, search_student_ajax, cubicle_detail
)

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('', dashboard, name='dashboard'),
    path('rent/<int:cubicle_id>/', rent_cubicle, name='rent_cubicle'),
    path('reports/', reports, name='reports'),
    path('upload/', upload_csv, name='upload_csv'),

    # Admin Cubicle Management URLs
    path('management/cubicles/', cubicle_list_admin, name='cubicle_list_admin'),
    path('management/cubicles/add/', cubicle_create, name='cubicle_create'),
    path('management/cubicles/<int:pk>/edit/', cubicle_update, name='cubicle_update'),
    path('management/cubicles/<int:pk>/delete/', cubicle_delete, name='cubicle_delete'),
    path('management/cubicles/<int:pk>/release/', force_release_cubicle, name='force_release_cubicle'),

    # Client Rental Management URLs
    path('my-rentals/<int:rental_id>/release/', release_my_cubicle, name='release_my_cubicle'),
    path('ajax/search-student/', search_student_ajax, name='search_student_ajax'),
    path('cubicles/<int:pk>/', cubicle_detail, name='cubicle_detail'),
]
