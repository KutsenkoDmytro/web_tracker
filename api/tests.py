from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from ads.models import Offer, Click, Lead, Campaign

class ApiTests(TestCase):


    def setUp(self):

        self.admin_user = User.objects.create_superuser(username='admin',
                                                        email='admin@example.com',
                                                        password='adminpassword')
        self.client = APIClient()

        self.campaign = Campaign.objects.create(name='Test Campaign', slug='test-campaign')
        self.offer = Offer.objects.create(title='Test Offer', slug='test-offer', content='Test content', cost_per_click=10.00, campaign=self.campaign)
        self.click = Click.objects.create(offer=self.offer)
        self.lead = Lead.objects.create(click=self.click, ip_address='127.0.0.1', operating_system='Windows', user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36', email='test@example.com', phone_number='123456789')

    def test_offer_api(self):
        response = self.client.get('/api/offer/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_offer_api(self):

        self.client.login(username='admin', password='adminpassword')

        new_offer_data = {'title': 'New Test Offer', 'slug': 'new-test-offer', 'content': 'New test content', 'cost_per_click': 20.00, 'campaign': self.campaign.id}
        response = self.client.post('/api/offer/', new_offer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_click_api(self):
        response = self.client.get('/api/click/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lead_api(self):
        response = self.client.get('/api/lead/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_campaign_api(self):
        response = self.client.get('/api/campaign/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)