from django.shortcuts import render, get_object_or_404
from .models import Attraction, Profile, Account
import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from math import sqrt
from django.contrib import messages
from .decorators import session_required, profile_required
from .utils import account_context_processor
from datetime import datetime
from django.views.decorators.cache import never_cache
from . import utils
# from django.contrib.auth import authenticate, login, logout





# modal view (deprecated)
def modal_view(request, message):
    return render(request, 'modal.html', {'message': message})

# this is a view for listing all attractions (not recommendations nor wishlist, just everything. )
def attraction_list(request):
    attractions = Attraction.objects.all()
    return render(request, 'attractions/list.html', {'attractions': attractions})

# detailed view for a single attraction
def attraction_detail(request, attraction_id):
    attraction = get_object_or_404(Attraction, pk=attraction_id)
    scores = [attraction.score_1, attraction.score_2, attraction.score_3, attraction.score_4, attraction.score_5]
    return render(request, 'attractions/detail.html', {'attraction': attraction, 'scores': scores})

@profile_required
@session_required
def recommendations_attractions(request):
    profile = account_context_processor(request).get('account').current_profile
    recommended_attractions = utils.recommend_attractions(profile.id)
    return render(request, 'attractions/recommendations.html', {'recommended_attractions': recommended_attractions})
#NOTICE THAT THIS IS DIFFERENT FROM utils recommend_attractions (one shows the recommendations and the other processes the logic. )
    

# view for listing all profiles
@session_required
def profile_list(request):
    # profiles = Profile.objects.all()  
    # profiles = account_context_processor(request).get('account').profiles.all() # This line doesnt work b/c accounts don't have profiles. profiles have accounts. this does mean it's less optimized but also less risk of error. 
    profiles = Profile.objects.filter(account=account_context_processor(request).get('account'))
    return render(request, 'profiles/list.html', {'profiles': profiles})

# detailed view for a single profile
@session_required
def profile_detail(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    duration = (profile.trip_end_date - profile.trip_start_date).days
    wishlist = profile.wishlist.all()
    scores = [profile.score_1, profile.score_2, profile.score_3, profile.score_4, profile.score_5]
    if profile.account != account_context_processor(request).get('account'):
        messages.error(request, 'You do not have permission to view this profile.')
        return redirect('profile_detail', profile_id=profile_id)
    
    return render(request, 'profiles/detail.html', {'profile': profile, 'duration': duration, 'wishlist': wishlist, 'scores': scores})


@session_required
def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)

    if profile.account != account_context_processor(request).get('account'):
        messages.error(request, 'You do not have permission to edit this profile.')
        return redirect('profile_detail', profile_id=profile_id)

    
    trip_start_date = request.POST.get('trip_start_date')
    trip_end_date = request.POST.get('trip_end_date')
    nickname = request.POST.get('nickname')
    profile.trip_start_date = trip_start_date
    profile.trip_end_date = trip_end_date
    profile.nickname = nickname
    profile.save()

    messages.success(request, 'Profile updated successfully.')
    return redirect('profile_detail', profile_id=profile_id)




# # Home page view
def home(request):
    return render(request, 'home.html') # note that there isn't any logic here b/c all of it is done in base.html (i.e. the logic for the home page is in base.html)
# def home(request):
#     return render(request, 'home.html')


# This section is for the suggesting attractions view
@session_required
def suggest(request):
    return render(request, 'suggest.html')


@session_required
def user_dashboard(request):
    return render(request, 'auth/user_dashboard.html')

@session_required
def new_profile(request):
    return render(request, 'profiles/new_profile.html')

@session_required
def create_profile(request):
    account = account_context_processor(request).get('account')
    if request.method == 'POST':
        profile = Profile()
        profile.name = request.POST.get('name')
        profile.description = request.POST.get('description')
        profile.score1 = request.POST.get('score1')
        profile.score2 = request.POST.get('score2')
        profile.score3 = request.POST.get('score3')
        profile.score4 = request.POST.get('score4')
        profile.score5 = request.POST.get('score5')
        profile.trip_start_date = request.POST.get('startDate') 
        profile.trip_end_date = request.POST.get('endDate') 
        profile.accommodation = request.POST.get('accommodation') 
        profile.nickname = request.POST.get('nickname')
        profile.account = account
        profile.save()

        account.current_profile = profile
        account.save()

        return redirect(f'/wv_app/profiles/{profile.id}')

    # return render(request, 'profiles/new_profile.html', {'show_modal': True})
    return render(request, 'profiles/new_profile.html')

