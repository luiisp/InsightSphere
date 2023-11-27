from django.contrib import admin
from .models import User
from .models import Channel

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'creator', 'verified')
    search_fields = ('name', 'description', 'creator__username')
    list_filter = ('verified',)

    actions = ['mark_as_verified', 'mark_as_unverified']

    def mark_as_verified(modeladmin, request, queryset):
        queryset.update(verified=True)
    mark_as_verified.short_description = "Marcar como verificado"

    def mark_as_unverified(modeladmin, request, queryset):
        queryset.update(verified=False)
    mark_as_unverified.short_description = "Marcar como não verificado"

admin.site.register(User)
admin.site.register(Channel, ChannelAdmin)
