from django.urls import path
from . import views
from .views import landing_page_view, dashboard_view, chart_view, diagram_view

urlpatterns = [
    path('', views.ads_list, name='ads_list'),
    path('landing_page/<slug:offer_slug>/', landing_page_view, name='landing_page'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('chart/', chart_view, name='chart'),
    path('diagram/', diagram_view, name='diagram'),
]
