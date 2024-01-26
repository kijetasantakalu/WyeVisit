from django.urls import path
from . import views
from . import utils
from .utils import ResendVerificationEmailView


urlpatterns = [
    path('', views.home, name='home'),
    path('modal/<str:message>', views.modal_view, name='modal_view'),
    path('attractions/', views.attraction_list, name='attraction_list'),
    path('attractions/recommendations', views.recommendations_attractions, name='recommendations_attractions'),
    path('attractions/<int:attraction_id>/', views.attraction_detail, name='attraction_detail'),
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/<int:profile_id>/', views.profile_detail, name='profile_detail'),
    path('profiles/<int:profile_id>/delete/', views.delete_profile, name='delete_profile'),
    path('profiles/<int:profile_id>/edit/', views.edit_profile, name='edit_profile'),
    path('new_profile/',views.new_profile,name='new_profile'),    
    path('create_profile/', views.create_profile, name='create_profile'),
    path('set_current_profile/<int:profile_id>/', views.set_current_profile, name='set_current_profile'),
    path('wishlist/add/<int:attraction_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:attraction_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/view/', views.view_wishlist, name='view_wishlist'),
    path('suggest',views.suggest, name='suggest'),
    # path("", views.index, name="index"),
    # path("auth/login", views.login, name="login"),
    # path("auth/logout", views.logout, name="logout"),
    # path("auth/callback", views.callback, name="callback"),
    path("auth/login", utils.login, name="login"),
    path("auth/logout", utils.logout, name="logout"),
    path("auth/callback", utils.callback, name="callback"),   
    path("auth/user_dashboard", views.user_dashboard, name="user_dashboard"),
    path('auth/resend_verification_email/', ResendVerificationEmailView.as_view(), name='resend_verification_email'),
    path('search/', views.search_attractions, name='search_attractions'),
    path('user/update/', views.update_account, name='update_account'), # name changed from user into account !!
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
