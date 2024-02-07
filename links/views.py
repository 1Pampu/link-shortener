from django.shortcuts import render
from django.shortcuts import redirect as django_redirect
from django.urls import reverse
from urllib.parse import urlencode
from .forms import LinkForm
from .models import Link, Click
from .utils import codeRandomizer, grapStatistics
import plotly.express as px
from datetime import timedelta
from django.utils import timezone
import pandas as pd

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)

        if form.is_valid():
            if not form.cleaned_data['short']:
                code = codeRandomizer(7)
                form.instance.short = code
            form.save()

            base_url = reverse('created')
            query_string = urlencode({'short': form.instance.short, 'original': form.instance.original})
            url = '{}?{}'.format(base_url, query_string)
            return django_redirect(url)

    else:
        form = LinkForm()

    return render(request, 'index.html', {'form': form})

def redirect(request, short):
    try:
        link = Link.objects.get(short=short)
    except Link.DoesNotExist:
        return render(request, '404.html', status=404)

    link.click()
    click = Click(link=link)
    click.save()
    return django_redirect(link.original)

def created(request):
    short = request.GET.get('short', None)
    original = request.GET.get('original', None)

    if not short or not original:
        return render(request, '404.html', status=404)

    try:
        link = Link.objects.get(short=short)
    except Link.DoesNotExist:
        return render(request, '404.html', status=404)

    return render(request, 'created.html', {'short': short, 'original': original})

def stats(request, short):
    try:
        link = Link.objects.get(short=short)
    except Link.DoesNotExist:
        return render(request, '404.html', status=404)

    lapse = request.GET.get('lapse', None)
    time_now =  timezone.now()

    graphContext = {}
    if lapse == '7':
        time_filter = time_now - timedelta(days=7)
        h1_time = "Last 7 days'"
        hours_or_days = range(0, 7)
        hours = False
        graphContext["total_hours_days"] = 7
        graphContext["label"] = "Day"
        graphContext["title"] = "Days"
    else:
        time_filter = time_now.replace(hour=0, minute=0, second=0, microsecond=0)
        h1_time = "Today's"
        hours_or_days = range(0, time_now.hour)
        hours = True
        graphContext["total_hours_days"] = time_now.hour
        graphContext["label"] = "Hour"
        graphContext["title"] = "Hour of the day (In UTC)"

    clicks = Click.objects.filter(link=link, date__gte=time_filter, date__lte = time_now)
    clicks_count = clicks.count()
    df = pd.DataFrame(list(clicks.values()))

    try:
        if hours:
            clicks_per_hour_day = df.groupby(df['date'].dt.hour).size().reset_index(name='Clicks')
        else:
            clicks_per_hour_day = df.groupby(df['date'].dt.day).size().reset_index(name='Clicks')

        for hour_day in hours_or_days:
            if hour_day not in clicks_per_hour_day['date'].values:
                row = pd.DataFrame({'date': hour_day, 'Clicks': 0}, index=[hour_day])
                clicks_per_hour_day = pd.concat([clicks_per_hour_day, row], ignore_index=True)

    except:
        clicks_per_hour_day = pd.DataFrame(columns=['date', 'Clicks'])
        for hour_day in hours_or_days:
            row = pd.DataFrame({'date': hour_day, 'Clicks': 0}, index=[hour_day])
            clicks_per_hour_day = pd.concat([clicks_per_hour_day, row], ignore_index=True)

    clicks_per_hour_day = clicks_per_hour_day.sort_values(by='date', ascending=True)
    clicks_per_hour_day.reset_index(inplace=True, drop=True)
    chart = grapStatistics(clicks_per_hour_day, clicks_count, graphContext)

    return render(request, 'stats.html', {'link': link, 'fig' : chart, 'h1_time': h1_time, 'clicks': clicks_count, 'lapse': lapse})