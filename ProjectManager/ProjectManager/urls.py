"""
URL configuration for ProjectManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from projects.views import admin_dashboard, home, project_detail, quick_logout, signup, custom_login, user_dashboard, mark_project_done, delete_project, edit_project

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('dashboard/', admin_dashboard, name='admin-dashboard'),
    path('project/<int:pk>/', project_detail, name='project-detail'),
    path('project/<int:pk>/done/', mark_project_done, name='mark-project-done'),
    path('project/<int:pk>/delete/', delete_project, name='delete-project'),
    path('project/<int:pk>/edit/', edit_project, name='edit-project'),
    path('logout/', quick_logout, name='quick-logout'),
    path('signup/', signup, name='signup'),
    path('login/', custom_login, name='login'),
    path('user-dashboard/', user_dashboard, name='user-dashboard'),
]
