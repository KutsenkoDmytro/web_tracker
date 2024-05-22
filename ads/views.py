import math
from collections import defaultdict
import json
from itertools import chain

from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

from ads.forms import LeadForm
from ads.functions import get_user_data, generate_colors, custom_serializer
from ads.models import Campaign, Offer, Click, Lead


def ads_list(request):
    campaigns = Campaign.objects.all()
    return render(request, 'ads/offer/list.html', {'campaigns': campaigns})


def landing_page_view(request, offer_slug):
    offer = get_object_or_404(Offer, slug=offer_slug)

    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            user_data = request.session.get('user_data')
            if user_data:
                del request.session['user_data']

            click_id = request.session.get('click_id')
            if click_id:
                click = get_object_or_404(Click, id=click_id)

                Lead.objects.create(
                    click=click,
                    email=form.cleaned_data['email'],
                    phone_number=form.cleaned_data['phone_number'],
                    **user_data
                )

                del request.session['click_id']

            if user_data['referrer']:
                return HttpResponseRedirect(user_data['referrer'])
    else:

        click = Click.objects.create(offer=offer)
        request.session['click_id'] = click.id

        user_data = get_user_data(request)
        request.session['user_data'] = user_data

        form = LeadForm()

    return render(request, 'ads/offer/feedback.html',
                  {'form': form, 'offer': offer})


def chart_view(request):
    all_clicks_by_dates = Click.objects \
        .annotate(date_item=TruncDate('timestamp')) \
        .values("date_item") \
        .annotate(clicks_count=Count('id')) \
        .order_by('date_item')

    all_leads_by_dates = Lead.objects \
        .annotate(date_item=TruncDate('timestamp')) \
        .values("date_item") \
        .annotate(leads_count=Count('id')) \
        .order_by('date_item')

    dates_list = sorted(
        set(chain(all_clicks_by_dates.values_list('date_item', flat=True),
                  all_leads_by_dates.values_list('date_item', flat=True))))

    data_by_date = defaultdict(lambda: {'leads_count': 0, 'clicks_count': 0})

    for lead in all_leads_by_dates:
        data_by_date[lead['date_item']]['leads_count'] = lead['leads_count']

    for click in all_clicks_by_dates:
        data_by_date[click['date_item']]['clicks_count'] = click['clicks_count']

    leads_list = [data_by_date[date]['leads_count'] for date in dates_list]
    clicks_list = [data_by_date[date]['clicks_count'] for date in dates_list]

    charts_data = {
        "chart_leads_and_clicks": {
            "dates_list": dates_list,
            "series": [
                {"name": "Ліди", "data": leads_list},
                {"name": "Кліки", "data": clicks_list},
            ]
        }
    }

    charts_data = json.dumps(charts_data, default=custom_serializer)

    return render(request, 'ads/visualization/chart.html',
                  {'charts_data': charts_data})


def dashboard_view(request):
    all_offers = Offer.objects.all()

    series = [
        [offer.title, offer.total_clicks(), offer.total_leads()]
        for offer in all_offers
    ]

    total_clicks = sum(offer.total_clicks() for offer in all_offers)
    total_leads = sum(offer.total_leads() for offer in all_offers)

    avg_clicks_per_offer = math.ceil(
        total_clicks / len(all_offers)) if all_offers else 0
    avg_leads_per_offer = math.ceil(
        total_leads / len(all_offers)) if all_offers else 0

    dashboard_data = {
        "dash_leads_and_clicks": {
            "series": series,
            "avg_clicks": avg_clicks_per_offer,
            "avg_leads": avg_leads_per_offer
        }
    }

    dashboard_data = json.dumps(dashboard_data, default=custom_serializer)

    return render(request, 'ads/visualization/dashboard.html',
                  {'dashboard_data': dashboard_data})


def diagram_view(request):
    filter_value = request.GET.get('filter', 'all')
    sort_value = request.GET.get('sort', 'asc')
    all_offers = Offer.objects.all()
    offers_list = list(all_offers)

    if filter_value != 'all':
        all_offers = all_offers.filter(id=filter_value)

    series = [
        [offer.title, round(offer.total_leads() / offer.total_clicks() * 100)]
        for offer in all_offers if offer.total_clicks() != 0
    ]

    series.sort(key=lambda x: x[1], reverse=(sort_value == 'desc'))

    colors = generate_colors(len(series))
    diagram_data = {
        'series': series,
        'colors': colors
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(diagram_data)

    return render(request, 'ads/visualization/diagram.html', {
        'diagram_data': diagram_data,
        'offers': offers_list,
        'current_filter': filter_value,
        'current_sort': sort_value
    })