@never_cache
@profile_required
@session_required
def add_to_wishlist(request, attraction_id):
    attraction = get_object_or_404(Attraction, id=attraction_id)
    # profile = Profile.objects.get(user=request.user)
    profile = account_context_processor(request).get('account').current_profile
    if profile.wishlist.filter(id=attraction.id).exists():
        messages.warning(request, "Already in wishlist.")
        return redirect('attraction_detail', attraction_id=attraction.id)
    profile.wishlist.add(attraction)
    if profile.wishlist.filter(id=attraction.id).exists():
        messages.success(request, "Added to wishlist successfully.")
    else:
        messages.error(request, "Failed to add to wishlist.")    
    return redirect('attraction_detail', attraction_id=attraction.id)
#  CHECK!!!! IVE CHANGED SOMETHING!!! (now each account can have multiple profiles) (i think this is correct) (i hope so)

@never_cache
@profile_required
@session_required
def remove_from_wishlist(request, attraction_id):
    attraction = get_object_or_404(Attraction, id=attraction_id)
    profile = account_context_processor(request).get('account').current_profile
    if not profile.wishlist.filter(id=attraction.id).exists():
        messages.warning(request, "This is not in wishlist.")
    profile.wishlist.remove(attraction)
    if not profile.wishlist.filter(id=attraction.id).exists():
        messages.success(request, "Removed from wishlist successfully.")
    else:
        messages.error(request, "Failed to remove from wishlist.")        
    return redirect('attraction_detail', attraction_id=attraction.id)

@profile_required
@session_required
def view_wishlist(request):
    profile = account_context_processor(request).get('account').current_profile
    attractions = profile.wishlist.all()
    return render(request, 'attractions/list.html', {'attractions': attractions})


# search functionality (This acts as the filter logic)
def search_attractions(request):
    query = request.GET.get('search_query','')
    if query:
        results = Attraction.objects.filter(name__icontains=query) | Attraction.objects.filter(description__icontains=query) | Attraction.objects.filter(tags__name__icontains=query)
    else:
        results = Attraction.objects.none()
    return render(request,'search_attractions.html',{'results':results})


@session_required
def set_current_profile(request, profile_id):
    account = account_context_processor(request).get('account')
    profile = get_object_or_404(Profile, id=profile_id)
    # account.current_profile = Profile.objects.get(id=profile_id)
    if profile.account != account:
        messages.error(request, 'This profile does not belong to you.')
        return redirect('profile_list')
    account.current_profile = profile
    account.save()
    messages.success(request, 'Profile successfully set.')
    return redirect('profile_detail', profile_id=profile_id)


@session_required
def delete_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    
    if profile.account == account_context_processor(request).get('account'):
        profile.delete()
        messages.success(request, 'Profile successfully deleted.')
    else:
        messages.error(request, 'This profile does not belong to you.')
    
    return redirect('profile_list')

# USERs (NOW CHANGED INTO ACCOUNTS)

@session_required
def update_account(request):
    if request.method == 'POST':
        account = request.account
        # user_profile = UserProfile.objects.get(user=user)  

        # Update user data
        account.username = request.POST.get('username')

        # # Update profile data
        # user_profile.description = request.POST.get('description')
        account.phone_number = request.POST.get('phoneNumber')  
        # user_profile.location = request.POST.get('location')
        
        # if 'profilePicture' in request.FILES:
        #     user_profile.profile_picture = request.FILES['profilePicture']

        # user_profile.save()

        account.save()
        messages.success(request, 'Profile successfully set.')
        return redirect('auth/user_dashboard')  

    return render(request, 'auth/user_dashboard.html')
 
# #OAUTH

# oauth = OAuth()

# oauth.register(
#     "auth0",
#     client_id=settings.AUTH0_CLIENT_ID,
#     client_secret=settings.AUTH0_CLIENT_SECRET,
#     client_kwargs={
#         "scope": "openid profile email",
#     },
#     server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
# )




# def login(request):
#     return oauth.auth0.authorize_redirect(
#         request, request.build_absolute_uri(reverse("callback"))
#     )

# def callback(request):
#     token = oauth.auth0.authorize_access_token(request)
#     request.session["user"] = token
#     return redirect(request.build_absolute_uri(reverse("home")))

# def logout(request):
#     request.session.clear()

#     return redirect(
#         f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
#         + urlencode(
#             {
#                 "returnTo": request.build_absolute_uri(reverse("home")),
#                 "client_id": settings.AUTH0_CLIENT_ID,
#             },
#             quote_via=quote_plus,
#         ),
#     )


# LEGACY (IGNORE)
# def index(request):
#     return render(
#         request,
#         "index.html",
#         context={
#             "session": request.session.get("user"),
#             "pretty": json.dumps(request.session.get("user"), indent=4),
#         },
#     )


#IMGUR
