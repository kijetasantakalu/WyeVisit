from django.contrib import admin
from .models import Attraction, User, Profile, Tag, AttractionTag, ProfileAttraction

# Define admin classes
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'scores', 'created_at', 'updated_at')
    filter_horizontal = ('tags',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'auth_id', 'created_at', 'updated_at')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_name', 'trip_start_date', 'trip_end_date', 'scores', 'created_at', 'updated_at')
    filter_horizontal = ('positive_tags', 'negative_tags')

class AttractionTagAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'tag')
    list_select_related = ('attraction', 'tag')

class ProfileAttractionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'attraction')
    list_select_related = ('profile', 'attraction')

# Register models and admin classes
admin.site.register(Tag, TagAdmin)
admin.site.register(Attraction, AttractionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(AttractionTag, AttractionTagAdmin)
admin.site.register(ProfileAttraction, ProfileAttractionAdmin)
