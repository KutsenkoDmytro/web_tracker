from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from . import views
from rest_framework import permissions

router = routers.DefaultRouter()
router.register(r'offer', views.OfferViewSet)
router.register(r'click', views.ClickViewSet)
router.register(r'lead', views.LeadViewSet)
router.register(r'campaign', views.CampaignViewSet)


schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="API for web analytics tracker",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@wat.local"),
      license=openapi.License(name="License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),  # http://127.0.0.1:8000/api/offer/
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
