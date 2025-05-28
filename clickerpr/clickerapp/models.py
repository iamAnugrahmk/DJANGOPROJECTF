from PIL import Image, ImageDraw
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
# Create your models here.

class Click(models.Model):
    user = models.ForeignKey(User, related_name="clicks", on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    image = models.ImageField(upload_to='click_images/', blank=True, null=True)
    video = models.FileField(upload_to='click_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked_clicks", blank=True)
    disliked_by = models.ManyToManyField(User, related_name="disliked_clicks", blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            
            if img.width == img.height:
                img = img.resize((1080, 1080), Image.Resampling.LANCZOS)

            
            elif img.width / img.height > 1.91:
                img = img.resize((1200, 630), Image.Resampling.LANCZOS)

           
            elif img.height / img.width > 1.78:
                img = img.resize((1080, 1920), Image.Resampling.LANCZOS)

            # Save the rzed img
            img.save(self.image.path)

    def __str__(self):
        return f"{self.body[:50]}..."

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    follows = models.ManyToManyField("self",
                                     related_name="followed_by",
                                     symmetrical=False,
                                     blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    bio = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img = img.resize(output_size, Image.Resampling.LANCZOS) 
                img.save(self.profile_image.path)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

from .models import Profile

def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'profile_list.html', {'profiles': profiles})