from django.contrib import admin
from .models import Room


class RoomDataAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'player1', 'player2', 'score_player1', 'score_player2')

admin.site.register(Room, RoomDataAdmin)