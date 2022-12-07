from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import RegisterView

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('registration', RegisterView.as_view(), name='registration'),
    path('profile', views.Profile.as_view(), name='profile'),
    path('profile/<int:pk>/delete',  views.ProfileDelete.as_view(), name='profile_delete'),
    path('profile/<int:pk>/update', views.ProfileUpdate.as_view(), name='profile_update'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]