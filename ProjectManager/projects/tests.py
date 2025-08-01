from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from .models import Project
from .views import ProjectForm, PersianUserCreationForm
import json

class ProjectModelTest(TestCase):
    """تست‌های مربوط به مدل Project"""
    
    def setUp(self):
        """تنظیم داده‌های اولیه برای تست‌ها"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.project = Project.objects.create(
            name='پروژه تست',
            description='توضیحات پروژه تست',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            assignee=self.user
        )
    
    def test_project_creation(self):
        """تست ایجاد پروژه"""
        self.assertEqual(self.project.name, 'پروژه تست')
        self.assertEqual(self.project.description, 'توضیحات پروژه تست')
        self.assertEqual(self.project.assignee, self.user)
        self.assertFalse(self.project.is_done)
    
    def test_project_string_representation(self):
        """تست نمایش رشته‌ای پروژه"""
        self.assertEqual(str(self.project), 'پروژه تست')
    
    def test_project_dates(self):
        """تست تاریخ‌های پروژه"""
        self.assertEqual(self.project.start_date, date.today())
        self.assertEqual(self.project.end_date, date.today() + timedelta(days=30))
    
    def test_project_auto_timestamps(self):
        """تست برچسب‌های زمانی خودکار"""
        self.assertIsNotNone(self.project.created_at)
        self.assertIsNotNone(self.project.updated_at)
    
    def test_project_mark_done(self):
        """تست علامت‌گذاری پروژه به عنوان انجام شده"""
        self.project.is_done = True
        self.project.save()
        self.assertTrue(self.project.is_done)

class ProjectFormTest(TestCase):
    """تست‌های مربوط به فرم پروژه"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_project_form_valid_data(self):
        """تست فرم با داده‌های معتبر"""
        form_data = {
            'name': 'پروژه جدید',
            'description': 'توضیحات پروژه جدید',
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=30),
            'assignee': self.user.id
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_project_form_invalid_data(self):
        """تست فرم با داده‌های نامعتبر"""
        form_data = {
            'name': '',  # نام خالی
            'description': 'توضیحات',
            'start_date': 'invalid-date',
            'assignee': self.user.id
        }
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('start_date', form.errors)
    
    def test_project_form_without_end_date(self):
        """تست فرم بدون تاریخ پایان"""
        form_data = {
            'name': 'پروژه بدون تاریخ پایان',
            'description': 'توضیحات',
            'start_date': date.today(),
            'assignee': self.user.id
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())

class UserCreationFormTest(TestCase):
    """تست‌های مربوط به فرم ثبت‌نام کاربر"""
    
    def test_user_creation_form_valid_data(self):
        """تست فرم ثبت‌نام با داده‌های معتبر"""
        form_data = {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = PersianUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_user_creation_form_password_mismatch(self):
        """تست فرم ثبت‌نام با رمزهای عبور متفاوت"""
        form_data = {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'differentpass'
        }
        form = PersianUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_user_creation_form_weak_password(self):
        """تست فرم ثبت‌نام با رمز عبور ضعیف"""
        form_data = {
            'username': 'newuser',
            'password1': '123',
            'password2': '123'
        }
        form = PersianUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

class HomeViewTest(TestCase):
    """تست‌های مربوط به صفحه اصلی"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.project = Project.objects.create(
            name='پروژه تست',
            description='توضیحات پروژه',
            start_date=date.today(),
            assignee=self.user
        )
    
    def test_home_view_returns_200(self):
        """تست بازگشت کد 200 از صفحه اصلی"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_home_view_contains_projects(self):
        """تست وجود پروژه‌ها در صفحه اصلی"""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'پروژه تست')
        self.assertIn('projects', response.context)

