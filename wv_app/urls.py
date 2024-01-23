from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('attractions/', views.attraction_list, name='attraction_list'),
    path('attractions/<int:attraction_id>/', views.attraction_detail, name='attraction_detail'),
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/<int:profile_id>/', views.profile_detail, name='profile_detail'),
    path('suggest',views.suggest, name='suggest'),
    # path("", views.index, name="index"),
    path("auth/login", views.login, name="login"),
    path("auth/logout", views.logout, name="logout"),
    path("auth/callback", views.callback, name="callback"),
    path("auth/user_dashboard", views.user_dashboard, name="user_dashboard"),
    path('search/', views.search_attractions, name='search_attractions'),
    path('user/update/', views.update_user, name='update_user'),
]

















# from django.urls import path
# from . import views

# urlpatterns = [
#     path('attractions/', views.show_attractions, name='show_attractions'),
#     path('users/', views.show_users, name='show_users'),
#     path('profiles/', views.show_profiles, name='show_profiles'),
#     path('categories/', views.show_categories, name='show_categories'),
#     path('reviews/', views.show_reviews, name='show_reviews'),
#     path('user_preferences/', views.show_user_preferences, name='show_user_preferences'),
# ]
