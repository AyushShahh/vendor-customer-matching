from django.contrib import admin
from .models import Watchlist


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    list_filter = ('user', 'product')

admin.site.register(Watchlist, WatchlistAdmin)