class ProjectDetailViewTest(TestCase):
    """تست‌های مربوط به صفحه جزئیات پروژه"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.project = Project.objects.create(
            name='پروژه تست',
            description='توضیحات پروژه',
            start_date=date.today(),
            assignee=self.user
        )
    
    def test_project_detail_view_returns_200(self):
        """تست بازگشت کد 200 از صفحه جزئیات پروژه"""
        response = self.client.get(reverse('project-detail', args=[self.project.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_project_detail_view_contains_project_info(self):
        """تست وجود اطلاعات پروژه در صفحه جزئیات"""
        response = self.client.get(reverse('project-detail', args=[self.project.pk]))
        self.assertContains(response, 'پروژه تست')
        self.assertContains(response, 'توضیحات پروژه')
    
    def test_project_detail_view_404_for_nonexistent_project(self):
        """تست بازگشت 404 برای پروژه غیرموجود"""
        response = self.client.get(reverse('project-detail', args=[999]))
        self.assertEqual(response.status_code, 404)

class AuthenticationTest(TestCase):
    """تست‌های مربوط به احراز هویت"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
    
    def test_signup_view_get(self):
        """تست نمایش فرم ثبت‌نام"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'نام کاربری')
    
    def test_signup_view_post_valid(self):
        """تست ثبت‌نام با داده‌های معتبر"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_view_get(self):
        """تست نمایش فرم ورود"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'نام کاربری')
    
    def test_login_view_post_valid(self):
        """تست ورود با داده‌های معتبر"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_logout_view(self):
        """تست خروج از سیستم"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('quick-logout'))
        self.assertEqual(response.status_code, 302)  # Redirect

class AdminDashboardTest(TestCase):
    """تست‌های مربوط به داشبورد ادمین"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        self.regular_user = User.objects.create_user(
            username='user',
            password='userpass123'
        )
        self.project = Project.objects.create(
            name='پروژه تست',
            description='توضیحات پروژه',
            start_date=date.today(),
            assignee=self.regular_user
        )
    
    def test_admin_dashboard_requires_superuser(self):
        """تست نیاز به دسترسی ادمین برای داشبورد"""
        # تست با کاربر عادی
        self.client.login(username='user', password='userpass123')
        response = self.client.get(reverse('admin-dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # تست با ادمین
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin-dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_dashboard_contains_projects(self):
        """تست وجود پروژه‌ها در داشبورد ادمین"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin-dashboard'))
        self.assertContains(response, 'پروژه تست')
        self.assertIn('projects', response.context)
    
    def test_admin_dashboard_create_project(self):
        """تست ایجاد پروژه از داشبورد ادمین"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(reverse('admin-dashboard'), {
            'name': 'پروژه جدید',
            'description': 'توضیحات پروژه جدید',
            'start_date': date.today(),
            'assignee': self.regular_user.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Project.objects.filter(name='پروژه جدید').exists())

class UserDashboardTest(TestCase):
    """تست‌های مربوط به داشبورد کاربر"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.project = Project.objects.create(
            name='پروژه تست',
            description='توضیحات پروژه',
            start_date=date.today(),
            assignee=self.user
        )
    
    def test_user_dashboard_requires_login(self):
        """تست نیاز به ورود برای داشبورد کاربر"""
        response = self.client.get(reverse('user-dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user-dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_user_dashboard_contains_assigned_projects(self):
        """تست وجود پروژه‌های تخصیص داده شده در داشبورد کاربر"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user-dashboard'))
        self.assertContains(response, 'پروژه تست')
        self.assertIn('projects', response.context)
    
    def test_user_dashboard_redirects_admin_to_admin_dashboard(self):
        """تست هدایت ادمین به داشبورد ادمین"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('user-dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to admin dashboard

class ProjectActionsTest(TestCase):
    """تست‌های مربوط به عملیات پروژه"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        self.project = Project.objects.create(
            name='پروژه تست',
            description='توضیحات پروژه',
            start_date=date.today(),
            assignee=self.user
        )
    
    def test_mark_project_done_requires_login(self):
        """تست نیاز به ورود برای علامت‌گذاری پروژه"""
        response = self.client.post(reverse('mark-project-done', args=[self.project.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_mark_project_done_requires_ownership(self):
        """تست نیاز به مالکیت پروژه برای علامت‌گذاری"""
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.post(reverse('mark-project-done', args=[self.project.pk]))
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_mark_project_done_success(self):
        """تست علامت‌گذاری موفق پروژه"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('mark-project-done', args=[self.project.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # بررسی تغییر وضعیت پروژه
        self.project.refresh_from_db()
        self.assertTrue(self.project.is_done)
    
    def test_delete_project_requires_admin(self):
        """تست نیاز به دسترسی ادمین برای حذف پروژه"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('delete-project', args=[self.project.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(reverse('delete-project', args=[self.project.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_edit_project_requires_admin(self):
        """تست نیاز به دسترسی ادمین برای ویرایش پروژه"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('edit-project', args=[self.project.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('edit-project', args=[self.project.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_edit_project_post_valid(self):
        """تست ویرایش پروژه با داده‌های معتبر"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(reverse('edit-project', args=[self.project.pk]), {
            'name': 'پروژه ویرایش شده',
            'description': 'توضیحات جدید',
            'start_date': date.today(),
            'assignee': self.user.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # بررسی تغییرات پروژه
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'پروژه ویرایش شده')
        self.assertEqual(self.project.description, 'توضیحات جدید')

class URLPatternsTest(TestCase):
    """تست‌های مربوط به الگوهای URL"""
    
    def test_home_url(self):
        """تست URL صفحه اصلی"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_url(self):
        """تست URL صفحه ورود"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_signup_url(self):
        """تست URL صفحه ثبت‌نام"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
    
    def test_logout_url(self):
        """تست URL خروج"""
        response = self.client.get(reverse('quick-logout'))
        self.assertEqual(response.status_code, 302)  # Redirect

class IntegrationTest(TestCase):
    """تست‌های یکپارچگی"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_complete_workflow(self):
        """تست جریان کامل کار"""
        # 1. ورود ادمین
        self.client.login(username='admin', password='adminpass123')
        
        # 2. ایجاد پروژه
        response = self.client.post(reverse('admin-dashboard'), {
            'name': 'پروژه یکپارچگی',
            'description': 'تست جریان کامل',
            'start_date': date.today(),
            'assignee': self.user.id
        })
        self.assertEqual(response.status_code, 302)
        
        # 3. بررسی وجود پروژه
        project = Project.objects.get(name='پروژه یکپارچگی')
        self.assertIsNotNone(project)
        
        # 4. ورود کاربر و بررسی پروژه
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user-dashboard'))
        self.assertContains(response, 'پروژه یکپارچگی')
        
        # 5. علامت‌گذاری پروژه به عنوان انجام شده
        response = self.client.post(reverse('mark-project-done', args=[project.pk]))
        self.assertEqual(response.status_code, 302)
        
        # 6. بررسی تغییر وضعیت
        project.refresh_from_db()
        self.assertTrue(project.is_done)
