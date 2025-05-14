from PIL import Image, ImageDraw
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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

            # Resize for Square Post (1:1)
            if img.width == img.height:
                img = img.resize((1080, 1080), Image.ANTIALIAS)

            # Resize for Landscape Post (1.91:1)
            elif img.width / img.height > 1.91:
                img = img.resize((1200, 630), Image.ANTIALIAS)

            # Resize for Stories / Reels (9:16)
            elif img.height / img.width > 1.78:
                img = img.resize((1080, 1920), Image.ANTIALIAS)

            # Save the resized image
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

            # Resize to 400x400 px
            img = img.resize((400, 400), Image.Resampling.LANCZOS)

            # Circular crop
            mask = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + img.size, fill=255)
            img.putalpha(mask)

            # Save the resized image
            img.save(self.profile_image.path)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()
post_save.connect(create_profile, sender=User)