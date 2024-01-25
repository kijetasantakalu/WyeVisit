from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Attraction(models.Model):
    # attraction_id = models.AutoField(primary_key=True,editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    # scores = models.IntegerField()
    score_1 = models.IntegerField(blank=True,null=True)
    score_2 = models.IntegerField(blank=True,null=True)
    score_3 = models.IntegerField(blank=True,null=True)
    score_4 = models.IntegerField(blank=True,null=True)
    score_5 = models.IntegerField(blank=True,null=True)
    tags = models.ManyToManyField(Tag, related_name='attractions',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Account(models.Model):
    is_active = models.BooleanField(blank=True,null=True,default=True)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    auth_id = models.CharField(max_length=255) # Identifier from OAuth provider (called user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=255,blank=True,null=True)
    profile_picture = models.CharField(max_length=255,null=True)
    email_notifications = models.BooleanField(blank=True,null=True,default=True)
    # current_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    current_profile = models.ForeignKey('Profile', on_delete=models.SET_NULL, blank=True, null=True, related_name='current_account') # CHECK THIS!!!! so firstly i changed the profile to be a string based foreign key to the profile model (bc of circular dependency or smthn), and then i added the on_delete=models.SET_NULL, blank=True, null=True, because cascade would mean the account would be deleted if the profile is deleted, and i dont want that!!!! :(( 

    def __str__(self):
        return self.username

class Profile(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    profile_name = models.CharField(max_length=255)
    trip_start_date = models.DateTimeField()
    trip_end_date = models.DateTimeField()
    # scores = models.IntegerField()
    score_1 = models.IntegerField(blank=True,null=True)
    score_2 = models.IntegerField(blank=True,null=True)
    score_3 = models.IntegerField(blank=True,null=True)
    score_4 = models.IntegerField(blank=True,null=True)
    score_5 = models.IntegerField(blank=True,null=True)
    positive_tags = models.ManyToManyField(Tag, related_name='positive_profiles',blank=True)
    negative_tags = models.ManyToManyField(Tag, related_name='negative_profiles',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    wishlist = models.ManyToManyField(Attraction, related_name='wishlisted_by', blank=True)


    def __str__(self):
        return self.profile_name

class AttractionTag(models.Model):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('attraction', 'tag')

class ProfileAttraction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('profile', 'attraction')