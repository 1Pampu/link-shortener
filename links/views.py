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


    time_now =  timezone.now()
    time_filter = time_now.replace(hour=0, minute=0, second=0, microsecond=0)
    hours = range(0, time_now.hour)

    clicks = Click.objects.filter(link=link, date__gte=time_filter, date__lte = time_now)
    clicks_count = clicks.count()
    df = pd.DataFrame(list(clicks.values()))

    try:
        clicks_per_hour = df.groupby(df['date'].dt.hour).size().reset_index(name='Clicks')

        for hour in hours:
            if hour not in clicks_per_hour['date'].values:
                row = pd.DataFrame({'date': hour, 'Clicks': 0}, index=[hour])
                clicks_per_hour = pd.concat([clicks_per_hour, row], ignore_index=True)

    except:
        clicks_per_hour = pd.DataFrame(columns=['date', 'Clicks'])
        for hour in hours:
            row = pd.DataFrame({'date': hour, 'Clicks': 0}, index=[hour])
            clicks_per_hour = pd.concat([clicks_per_hour, row], ignore_index=True)

    clicks_per_hour = clicks_per_hour.sort_values(by='date', ascending=True)
    clicks_per_hour.reset_index(inplace=True, drop=True)
    chart = grapStatistics(clicks_per_hour, time_now.hour)

    context = {
        'link': link,
        'fig': chart,
        'clicks': clicks_count,
    }

    return render(request, 'stats.html', context)