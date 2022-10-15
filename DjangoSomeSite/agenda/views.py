from datetime import datetime, timedelta

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.http.response import Http404, JsonResponse
from django.utils import timezone

from .models import Event

# Create your views here.


def str_to_aware_time(time: str) -> datetime:
    time = datetime.strptime(time, '%Y-%m-%dT%H:%M')
    return timezone.make_aware(time)


@login_required(login_url='/login/')
def list_event(request):
    user = request.user
    time_now = timezone.now()
    events = Event.objects.filter(
        user=user,
        date__gt=time_now - timedelta(hours=1)
    )
    data = {'events': events}
    return render(request, 'agenda/index.html', data)


@login_required(login_url='/login/')
def list_history(request):
    events = Event.objects.filter(
        user=request.user,
        date__lt=timezone.now() - timedelta(hours=1)
    )
    data = {'events': events}
    return render(request, 'agenda/history.html', data)


@login_required(login_url='/login/')
def new_event(request, event_id):
    data = {}
    if event_id:
        data['event'] = Event.objects.get(id=event_id)
    return render(request, 'agenda/new_event.html', data)


@login_required(login_url='/login/')
def submit_event(request):
    if request.POST:
        title = request.POST.get('title')
        date = str_to_aware_time(request.POST.get('date'))
        description = request.POST.get('description')
        local = request.POST.get('local')
        user = request.user
        event_id = request.POST.get('event_id')
        if event_id:
            Event.objects.filter(id=event_id).update(
                title=title,
                date=date,
                description=description,
                local=local
            )
        else:
            Event.objects.create(
                title=title,
                date=date,
                description=description,
                local=local,
                user=user
            )
    return redirect(reverse('agenda:index'))


@login_required(login_url='/login/')
def delete_event(request, event_id):
    user = request.user
    event = Event.objects.get(id=event_id)
    if user == event.user:
        event.delete()
    else:
        raise Http404()
    return redirect(reverse('agenda:index'))


@login_required(login_url='/login/')
def list_json(request):
    event = Event.objects.filter(
        user=request.user
    ).values('id', 'title', 'date',
             'creation_date', 'description', 'local')
    return JsonResponse(list(event), safe=False)
