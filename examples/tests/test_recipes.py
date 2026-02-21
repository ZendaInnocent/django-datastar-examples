import pytest
from model_bakery import baker

pytestmark = pytest.mark.django_db


class TestContactRecipe:
    """Test cases demonstrating Contact recipe usage."""

    def test_make_single_contact(self):
        """Create a single contact using recipe."""
        contact = baker.make_recipe('examples.contact')
        assert contact.id is not None
        assert contact.email.startswith('user')

    def test_make_multiple_contacts(self):
        """Create multiple contacts at once."""
        contacts = baker.make_recipe('examples.contact', _quantity=5)
        assert len(contacts) == 5
        # Verify unique emails
        emails = [c.email for c in contacts]
        assert len(set(emails)) == 5

    def test_override_recipe_values(self):
        """Override recipe values at creation time."""
        contact = baker.make_recipe(
            'examples.contact',
            first_name='John',
            last_name='Doe',
        )
        assert contact.first_name == 'John'
        assert contact.last_name == 'Doe'

    def test_prepare_recipe(self):
        """Use prepare_recipe to create unsaved instances."""
        contact = baker.prepare_recipe('examples.contact')
        assert contact.id is None  # Not saved to DB
        assert contact.email is not None


class TestTodoRecipe:
    """Test cases demonstrating Todo recipe usage."""

    def test_make_single_todo(self):
        """Create a single todo using recipe."""
        todo = baker.make_recipe('examples.todo')
        assert todo.id is not None
        assert todo.is_completed is False

    def test_make_completed_todo(self):
        """Create a completed todo."""
        todo = baker.make_recipe('examples.todo_completed')
        assert todo.is_completed is True

    def test_make_multiple_todos(self):
        """Create multiple todos with baker.baker.sequential ordering."""
        todos = baker.make_recipe('examples.todo', _quantity=3)
        assert len(todos) == 3
        # Verify baker.baker.sequential order (within this batch)
        assert todos[0].order == todos[1].order - 1
        assert todos[1].order == todos[2].order - 1


class TestNotificationRecipe:
    """Test cases demonstrating Notification recipe usage."""

    def test_make_single_notification(self):
        """Create a single notification."""
        notification = baker.make_recipe('examples.notification')
        assert notification.id is not None
        assert notification.read is False

    def test_make_read_notification(self):
        """Create a read notification."""
        notification = baker.make_recipe('examples.notification_read')
        assert notification.read is True

    def test_cycled_notifications(self):
        """Create notifications with cycling messages."""
        notifications = baker.make_recipe('examples.notification_cycled', _quantity=3)
        assert len(notifications) == 3
        # Messages should cycle - check pattern
        assert notifications[0].message != notifications[1].message
        assert notifications[1].message != notifications[2].message


class TestItemRecipe:
    """Test cases demonstrating Item recipe usage."""

    def test_make_single_item(self):
        """Create a single item."""
        item = baker.make_recipe('examples.item')
        assert item.id is not None

    def test_make_item_with_description(self):
        """Create an item with description."""
        item = baker.make_recipe('examples.item_with_description')
        assert item.description != ''

    def test_make_multiple_items(self):
        """Create multiple items with baker.baker.sequential ordering."""
        items = baker.make_recipe('examples.item', _quantity=4)
        assert len(items) == 4
        # Verify baker.baker.sequential order (within this batch)
        assert items[0].order == items[1].order - 1
        assert items[2].order == items[3].order - 1
