from django.shortcuts import render, get_object_or_404
from .models import Attraction, Profile, User
import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
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

# Home page view
def home(request):
    return render(request, 'home.html')


# This section is for the suggesting attractions view
def suggest(request):
    return render(request, 'suggest.html')


def user_dashboard(request):
    return render(request, 'auth/user_dashboard.html')


# search functionality (This acts as the filter logic)
def search_attractions(request):
    query = request.GET.get('search_query','')
    if query:
        results = Attraction.objects.filter(name__icontains=query) | Attraction.objects.filter(description__icontains=query) | Attraction.objects.filter(tags__icontains=query)
    else:
        results = Attraction.objects.none()
    return render(request,'search_attractions.html',{'results':results})






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
