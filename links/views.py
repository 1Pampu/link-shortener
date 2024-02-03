from django.shortcuts import render
from .forms import LinkForm
from .models import Link, Click
from django.shortcuts import redirect as django_redirect

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)

        if form.is_valid():
            if request.user.is_authenticated:
                form.save(user=request.user)
            else:
                form.save()
    else:
        form = LinkForm()

    context = {
        'form': form
    }

    return render(request, 'index.html', context)

def redirect(request, short):
    try:
        link = Link.objects.get(short=short)
    except Link.DoesNotExist:
        return django_redirect('index')

    link.click()
    if link.user:
        click = Click(link=link)
        click.save()
    return django_redirect(link.original)