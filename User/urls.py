from django.urls import path
from . import views
from .views import CreateUserView, UserListView, UserUpdateView, CreateTokenView

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create-user'),
    path('list/', views.UserListView.as_view(), name='user-list'),
    path('update/', views.UserUpdateView.as_view(), name='update-user'),
    path('delete/', views.UserDeleteView.as_view(), name='user-delete'), # Add path to User/visits
    path('create-token/', CreateTokenView.as_view(), name='create-token'),
]


