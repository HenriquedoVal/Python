from django.shortcuts import render
from django.conf import settings


def index(request):
    apps = [app[:app.index('.')] for app in settings.INSTALLED_APPS
            if not app.startswith('django.')]
    return render(
        request,
        'somesite/index.html',
        {'apps': apps}
    )
