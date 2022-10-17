import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Event

# Create your tests here.


class EventModelTests(TestCase):

    def test_isimminent_for_future_and_past_events(self):
        """
        isimminent() returns False for past events and
        more than one hour in the future, True if it is
        less than one hour in the future.
        """
        future_time = timezone.now() + datetime.timedelta(minutes=61)
        past_time = timezone.now() - datetime.timedelta(minutes=1)
        imminent_time = timezone.now() + datetime.timedelta(minutes=30)

        future_event = Event(date=future_time)
        past_event = Event(date=past_time)
        imminent_event = Event(date=imminent_time)

        self.assertIs(future_event.isimminent(), False)
        self.assertIs(past_event.isimminent(), False)
        self.assertIs(imminent_event.isimminent(), True)

    def test_islate_with_future_and_past_events(self):
        """
        islate() returns False for past events and True for
        future events.
        """
        minute = datetime.timedelta(minutes=1)
        late_event = Event(date=timezone.now() - minute)
        future_event = Event(date=timezone.now() + minute)
        self.assertIs(late_event.islate(), True)
        self.assertIs(future_event.islate(), False)


def create_event(title, minutes, user):
    """
    Create a event with the given `title` and dated the given
    number of `minutes` offset to now.
    """
    date = timezone.now() + datetime.timedelta(minutes=minutes)
    return Event.objects.create(title=title, date=date, user=user)


class AgendaIndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(
            username='testuser', password='password'
        )

    def test_login_required_access(self):
        """
        User not logged in will be redirected to login page.
        After login access is granted.
        """
        response = self.client.get(reverse('agenda:index'))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(user=self.test_user)
        response = self.client.get(reverse('agenda:index'))
        self.assertEqual(response.status_code, 200)

    def test_no_events(self):
        """
        If no events exists, options to edit the events must not
        appear ('Editar' and 'Excluir').
        """
        self.client.force_login(user=self.test_user)
        response = self.client.get(reverse('agenda:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Editar')
        self.assertNotContains(response, 'Excluir')
        self.assertContains(response, 'Agendamentos')

    def test_event_in_index(self):
        """
        Future events must appear on index.
        Event.objects.create() must be called after login() method.
        force_login() is needed to access page, otherwise will
        get 302 status code.
        """
        self.client.login(username='testuser', password='password')
        title = 'Valid event.'
        event = create_event(
            title=title, minutes=30, user=self.test_user
        )
        self.assertIsNotNone(event)
        self.client.logout()

        self.client.force_login(user=self.test_user)
        response = self.client.get(reverse('agenda:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, title)
        self.assertContains(response, 'Excluir')
        self.assertContains(response, 'Editar')

    def test_late_event_in_index(self):
        """
        Events that are late up to 1 hour must appear on index.
        """
        self.client.login(username='testuser', password='password')
        too_late_title = 'Too late title.'
        not_too_late_title = 'Not too late title.'

        too_late_event = create_event(
            title=too_late_title, minutes=-61, user=self.test_user
        )
        not_too_late_event = create_event(
            title=not_too_late_title, minutes=-59, user=self.test_user
        )

        self.assertIsNotNone(too_late_event)
        self.assertIsNotNone(not_too_late_event)
        self.client.logout()

        self.client.force_login(user=self.test_user)
        response = self.client.get(reverse('agenda:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, not_too_late_title)
        self.assertNotContains(response, too_late_title)


class AgendaHistoryViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(
            username='testuser', password='password'
        )

    def test_future_and_past_events(self):
        """
        Events more than one hour late must appear on history view,
        future events must not.
        """
        future_title = 'Future title.'
        late_title = 'Late title.'
        past_title = 'Past title.'

        self.client.login(username='testuser', password='password')
        future_event = create_event(
            title=future_title, minutes=1, user=self.test_user
        )
        late_event = create_event(
            title=late_title, minutes=-59, user=self.test_user
        )
        past_event = create_event(
            title=past_title, minutes=-61, user=self.test_user
        )

        self.assertIsNotNone(future_event)
        self.assertIsNotNone(late_event)
        self.assertIsNotNone(past_event)
        self.client.logout()

        self.client.force_login(user=self.test_user)
        response = self.client.get(reverse('agenda:history'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, future_title)
        self.assertNotContains(response, late_title)
        self.assertContains(response, past_title)
