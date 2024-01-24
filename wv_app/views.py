from django.shortcuts import render, get_object_or_404
from .models import Attraction, Profile, Account
import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from math import sqrt
# from django.contrib.auth import authenticate, login, logout

# View for listing all attractions
def attraction_list(request):
    attractions = Attraction.objects.all()
    return render(request, 'attractions/list.html', {'attractions': attractions})

# Detailed view for a single attraction
def attraction_detail(request, attraction_id):
    attraction = get_object_or_404(Attraction, pk=attraction_id)
    return render(request, 'attractions/detail.html', {'attraction': attraction})

# View for listing all profiles
def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'profiles/list.html', {'profiles': profiles})

# Detailed view for a single profile
def profile_detail(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    return render(request, 'profiles/detail.html', {'profile': profile})

# # Home page view
def home(request):
    return render(request, 'home.html')
# def home(request):
#     return render(request, 'home.html')


# This section is for the suggesting attractions view
def suggest(request):
    return render(request, 'suggest.html')


def user_dashboard(request):
    return render(request, 'auth/user_dashboard.html')

def new_profile(request):
    return render(request, 'profiles/new_profile.html')


# search functionality (This acts as the filter logic)
def search_attractions(request):
    query = request.GET.get('search_query','')
    if query:
        results = Attraction.objects.filter(name__icontains=query) | Attraction.objects.filter(description__icontains=query) | Attraction.objects.filter(tags__name__icontains=query)
    else:
        results = Attraction.objects.none()
    return render(request,'search_attractions.html',{'results':results})


# USERs (NOW CHANGED INTO ACCOUNTS)

def update_account(request):
    if request.method == 'POST':
        account = request.account
        # user_profile = UserProfile.objects.get(user=user)  

        # Update user data
        account.username = request.POST.get('username')
        account.save()

        # # Update profile data
        # user_profile.description = request.POST.get('description')
        user_profile.phone_number = request.POST.get('phoneNumber')  
        # user_profile.location = request.POST.get('location')
        
        # if 'profilePicture' in request.FILES:
        #     user_profile.profile_picture = request.FILES['profilePicture']

        # user_profile.save()

        return redirect('auth/user_dashboard')  

    return render(request, 'auth/user_dashboard.html')

#OAUTH

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)



# Adding oauth context to all requests (context processor)
def oauth_context_processor(request):
    return {
        'session': request.session.get("user")
    }


def account_context_processor(request):
    account = None
    # user_id = request.session.get("user").get('sub')
    try:
        user_id = request.session.get("user").get('userinfo').get('sub')
    except:
        user_id = None
    # print("USERID " + str(user_id))
    if user_id:
        try:
            account = Account.objects.get(auth_id=user_id)
        except Account.DoesNotExist:
            pass
    return {
        'account': account
    }



def calculate_score_distance(user_scores, attraction_scores):
    return sqrt(sum((u - a) ** 2 for u, a in zip(user_scores, attraction_scores))) # euclidean distance (i think)


def get_closest_attractions(profile_id):
    if account == None:
        return
    attractions = Attraction.objects.all()

    profile_scores = [profile.score1, profile.score2, profile.score3, profile.score4, profile.score5]

    scored_attractions = []
    for attraction in attractions:
        attraction_scores = [attraction.score1, attraction.score2, attraction.score3, attraction.score4, attraction.score5]
        distance = calculate_distance(user_scores, attraction_scores)
        scored_attractions.append((attraction, distance))

    # Sort attractions by their distance (ascending)
    closest_attractions = sorted(scored_attractions, key=lambda x: x[1])

    return closest_attractions

def recommend_attractions(request):
    pass
    




def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("home")))

def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("home")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


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
