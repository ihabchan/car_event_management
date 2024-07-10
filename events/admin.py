from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Post, Merch, Event, Cart, Wishlist, Purchase, EventParticipant

class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Merch)
admin.site.register(Event)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Purchase)
admin.site.register(EventParticipant)

from django.contrib import admin
from .models import CustomUser

