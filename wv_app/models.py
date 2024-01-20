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
    scores = models.IntegerField()
    tags = models.ManyToManyField(Tag, related_name='attractions',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    auth_id = models.CharField(max_length=255) # Identifier from OAuth provider
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_name = models.CharField(max_length=255)
    trip_start_date = models.DateTimeField()
    trip_end_date = models.DateTimeField()
    scores = models.IntegerField()
    positive_tags = models.ManyToManyField(Tag, related_name='positive_profiles',blank=True)
    negative_tags = models.ManyToManyField(Tag, related_name='negative_profiles',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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