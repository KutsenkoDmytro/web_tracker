from django.test import TestCase
from django.utils import timezone

from .models import Campaign, Offer, Click, Lead


class CampaignModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Campaign.objects.create(name='Test Campaign', slug='test-campaign')

    def test_name_label(self):
        campaign = Campaign.objects.get(id=1)
        field_label = campaign._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Кампанія')

    def test_name_max_length(self):
        campaign = Campaign.objects.get(id=1)
        max_length = campaign._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)


class OfferModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        campaign = Campaign.objects.create(name='Test Campaign',
                                           slug='test-campaign')
        Offer.objects.create(title='Test Offer', slug='test-offer',
                             content='Test Content', cost_per_click=1.0,
                             campaign=campaign)

    def test_title_label(self):
        offer = Offer.objects.get(id=1)
        field_label = offer._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Офер')

    def test_total_clicks(self):
        offer = Offer.objects.get(id=1)
        self.assertEquals(offer.total_clicks(), 0)


class ClickModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        campaign = Campaign.objects.create(name='Test Campaign',
                                           slug='test-campaign')
        offer = Offer.objects.create(title='Test Offer', slug='test-offer',
                                     content='Test Content', cost_per_click=1.0,
                                     campaign=campaign)
        Click.objects.create(offer=offer, timestamp=timezone.now())

    def test_offer_label(self):
        click = Click.objects.get(id=1)
        field_label = click._meta.get_field('offer').verbose_name
        self.assertEquals(field_label, 'Офер')


class LeadModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        campaign = Campaign.objects.create(name='Test Campaign',
                                           slug='test-campaign')
        offer = Offer.objects.create(title='Test Offer', slug='test-offer',
                                     content='Test Content', cost_per_click=1.0,
                                     campaign=campaign)
        click = Click.objects.create(offer=offer, timestamp=timezone.now())
        Lead.objects.create(click=click, timestamp=timezone.now(),
                            ip_address='127.0.0.1', operating_system='Test OS',
                            user_agent='Test User Agent',
                            referrer='http://example.com',
                            email='test@example.com', phone_number='1234567890')

    def test_ip_address_label(self):
        lead = Lead.objects.get(id=1)
        field_label = lead._meta.get_field('ip_address').verbose_name
        self.assertEquals(field_label, 'IP адреса')

    def test_email(self):
        lead = Lead.objects.get(id=1)
        self.assertEquals(lead.email, 'test@example.com')
