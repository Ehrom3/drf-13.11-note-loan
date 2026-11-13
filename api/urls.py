from django.urls import path
from . import views

urlpatterns = [
    path('reg/',  views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('refresh/', views.refresh_view, name='token_refresh'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_noteloan_view, name='create_noteloan'),
    path('detail/<int:id>/', views.deteil_update_view, name='detail_update'),
]
 
