from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import UpdateView
from core.models import GENDERS, School, Student
from django import forms
from django.core.mail import send_mail
from school.settings import EMAIL_HOST_USER
from .forms import LoginForm, StudentForm, RegisterForm, GroupForm


@login_required(login_url='/login')
def main(request):
    return render(request, 'index.html', {'group': request.user.group})


@login_required(login_url='/login')
def search_student(request):
    student_name = request.GET.get('student_name', None)
    if student_name is not None:

        students = Student.objects.filter(name__icontains=student_name, 
                                            group=request.user.group)

        return render(request, 'search.html', {'students': students, 
                                            'student_name': student_name})

    return redirect('/')


@login_required(login_url='/login')
def item_student(request, pk):
    student = Student.objects.get(id=pk)
    if student.group == request.user.group:
        return render(request, 'student/student.html', {'student': student})
    messages.warning(request, f'Ученик "{student.name}" не из вашего класса')
    return redirect('/')


@login_required(login_url='/login')
def delete_student(request, pk):
    student = Student.objects.get(id=pk)
    name = student.name
    if(request.user.group == student.group):
        student.delete()
        messages.success(request, f'Ученик "{name}" успешно удален из списка')
    else:
        messages.warning(request, f'Ученик "{name}" не из вашего класса')
    return redirect('/')


@login_required(login_url='/login')
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid() and request.user.group.id == int(request.POST.get('group', None)):
            instance = form.save()
            messages.success(request, f'Ученик "{instance.name}" успешно добавлен')
            return redirect('/')
        messages.error(request, f'Исправьте ошибки')
        return render(request, 'student/create_student.html', {'form': form})
    form = StudentForm()
    return render(request, 'student/create_student.html', {'form': form})


class UpdateStudent(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    template_name = 'student/edit_student.html'
    context_object_name = 'student'
    form_class = StudentForm
    success_url = '/'
    success_message = ''
    login_url = "/login"
    name = ''

    def form_valid(self, form, **kwargs):
        self.name = self.request.POST.get('name')
        if int(self.request.POST.get('group', None)) == self.request.user.group.id: 
            self.success_message = f'Ученик "{self.name}" успешно отредактирован!'
            return super(UpdateStudent, self).form_valid(form)
        messages.warning(self.request, f'Ученик "{self.name}" не из вашего класса')
        return redirect('/')
    
    def dispatch(self, request, pk, *args, **kwargs):
        student = Student.objects.get(id=pk)
        if student.group == request.user.group:
            return super().dispatch(request, pk, *args, **kwargs)
        messages.warning(self.request, f'Ученик "{student.name}" не из вашего класса')
        return redirect('/')


def login_profile(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                phone_number = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']
                user = authenticate(phone_number=phone_number, password=password)
                if user:
                    login(request, user)
                    path = request.session.get('path', '/')
                    return redirect(path)
            messages.error(request, f'Не существует пользователя или неверный пароль')
        form = LoginForm()
        if request.GET.get('next', None) is not None:
            request.session['path'] = request.GET.get('next')
        return render(request, 'auth/login.html', {'form': form})
    return redirect('/')


def logout_profile(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def register_profile(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.is_staff = True
                instance.is_admin = True
                instance.save()
                login(request, instance)
                messages.success(request, f'Добро пожаловать {instance.name}')
                return redirect('/')
            group_form = GroupForm()
            schools = School.objects.all()
            print(form.errors)
            messages.error(request, f'Исправьте ошибки')
            return render(request, "auth/register.html", {"form": form, 'group_form': group_form, 'schools': schools})    
        form = RegisterForm()
        group_form = GroupForm()
        schools = School.objects.all()
        return render(request, "auth/register.html", {"form": form, 'group_form': group_form, 'schools': schools})
    return redirect('/')


def get_groups_by_school(request, pk):
    school = School.objects.get(id=pk)
    groups = school.groups.filter(teacher=None).values('id', 'title')
    return JsonResponse({'groups': list(groups)})


def create_group(request, pk):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            instance = form.save()
            school = School.objects.get(id=pk)
            school.groups.add(instance)
            school.save()
            return JsonResponse({'is_done': True, 'title': instance.title, 'id': instance.id})
        return JsonResponse({'is_done': False, 'errors': form.errors})
    return redirect('/')


@login_required(login_url='/login')
def profile(request):
    return render(request, 'auth/profile.html', {})


@login_required(login_url='/login')
def send_message(request):
    if request.method == 'POST': 
        subject = f'{request.user.name} - ' + request.POST.get('subject')
        message = request.POST.get('message')
        students = Student.objects.filter(id__in=request.POST.getlist('students'))
        result = send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [student.email for student in students],
            fail_silently=True,
        )
        if result:
            messages.success(request, 'Сообщение успешо отпрвалено!')
            return redirect('/')
        messages.error(request, 'Ошибка отправки')
    students = Student.objects.filter(group=request.user.group)
    return render(request, 'message/send_message.html', {'id': int(request.GET.get('id', '-1')), 'students': students})

# Create your views here.
