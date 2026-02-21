"""
Tests for the seed_data management command.
"""

import pytest
from io import StringIO
from django.core.management import call_command

from examples.models import Contact, Todo, Notification, Item


@pytest.mark.django_db
class TestSeedDataCommand:
    """Test the seed_data management command."""

    def test_seed_data_creates_contacts(self):
        """Verify seed_data creates expected number of contacts."""
        call_command('seed_data', stdout=StringIO())
        assert Contact.objects.count() == 12

    def test_seed_data_creates_todos(self):
        """Verify seed_data creates expected number of todos."""
        call_command('seed_data', stdout=StringIO())
        assert Todo.objects.count() == 7

    def test_seed_data_creates_items(self):
        """Verify seed_data creates expected number of items."""
        call_command('seed_data', stdout=StringIO())
        assert Item.objects.count() == 5

    def test_seed_data_creates_notifications(self):
        """Verify seed_data creates expected number of notifications."""
        call_command('seed_data', stdout=StringIO())
        assert Notification.objects.count() == 12

    def test_seed_data_clears_existing_data(self):
        """Verify seed_data clears existing data before creating new."""
        Contact.objects.create(first_name='Old', last_name='Data', email='old@test.com')
        call_command('seed_data', stdout=StringIO())
        assert Contact.objects.filter(first_name='Old').count() == 0

    def test_seed_data_output(self):
        """Verify seed_data outputs success messages."""
        out = StringIO()
        call_command('seed_data', stdout=out)
        output = out.getvalue()
        assert 'Created 12 contacts' in output
        assert 'Created 7 todos' in output
        assert 'Created 5 items' in output
        assert 'Created 12 notifications' in output
        assert 'Successfully seeded database' in output

    def test_seed_data_todo_completed_status(self):
        """Verify todos have correct completed status."""
        call_command('seed_data', stdout=StringIO())
        completed_count = Todo.objects.filter(is_completed=True).count()
        assert completed_count == 3, (
            f'Expected 3 completed todos (indices 0,3,6), got {completed_count}'
        )

    def test_seed_data_notification_read_status(self):
        """Verify notifications have correct read status."""
        call_command('seed_data', stdout=StringIO())
        read_count = Notification.objects.filter(read=True).count()
        unread_count = Notification.objects.filter(read=False).count()
        assert read_count == 9, f'Expected 9 read notifications, got {read_count}'
        assert unread_count == 3, f'Expected 3 unread notifications, got {unread_count}'

    def test_seed_data_ordering(self):
        """Verify items are ordered correctly."""
        call_command('seed_data', stdout=StringIO())
        items = list(Item.objects.values_list('name', flat=True))
        assert items[0] == 'First Item'
        assert items[-1] == 'Fifth Item'
