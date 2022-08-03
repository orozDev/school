from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .views import *


urlpatterns = [
    path('', main, name='main'),
    path('search/', search_student, name='search_student'),
    path('student/<int:pk>/', item_student, name='item_student'),
    path('student/<int:pk>/delete/', delete_student, name='delete_student'),
    path('student/create/', create_student, name='create_student'),
    path('student/<int:pk>/update/', UpdateStudent.as_view(), name='update_student'),

    path('login/', login_profile, name='login'),
    path('logout/', logout_profile, name='logout'),
    path('register/', register_profile, name='register'),
    path('profile/', profile, name='profile'),

    path('send_message/', send_message, name='send_message'),

    path('reset_password/', PasswordResetView.as_view(), name='reset_pasword'),
    path('reset_password_sent/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('ajax/get_groups_by_school/<int:pk>/', get_groups_by_school),
    path('ajax/create_school/<int:pk>/', create_group),
]   