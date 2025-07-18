from django.urls import path
from .views import register_view, employer_register_view, login_view, home_view, logout_view, employer_home_view, profile_view, employer_profile_view, companies_view,companies_follow_view,companies_unfollow_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('employer-register/', employer_register_view, name='employer_register'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('employer-home/', employer_home_view, name='employer_home'),
    path('profile/', profile_view, name='profile'),
    path('employer/profile/', employer_profile_view, name='employer_profile'),
    path('companies/', companies_view, name='companies'),
    path('companies/<int:company_id>/follow/',companies_follow_view,name='follow'),
    path('companies/<int:company_id>/unfollow/',companies_unfollow_view,name='unfollow'),
]
