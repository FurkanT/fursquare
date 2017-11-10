from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class Venue(models.Model):
    venue_name = models.CharField(max_length=144, unique=True)
    venue_address = models.CharField(max_length=256, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'."
                                         " Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, unique=True)
    venue_type = models.ForeignKey("VenueType", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User)

    def __str__(self):
        return self.venue_name

    @property
    def get_average_rating(self):
        try:
            rating = Rating.objects.get(venue__id=self.pk).rating
        except ObjectDoesNotExist:
            rating = "No one rated yet"
        except MultipleObjectsReturned:
            rating = int(Rating.objects.filter(venue__id=self.pk).aggregate(Avg('rating'))['rating__avg'])
        return str(rating)

    @property
    def get_venue_vote_count(self):
        vote_count = Rating.objects.filter(venue__id=self.pk).count()
        return vote_count

    @property
    def get_venue_ratings(self):
        ratings = Rating.objects.filter(venue__id=self.pk)
        return ratings


class VenueType(models.Model):
    venue_type = models.CharField(max_length=105, unique=True)
    created_by = models.ForeignKey(User)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.venue_type


class Comment(models.Model):
    title = models.CharField(max_length=124)
    comment = models.CharField(max_length=255)
    commented_by = models.ForeignKey(User)
    commented_to = models.ForeignKey(Venue)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    venue = models.ForeignKey("Venue", related_name='ratings', on_delete=models.CASCADE)
    rated_by = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('rated_by', 'venue')


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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
