from rest_framework import serializers
from ads.models import Offer, Click, Lead, Campaign


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'

class ClickSerializer(serializers.ModelSerializer):

    class Meta:
        model = Click
        fields = '__all__'

class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = '__all__'