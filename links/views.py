from django.shortcuts import render
from .forms import LinkForm
from .models import Link, Click
from django.shortcuts import redirect as django_redirect

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, 'created.html', {'short': form.instance.short, 'original': form.instance.original})

    else:
        form = LinkForm()

    return render(request, 'index.html', {'form': form})

def redirect(request, short):
    try:
        link = Link.objects.get(short=short)
    except Link.DoesNotExist:
        return django_redirect('index')

    link.click()
    click = Click(link=link)
    click.save()
    return django_redirect(link.original)