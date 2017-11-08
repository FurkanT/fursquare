from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Venues(models.Model):
    venue_name = models.CharField(max_length=144, unique=True)
    venue_address = models.CharField(max_length=256, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'."
                                         " Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, unique=True)
    comments = models.ForeignKey(Comments, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    venue_type = models.ForeignKey(VenueType, on_delete=models.CASCADE)

    def __str__(self):
        return self.venue_name


class VenueType(models.Model):
    venue_type = models.CharField(max_length=105, unique=True)

    def __str__(self):
        return self.venue_type


class Comments(models.Model):
    title = models.CharField(max_length=124)
    comment = models.CharField(max_length=255)
    commented_by = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],)

    def __str__(self):
        return self.rating


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='images/',
                               blank=True,
                               default='static/images/default-avatar.png')

    def __str__(self):
        return self.user.username + "'s Profile"


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


