"""todoapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

# # /importing tasks(application) views
from tasks import views

# /importing crm(application) views
from crm import views as crm_views

# for images
from django.conf import settings
from django.conf.urls.static import static

# api views
from crmapi import views as api_views
from rest_framework.routers import DefaultRouter

# for token generation
from rest_framework.authtoken.views import ObtainAuthToken

# for todoapi
from todoapi import views as todo_views



router=DefaultRouter() 
# for crmapi
router.register("api/employees",api_views.EmployeesView,basename="employees")
router.register("api/v1/employees",api_views.EmployeeViewsetView,basename="memployees") #url for ModelViewSet
# for todoapi
router.register("api/users",todo_views.UsersView,basename="users") 
router.register("api/todos",todo_views.TodosView,basename="todos")


urlpatterns = [
    path('admin/', admin.site.urls),
    # todo views
    path('todos/add/',views.TodoCreateView.as_view(),name="todo-add"),
    path('todos/all/',views.TodoListView.as_view(),name='todo-list'),
    path('todos/<int:pk>',views.TodoDetailView.as_view(),name="todo-detail"), #<int:pk> the id used in update,detail,delete
    path('todos/<int:pk>/remove/',views.TodoDeleteView.as_view(),name='todo-delete'),
    path('todos/<int:pk>/change/',views.TaskEditView.as_view(),name="todo-edit"),
    path('todos/all/finished/',views.TodoCompletedView.as_view(),name='todo-completed'),
    # crm_views
    path('employees/add/',crm_views.EmployeeCreateView.as_view(),name="emp-add"),
    path('employees/all/',crm_views.EmployeeListView.as_view(),name='emp-list'),
    path("employees/<int:pk>",crm_views.EmployeeDetailView.as_view(),name="emp-detail"),
    path('employees/<int:pk>/remove/',crm_views.EmployeeDeleteView.as_view(),name="emp-delete"),
    path("employees/<int:pk>/change/",crm_views.EmployeeEditView.as_view(),name="emp-edit"),
    #registration form
    path("register/",crm_views.SignUpView.as_view(),name="register"),
    path("login/",crm_views.SignInView.as_view(),name="signin"),
    path("logout/",crm_views.signout_view,name="signout"),
    path("api/token/",ObtainAuthToken.as_view())

]  + router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
