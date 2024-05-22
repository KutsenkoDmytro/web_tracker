from rest_framework import viewsets
from ads.models import Offer, Click, Lead, Campaign
from .serializers import OfferSerializer, ClickSerializer, LeadSerializer, \
    CampaignSerializer
from .permissions import IsAdminOrReadOnly


class CampaignViewSet(viewsets.ModelViewSet):

    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = (IsAdminOrReadOnly,)


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ClickViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Click.objects.all()
    serializer_class = ClickSerializer
    permission_classes = (IsAdminOrReadOnly,)


class LeadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = (IsAdminOrReadOnly,)
