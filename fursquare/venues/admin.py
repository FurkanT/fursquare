from django.contrib import admin
from .models import Venue, VenueType, Profile, Comment, Rating
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class VenueAdmin(admin.ModelAdmin):
    model = Venue
    list_display = ('venue_name', 'venue_type', 'venue_address', 'phone_number', 'rating', 'total_vote_count')
    search_fields = ('venue_name', 'venue_type')


class VenueTypeAdmin(admin.ModelAdmin):
    model = VenueType
    list_display = ('venue_type', 'created_by', 'approved')


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('title', 'comment', 'commented_by', 'commented_to', 'created_date', 'updated_date')


class RatingAdmin(admin.ModelAdmin):
    model = Rating


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'get_date_of_birth', 'get_avatar', 'is_active', 'is_staff')
    list_select_related = ('profile',)
    search_fields = ('username', )

    def get_date_of_birth(self, instance):
        return instance.profile.date_of_birth
    get_date_of_birth.short_description = 'Birthday'

    def get_avatar(self, instance):
        return instance.profile.avatar

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(VenueType, VenueTypeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Rating, RatingAdmin)

