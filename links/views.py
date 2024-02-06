from django.shortcuts import render
from django.urls import reverse
from urllib.parse import urlencode
from .forms import LinkForm
from .models import Link, Click
from django.shortcuts import redirect as django_redirect
from .utils import codeRandomizer

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