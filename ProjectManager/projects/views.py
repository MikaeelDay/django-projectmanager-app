from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from django import forms
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'assignee']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'assignee': forms.Select(attrs={'class': 'form-control'}),
        }

class PersianUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        labels = {
            "username": "نام کاربری",
            "password1": "رمز عبور",
            "password2": "تکرار رمز عبور",
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'نام کاربری'
        self.fields['password1'].label = 'رمز عبور'
        self.fields['password2'].label = 'تکرار رمز عبور'
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        for field in self.fields.values():
            field.error_messages = {
                'required': 'این فیلد الزامی است.',
                'invalid': 'مقدار وارد شده معتبر نیست.'
            }

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-dashboard')
    else:
        form = ProjectForm()
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'projects/admin_dashboard.html', {'form': form, 'projects': projects})



def home(request):
    from .models import Project
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'projects': projects})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})


def quick_logout(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin-dashboard')
        else:
            return redirect('user-dashboard')
    if request.method == 'POST':
        form = PersianUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد. اکنون می‌توانید وارد شوید.')
            return redirect('login')
    else:
        form = PersianUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def custom_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin-dashboard')
        else:
            return redirect('user-dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.is_superuser:
                return redirect('admin-dashboard')
            else:
                return redirect('user-dashboard')
    else:
        form = AuthenticationForm()
    
    # Add form-control class to login form fields
    form.fields['username'].widget.attrs.update({'class': 'form-control'})
    form.fields['password'].widget.attrs.update({'class': 'form-control'})
    
    return render(request, 'registration/login.html', {'form': form})


@login_required
def user_dashboard(request):
    if request.user.is_superuser:
        return redirect('admin-dashboard')
    user_projects = request.user.assigned_projects.all().order_by('-created_at')
    return render(request, 'user_dashboard.html', {'projects': user_projects})


@login_required
def mark_project_done(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.assignee != request.user:
        return HttpResponseForbidden('شما اجازه تغییر این پروژه را ندارید.')
    if request.method == 'POST':
        project.is_done = True
        project.save()
        return HttpResponseRedirect(reverse('user-dashboard'))
    return HttpResponseForbidden('درخواست نامعتبر است.')


@user_passes_test(lambda u: u.is_superuser)
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project_name = project.name
        project.delete()
        messages.success(request, f'پروژه "{project_name}" با موفقیت حذف شد.')
        return redirect('admin-dashboard')
    return HttpResponseForbidden('درخواست نامعتبر است.')


@user_passes_test(lambda u: u.is_superuser)
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f'پروژه "{project.name}" با موفقیت ویرایش شد.')
            return redirect('admin-dashboard')
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/edit_project.html', {
        'form': form, 
        'project': project
    })
