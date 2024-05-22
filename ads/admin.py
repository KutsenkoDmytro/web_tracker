from django.contrib import admin
from .models import Campaign, Offer, Click, Lead

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'cost_per_click', 'time_create', 'time_update', 'campaign',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ('offer', 'timestamp')

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'timestamp', 'operating_system', 'user_agent', 'referrer', 'email', 'phone_number')
