from django.urls import path
from . views import *

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('<int:pk>/', TaskDetailView.as_view(), name='detail'),
    path('create/', CreateTask.as_view(), name='create'),
    path('<int:pk>/edit', EditTask.as_view(), name='edit'),
    path('<int:pk>/delete', DeleteTask.as_view(), name='delete'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]